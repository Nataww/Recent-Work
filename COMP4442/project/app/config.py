import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    AWS_REGION = os.environ.get('AWS_REGION')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_SESSION_TOKEN = os.environ.get('AWS_SESSION_TOKEN')
    COGNITO_USER_POOL_ID = os.environ.get('COGNITO_USER_POOL_ID')
    COGNITO_APP_CLIENT_ID = os.environ.get('COGNITO_APP_CLIENT_ID')
    COGNITO_APP_CLIENT_SECRET = os.environ.get('COGNITO_APP_CLIENT_SECRET')
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    
    # File upload settings
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20MB
    UPLOAD_FOLDER = '/tmp'  
