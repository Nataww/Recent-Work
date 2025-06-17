from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.cognito import CognitoService
from app.s3 import S3Service
from flask_login import login_required, current_user, login_user, logout_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
import functools
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# User class for Login
class User:
    def __init__(self, username, token_data=None):
        self.id = username
        self.username = username
        self.token_data = token_data
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        return self.username

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class ConfirmForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    confirmation_code = StringField('Confirmation Code', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class UploadForm(FlaskForm):
    file = FileField('Select File', validators=[
        DataRequired(),
       
    ])
    submit = SubmitField('Upload File')


cognito_service = CognitoService()
s3_service = S3Service()


from app import login_manager
@login_manager.user_loader
def load_user(user_id):
    logger.info(f"Loading user: {user_id}")
    if 'user' in session and session['user']['username'] == user_id:
        user = User(
            username=user_id, 
            token_data=session['user'].get('token_data')
        )
        logger.info(f"User {user_id} loaded from session")
        return user
    logger.warning(f"User {user_id} not found in session")
    return None


main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__, url_prefix='/auth')
files = Blueprint('files', __name__, url_prefix='/files')

# Authentication routes
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        result = cognito_service.sign_up(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data,
            name=form.name.data
        )
        
        if result['status'] == 'success':
            
            session['pending_confirmation'] = form.username.data
            flash('Registration successful! Check your email for the verification code.', 'success')
            flash('Enter the code on the next page to complete your account setup.', 'info')
            return redirect(url_for('auth.confirm'))
        else:
            flash(f"Error: {result['message']}", 'danger')
    
    return render_template('login.html', form=form, action='register')

@auth.route('/confirm', methods=['GET', 'POST'])
def confirm():
    form = ConfirmForm()
    
    
    if 'pending_confirmation' in session and not form.username.data:
        form.username.data = session['pending_confirmation']
    
    if form.validate_on_submit():
        result = cognito_service.confirm_sign_up(
            username=form.username.data,
            confirmation_code=form.confirmation_code.data
        )
        
        if result['status'] == 'success':
            
            if 'pending_confirmation' in session:
                session.pop('pending_confirmation')
                
            flash('Email verified successfully. You can now login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(f"Error: {result['message']}", 'danger')
    
    return render_template('login.html', form=form, action='confirm')

@auth.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        logger.info(f"User already authenticated: {current_user.username}")
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        logger.info(f"Login attempt for user: {form.username.data}")
        result = cognito_service.sign_in(
            username=form.username.data,
            password=form.password.data
        )
        
        if result['status'] == 'success':
            logger.info(f"Login successful for: {form.username.data}")
            
            # Store user info in session
            session['user'] = {
                'username': form.username.data,
                'token_data': result['data']
            }
            
            # Create user object and login
            user = User(username=form.username.data, token_data=result['data'])
            login_success = login_user(user, remember=True)
            logger.info(f"Flask-Login success: {login_success}")
            
            # Force session save
            session.modified = True
            
            logger.info(f"Redirecting to main index")
            next_page = request.args.get('next')
            if next_page:
                logger.info(f"Redirecting to next page: {next_page}")
            return redirect(next_page or url_for('main.index'))
        else:
            logger.error(f"Login failed: {result['message']}")
            flash(f"Error: {result['message']}", 'danger')
    
    return render_template('login.html', form=form, action='login')

@auth.route('/logout')
def logout():
    logout_user()
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

# Add a new route for verification
@auth.route('/verify')
def verify():
    """Direct link to the verification page"""
    # Redirect to the confirmation page
    return redirect(url_for('auth.confirm'))

# Main routes
@main.route('/')
@login_required
def index():
    logger.info(f"Root index page accessed by user: {current_user.username}")
    return redirect(url_for('files.list'))  # Redirect root to /files/list

# Debug route to check session
@main.route('/debug_session')
def debug_session():
    """Debug endpoint to check session state"""
    logger.info("Debug session page accessed")
    content = []
    content.append("<h1>Session Debug</h1>")
    
    # Check current_user
    if hasattr(current_user, 'is_authenticated'):
        content.append(f"<p>current_user.is_authenticated: {current_user.is_authenticated}</p>")
        if current_user.is_authenticated:
            content.append(f"<p>current_user.username: {current_user.username}</p>")
    else:
        content.append("<p>No current_user found</p>")
    
    # Check session
    content.append("<h2>Session Contents:</h2>")
    content.append("<pre>")
    for key, value in session.items():
        content.append(f"{key}: {value}")
    content.append("</pre>")
    
    return "<br>".join(content)

@files.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    
    if form.validate_on_submit():
        file = form.file.data
        storage_class = request.form.get('storage_class', 'STANDARD')
        folder = request.form.get('folder', 'root')
        
        # Log start of upload process
        logger.info(f"Starting file upload process for user: {current_user.username}")
        
        result = s3_service.upload_file(
            file=file,
            username=current_user.username,
            folder=folder,
            storage_class=storage_class
        )
       
        if result['status'] == 'success':
            logger.info(f"File upload completed successfully for user: {current_user.username}")
        else:
            logger.error(f"File upload failed for user: {current_user.username}, error: {result['message']}")
        
        if result['status'] == 'success':
        
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'status': 'success',
                    'message': 'File uploaded successfully',
                    'redirect': url_for('files.list'),
                    'file_info': {
                        'filename': file.filename,
                        'size': result.get('data', {}).get('size', 0),
                        'file_url': result.get('data', {}).get('file_url', ''),
                        'storage_class': result.get('data', {}).get('storage_class', 'STANDARD')
                    }
                })
            
            # Regular form submission
            flash('File uploaded successfully.', 'success')
            return redirect(url_for('files.list'))
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'status': 'error',
                    'message': result['message']
                }), 400
            
            # Regular form submission error
            flash(f"Error: {result['message']}", 'danger')
    
    # Get the list of folders for the dropdown
    folder_result = s3_service.list_files(username=current_user.username)
    folders = []
    
    if folder_result['status'] == 'success' and 'folders' in folder_result['data']:
        folders = folder_result['data']['folders']
    
    
    return render_template('upload.html', form=form, folders=folders)

