import boto3
import hmac
import hashlib
import base64
import os
from app.config import Config

class CognitoService:
    def __init__(self):
        self.client = boto3.client('cognito-idp', region_name=Config.AWS_REGION)
        self.user_pool_id = Config.COGNITO_USER_POOL_ID
        self.client_id = Config.COGNITO_APP_CLIENT_ID
        self.client_secret = Config.COGNITO_APP_CLIENT_SECRET

    def get_secret_hash(self, username):
        if not self.client_secret:
            return None
            
        message = username + self.client_id
        try:
            dig = hmac.new(
                key=bytes(self.client_secret, 'utf-8'),
                msg=bytes(message, 'utf-8'),
                digestmod=hashlib.sha256
            ).digest()
            return base64.b64encode(dig).decode()
        except Exception as e:
            print(f"Error generating secret hash: {str(e)}")
            return None

    def sign_up(self, username, password, email, name=None):
        """Register a new user with Cognito"""
        try:
            
            user_attributes = [
                {
                    'Name': 'email',
                    'Value': email
                }
            ]
            
            
            if name:
                user_attributes.append({
                    'Name': 'name',
                    'Value': name
                })
            
            sign_up_params = {
                'ClientId': self.client_id,
                'Username': username,
                'Password': password,
                'UserAttributes': user_attributes
            }
            
            
            secret_hash = self.get_secret_hash(username)
            if secret_hash:
                sign_up_params['SecretHash'] = secret_hash
                
            response = self.client.sign_up(**sign_up_params)
            return {
                'status': 'success',
                'message': 'Registration successful. Please check your email for verification code.',
                'data': response
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def confirm_sign_up(self, username, confirmation_code):
        """Confirm user registration with verification code"""
        try:
            confirm_params = {
                'ClientId': self.client_id,
                'Username': username,
                'ConfirmationCode': confirmation_code
            }
            
           
            secret_hash = self.get_secret_hash(username)
            if secret_hash:
                confirm_params['SecretHash'] = secret_hash
                
            response = self.client.confirm_sign_up(**confirm_params)
            return {
                'status': 'success',
                'message': 'Email verification successful. You can now login.',
                'data': response
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def sign_in(self, username, password):
        """Authenticate a user with Cognito"""
        try:
            auth_params = {
                'USERNAME': username,
                'PASSWORD': password
            }
            
            
            secret_hash = self.get_secret_hash(username)
            if secret_hash:
                auth_params['SECRET_HASH'] = secret_hash
            
            print(f"Initiating auth for user: {username}")
            print(f"Auth params: USERNAME and PASSWORD set, SECRET_HASH: {'Present' if secret_hash else 'Not needed'}")
                
            response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters=auth_params
            )
            
            # Log successful authentication
            print(f"Authentication successful for {username}")
            print(f"Response type: {type(response)}")
            print(f"Response keys: {response.keys() if hasattr(response, 'keys') else 'Not a dict'}")
            
            return {
                'status': 'success',
                'message': 'Login successful',
                'data': response
            }
        except Exception as e:
            print(f"Authentication error for {username}: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }

    def forgot_password(self, username):
        """Initiate forgot password flow"""
        try:
            forgot_params = {
                'ClientId': self.client_id,
                'Username': username
            }
            
            
            secret_hash = self.get_secret_hash(username)
            if secret_hash:
                forgot_params['SecretHash'] = secret_hash
                
            response = self.client.forgot_password(**forgot_params)
            return {
                'status': 'success',
                'message': 'Password reset code sent to your email',
                'data': response
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def confirm_forgot_password(self, username, confirmation_code, new_password):
        """Complete forgot password flow with verification code"""
        try:
            confirm_params = {
                'ClientId': self.client_id,
                'Username': username,
                'ConfirmationCode': confirmation_code,
                'Password': new_password
            }
            
            
            secret_hash = self.get_secret_hash(username)
            if secret_hash:
                confirm_params['SecretHash'] = secret_hash
                
            response = self.client.confirm_forgot_password(**confirm_params)
            return {
                'status': 'success',
                'message': 'Password has been reset successfully',
                'data': response
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
