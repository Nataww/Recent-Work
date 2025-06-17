# -*- coding: utf-8 -*-
# ==============================================================================
# Copyright (c) 2024 Xavier de Carné de Carnavalet
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ==============================================================================

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, abort, flash
from flask_mysqldb import MySQL
from flask_session import Session
from src.pwned import is_pwned
import yaml
from io import BytesIO
import os
import hashlib
import pyotp
import qrcode
import logging
import json
from src.captchas import generate_captcha, generate_captcha_image


app = Flask(__name__)

# Configure secret key and Flask-Session
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'  # Options: 'filesystem', 'redis', 'memcached', etc.
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True  # To sign session cookies for extra security
app.config['SESSION_FILE_DIR'] = './sessions'  # Needed if using filesystem type

# Load database configuration from db.yaml or configure directly here
db_config = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db_config['mysql_host']
app.config['MYSQL_USER'] = db_config['mysql_user']
app.config['MYSQL_PASSWORD'] = db_config['mysql_password']
app.config['MYSQL_DB'] = db_config['mysql_db']

mysql = MySQL(app)

#set XSS
app.config['SESSION_COOKIE_HTTPONLY'] = True
# set HTTPS secure
app.config['SESSION_COOKIE_SECURE'] = True

# Initialize the Flask-Session
Session(app)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    sender_id = session['user_id']
    return render_template('chat.html', sender_id=sender_id)

@app.route('/users')
def users():
    if 'user_id' not in session:
        abort(403)

    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id, username FROM users")
    user_data = cur.fetchall()
    cur.close()

    filtered_users = [[user[0], user[1]] for user in user_data if user[0] != session['user_id']]
    return {'users': filtered_users}

@app.route('/register', methods=['GET','POST'])
def register():
    # Default error is none
    error = None
    # If user input register information
    if request.method == 'POST':
        # Get user input
        registerDetails = request.form
        username = registerDetails["username"]
        password = registerDetails["password"]
        confirmPassword = registerDetails["confirm_password"]

        # Generate otp and recovery_key
        otp_secret = pyotp.random_base32()
        recovery_key = pyotp.random_base32()
        
        # Using SHA-256 to hash user password
        hashed_password = hashlib.sha256()
        hashed_password.update(password.encode('utf-8'))
        hashed_password = hashed_password.hexdigest()

        # Get the number of the username
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
        result = cur.fetchone()
        cur.close()

        # If username is greater than 1, it means the username exists
        if result[0] > 0:
            error = "Username already exists. Please choose a different username."
            return render_template('register.html', error=error)
    
        # Check whether the password and the confirmPassword are the same
        if password == confirmPassword:

            # Check the password is it pwned
            if is_pwned(password):
                error = f"The password '{password}' has been pwned! Please change a stronger password"
                return render_template('register.html', error=error)
            
            # Write data into database
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (username, password, otp_secret, recovery_key) VALUES (%s, %s, %s, %s)", (username, hashed_password, otp_secret, recovery_key))
            mysql.connection.commit()
            cur.close()

            # Generate the OTP URI for the QR code
            otp_uri = pyotp.totp.TOTP(otp_secret).provisioning_uri(username, issuer_name='app')

            # Generate the QR code
            qr = qrcode.QRCode()
            qr.add_data(otp_uri)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Save the QR code image
            qr_img_path = f"static/{username}_qr.png"
            qr_img.save(qr_img_path)

            flash('You are now registered.')
            return render_template('register.html', username=username, qr_img_path=qr_img_path, recovery_key=recovery_key)
        else:
            error = 'The password confirmation does not match'
    return render_template('register.html', error=error)
    

@app.route('/fetch_messages')
def fetch_messages():
    if 'user_id' not in session:
        abort(403)

    last_message_id = request.args.get('last_message_id', 0, type=int)
    peer_id = request.args.get('peer_id', type=int)
    
    cur = mysql.connection.cursor()
    query = """SELECT message_id,sender_id,receiver_id,message_text,iv,signature FROM messages 
               WHERE message_id > %s AND 
               ((sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s))
               ORDER BY message_id ASC"""
    cur.execute(query, (last_message_id, peer_id, session['user_id'], session['user_id'], peer_id))

    # Fetch the column names
    column_names = [desc[0] for desc in cur.description]
    # Fetch all rows, and create a list of dictionaries, each representing a message
    messages = [dict(zip(column_names, row)) for row in cur.fetchall()]
    # print(messages)
    cur.close()
    return jsonify({'messages': messages})