@files.route('/list')
@login_required
def list():
    result = s3_service.list_files(username=current_user.username)
    
    if result['status'] == 'success':
        # Extract files and folders from the result
        files = result['data']['files']
        folders = result['data']['folders']
        
        return render_template('files.html', files=files, folders=folders)
    else:
        flash(f"Error: {result['message']}", 'danger')
        return redirect(url_for('main.index'))

@files.route('/delete/<path:file_key>', methods=['POST'])
@login_required
def delete(file_key):
    # Ensure the file belongs to the current user
    if not file_key.startswith(f"users/{current_user.username}/"):
        flash("Access denied: You can only delete your own files.", 'danger')
        return redirect(url_for('files.list'))
    
    result = s3_service.delete_file(file_key=file_key)
    
    if result['status'] == 'success':
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'status': 'success',
                'message': 'File deleted successfully'
            })
        
        
        flash('File deleted successfully.', 'success')
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'status': 'error',
                'message': result['message']
            }), 400
            
        
        flash(f"Error: {result['message']}", 'danger')
    
    return redirect(url_for('files.list'))

@files.route('/download/<path:file_key>')
@login_required
def download(file_key):
    # Ensure the file belongs to the current user
    if not file_key.startswith(f"users/{current_user.username}/"):
        flash("Access denied: You can only download your own files.", 'danger')
        return redirect(url_for('files.list'))
    
    result = s3_service.generate_presigned_url(file_key=file_key)
    
    if result['status'] == 'success':
        return redirect(result['data']['url'])
    else:
        flash(f"Error: {result['message']}", 'danger')
        return redirect(url_for('files.list'))

@files.route('/share')
@login_required
def share():
    # Get the file key from the query string
    file_key = request.args.get('file_key')
    
    if not file_key:
        return jsonify({'status': 'error', 'message': 'File key is required.'}), 400

    # Ensure the file belongs to the current user
    if not file_key.startswith(f"users/{current_user.username}/"):
        return jsonify({'status': 'error', 'message': 'Access denied: You can only share your own files.'}), 403
    
    # Generate a presigned URL for sharing the file.
    result = s3_service.generate_presigned_url(file_key=file_key, expiration=86400)  # 24 hours
    
    if result['status'] == 'success':
        # Return the shareable link in JSON format
        return jsonify({'status': 'success', 'link': result['data']['url']})
    else:
        # Return an error message if something went wrong
        return jsonify({'status': 'error', 'message': result['message']}), 500

@files.route('/get_presigned_url')
@login_required
def get_presigned_url():
    """Generate a presigned URL for previewing a file"""
    # Get the file key from the query string
    file_key = request.args.get('file_key')
    
    if not file_key:
        return jsonify({'status': 'error', 'message': 'File key is required.'}), 400

    # Ensure the file belongs to the current user
    if not file_key.startswith(f"users/{current_user.username}/"):
        return jsonify({'status': 'error', 'message': 'Access denied: You can only preview your own files.'}), 403
    
    # Generate a presigned URL with a shorter expiration for preview (5 minutes)
    result = s3_service.generate_presigned_url(file_key=file_key, expiration=300)
    
    if result['status'] == 'success':
        return jsonify({'status': 'success', 'url': result['data']['url']})
    else:
        return jsonify({'status': 'error', 'message': result['message']}), 500

@files.route('/create_folder', methods=['POST'])
@login_required
def create_folder():
    """Create a new folder in user's S3 space"""
    folder_name = request.form.get('folder_name')
    
    if not folder_name:
        return jsonify({'status': 'error', 'message': 'Folder name is required.'}), 400
        
    # Validate folder name (no special characters except - and _)
    import re
    if not re.match(r'^[a-zA-Z0-9\-_]+$', folder_name):
        return jsonify({'status': 'error', 'message': 'Folder name can only contain letters, numbers, hyphens, and underscores.'}), 400
    
    # Create the folder
    result = s3_service.create_folder(username=current_user.username, folder_name=folder_name)
    
    if result['status'] == 'success':
        return jsonify({'status': 'success', 'message': 'Folder created successfully'})
    else:
        return jsonify({'status': 'error', 'message': result['message']}), 500

@files.route('/change_storage_class', methods=['POST'])
@login_required
def change_storage_class():
    """Change the storage class of a file"""
    file_key = request.form.get('file_key')
    storage_class = request.form.get('storage_class')
    
    if not file_key or not storage_class:
        return jsonify({'status': 'error', 'message': 'File key and storage class are required.'}), 400

    # Security check: Ensure the file belongs to the current user
    if not file_key.startswith(f"users/{current_user.username}/"):
        return jsonify({'status': 'error', 'message': 'Access denied: You can only modify your own files.'}), 403
    
    # Valid storage classes
    valid_storage_classes = [
        'STANDARD', 'REDUCED_REDUNDANCY', 'STANDARD_IA', 
        'ONEZONE_IA', 'INTELLIGENT_TIERING', 'GLACIER', 
        'DEEP_ARCHIVE', 'GLACIER_IR'
    ]
    
    if storage_class not in valid_storage_classes:
        return jsonify({'status': 'error', 'message': 'Invalid storage class.'}), 400
    
    result = s3_service.change_storage_class(file_key=file_key, storage_class=storage_class)
    
    if result['status'] == 'success':
        return jsonify({'status': 'success', 'message': 'Storage class changed successfully'})
    else:
        return jsonify({'status': 'error', 'message': result['message']}), 500

@main.route('/dashboard')
@login_required
def dashboard():
    # Fetch user storage data from the S3 service
    username = current_user.username
    result = s3_service.list_files(username=username)
    
    if result['status'] == 'success':
        files = result['data']['files']
        
        # Calculate total storage used
        total_storage_used = sum(file['size'] for file in files) / (1024 * 1024)  # Convert to MB
        
        # Calculate storage by file type
        file_type_storage = {}
        for file in files:
            file_extension = file['filename'].split('.')[-1].lower()
            file_type_storage[file_extension] = file_type_storage.get(file_extension, 0) + file['size']
        
        # Sort file types by storage used and get top 5
        top_file_types = sorted(file_type_storage.items(), key=lambda x: x[1], reverse=True)[:5]
        top_file_types = [{'type': t[0].upper(), 'size': t[1] / (1024 * 1024)} for t in top_file_types]  # Convert to MB
        
        # Calculate item counts by storage class
        storage_class_counts = {}
        for file in files:
            storage_class = file['storage_class']
            storage_class_counts[storage_class] = storage_class_counts.get(storage_class, 0) + 1
        
        return render_template('dashboard.html',
                               username=username,
                               total_storage_used=total_storage_used,
                               top_file_types=top_file_types,
                               storage_class_counts=storage_class_counts)
    else:
        flash(f"Error: {result['message']}", 'danger')
        return redirect(url_for('main.index'))