# In-memory dictionary to store failed login attempts
failed_login_attempts = {}

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Default there is no error
    error = None
    if request.method == 'POST':
        
        # Initialize the IP address
        ip_address = None

        # Get current user IP address
        if 'HTTP_X_REAL_IP' in request.environ:
            ip_address = request.environ['HTTP_X_REAL_IP']
        else:
            ip_address = request.remote_addr

        # Check if the IP address exists in the failed_login_attempts dictionary
        if ip_address in failed_login_attempts:
            # Increment the login attempt count for the IP address
            failed_login_attempts[ip_address] += 1
        else:
            # Initialize the login attempt count for the IP address
            failed_login_attempts[ip_address] = 1

        # Check if the login attempt count exceeds the threshold (e.g., 5 failed attempts)
        failed_attempts_threshold = 5
        if failed_login_attempts[ip_address] > failed_attempts_threshold:
            # Block the IP address by returning an error response
            return jsonify({'error': 'Too many failed login attempts. Your IP has been blocked.'}), 403

        # Store the user value in the session
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']
        otp = request.form['otp']
        if (userDetails['token']!= session["token"]):
            redirect(url_for('login'))
        # Get user data in database for verification
        cur = mysql.connection.cursor()
        cur.execute("SELECT user_id, password FROM users WHERE username=%s", (username,))
        account = cur.fetchone()
        cur.execute("SELECT otp_secret, recovery_key FROM users WHERE username = %s", (username,))
        result = cur.fetchone()

        # Initialize stored password
        stored_password = None

        # Ensure that user is registered
        if result is not None:
            otp_secret = result[0]
            recovery_key = result[1]
            totp = pyotp.TOTP(otp_secret)
            stored_password = hashlib.sha256()
            stored_password.update(password.encode('utf-8'))
            stored_password = stored_password.hexdigest()
        
        # Check the user otp and password are correct or not
        if stored_password is not None and stored_password == account[1]:
            if totp.verify(otp) or otp == recovery_key:
                session['username'] = username
                session['user_id'] = account[0]
                failed_login_attempts.pop(ip_address, None)
                return redirect(url_for('captcha'))
            else:    
                error = "Invalid OTP"
        else:
            error = 'Invalid credentials'
    token = str(os.urandom(255))
    session["token"] = token
    return render_template('login.html', error=error, token = token)

@app.route('/captcha', methods=['GET', 'POST'])
def captcha():
    # Implement proper session binding requirements
    if 'username' not in session or 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        # Generate a new CAPTCHA and store it in the session
        captcha = generate_captcha()
        session['captcha'] = captcha
        image_path = generate_captcha_image(captcha)

        return render_template('captcha.html', image_path=image_path)

    elif request.method == 'POST':
        captcha_session = session.get('captcha')
        user_captcha = request.form['captcha']

        # Verify the CAPTCHA
        if user_captcha != captcha_session:
            flash('Invalid CAPTCHA. Please try again.')
            return redirect(url_for('captcha'))
    return redirect(url_for('index'))

@app.route('/send_message', methods=['POST'])
def send_message():
    if not request.json or not 'message_text' in request.json:
        abort(400)  # Bad request if the request doesn't contain JSON or lacks 'message_text'
    if 'user_id' not in session:
        abort(403)

    # Extract data from the request
    sender_id = session['user_id']
    receiver_id = request.json['receiver_id']
    message_text = request.json['message_text']
    iv = request.json['iv']
    signature = request.json['signature']

    # Assuming you have a function to save messages
    save_message(sender_id, receiver_id, message_text,iv,signature)
    
    return jsonify({'status': 'success', 'message': 'Message sent'}), 200

def save_message(sender, receiver, message, iv, signature):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO messages (sender_id, receiver_id, message_text,iv, signature) VALUES (%s, %s, %s, %s, %s)", (sender, receiver, message,iv, signature))
    mysql.connection.commit()
    cur.close()

@app.route('/erase_chat', methods=['POST'])
def erase_chat():
    if 'user_id' not in session:
        abort(403)

    peer_id = request.json['peer_id']
    cur = mysql.connection.cursor()
    query = "DELETE FROM messages WHERE ((sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s))"
    cur.execute(query, (peer_id, session['user_id'], session['user_id'], peer_id))
    mysql.connection.commit()

    # Check if the operation was successful by evaluating affected rows
    if cur.rowcount > 0:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'failure'}), 200

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been successfully logged out.', 'info')  # Flash a logout success message
    return redirect(url_for('index'))

user_id_public_key_map = {}

@app.route('/exchange_key', methods=['POST'])
def exchange_key_sender():
    if 'user_id' not in session:
        abort(403)
    sender_id = int(session['user_id'])
    receiver_id = int(request.json['receiver_id'])

    publickey = request.json['publickey']
    salt = request.json['salt']
    user_id_public_key_map[sender_id] = {}
    user_id_public_key_map[sender_id][receiver_id] = {
        "publickey": publickey,
        "salt": salt
    }
    return jsonify({"result":"Success"})


@app.route('/exchange_key_receive')
def exchange_key_receive():
    recieving_keys = {}
    receiver_id = session['user_id']
    for sender_id in user_id_public_key_map.keys():
        if receiver_id in user_id_public_key_map[sender_id]:
            recieving_keys[sender_id] = user_id_public_key_map[sender_id][receiver_id]
            del user_id_public_key_map[sender_id][receiver_id]
    return jsonify(recieving_keys)

user_id_salt_map = {}
@app.route('/exchange_refrash_key', methods=["POST"])
def exchange_refrash_key():
    if 'user_id' not in session:
        abort(403)
    sender_id = int (session['user_id'])
    receiver_id = int(request.json['receiver_id'])
    ciphertext = request.json['encryptedMessage']
    signature = request.json['signature']
    iv = request.json['iv']
    salt = request.json["salt"]
    
    user_id_salt_map[sender_id] = {}
    user_id_salt_map[sender_id][receiver_id] = {
        "salt": salt,
        "ciphertext": ciphertext,
        "signature": signature,
        "iv": iv
    }
    return jsonify({"result":"Success"})

@app.route('/exchange_refrash_key_receive')
def exchange_refrash_key_receive():
    recieving_salts ={}
    receiver_id = session["user_id"]
    for sender_id in user_id_salt_map.keys():
        if receiver_id in user_id_salt_map[sender_id]:
            recieving_salts[sender_id] = user_id_salt_map[sender_id][receiver_id]
            del user_id_salt_map[sender_id][receiver_id]
    return jsonify(recieving_salts)

if __name__ == '__main__':
    app.run(debug=True)

