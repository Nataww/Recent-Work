import boto3
import uuid
from app.config import Config
import logging
import os
import mimetypes

# Setup logging
logger = logging.getLogger(__name__)

class S3Service:
    def __init__(self):
        try:
            # Prepare credentials for S3 client
            client_kwargs = {
                'service_name': 's3',
                'region_name': Config.AWS_REGION,
                'aws_access_key_id': Config.AWS_ACCESS_KEY_ID,
                'aws_secret_access_key': Config.AWS_SECRET_ACCESS_KEY
            }
            
            # Add session token if available
            if Config.AWS_SESSION_TOKEN:
                client_kwargs['aws_session_token'] = Config.AWS_SESSION_TOKEN
                logger.info("Using temporary credentials with session token")
            
            # Initialize S3 client with credentials
            self.s3 = boto3.client(**client_kwargs)
            self.bucket_name = Config.S3_BUCKET_NAME
            
            logger.info(f"S3 Service initialized with bucket: {self.bucket_name}")
            logger.info(f"Using AWS region: {Config.AWS_REGION}")
            if Config.AWS_ACCESS_KEY_ID:
                masked_key = f"{Config.AWS_ACCESS_KEY_ID[:4]}...{Config.AWS_ACCESS_KEY_ID[-4:]}"
                logger.info(f"Using access key ID: {masked_key}")
            else:
                logger.warning("No AWS access key provided")
        except Exception as e:
            logger.error(f"Error initializing S3 service: {str(e)}")
            raise

    def upload_file(self, file, username, folder=None, storage_class='STANDARD'):
        """Upload a file to S3 bucket with STANDARD storage class only."""
        try:
            # Ensure the storage class is always STANDARD
            storage_class = 'STANDARD'

            # Build the key for the file
            folder_prefix = f"users/{username}/"
            if folder and folder != 'root':
                folder_prefix += f"{folder}/"

            file_key = f"{folder_prefix}{file.filename}"

            # Upload the file with the STANDARD storage class
            self.s3.upload_fileobj(
                file,
                self.bucket_name,
                file_key,
                ExtraArgs={
                    "StorageClass": storage_class
                }
            )

            return {
                'status': 'success',
                'message': 'File uploaded successfully',
                'data': {
                    'key': file_key,
                    'storage_class': storage_class
                }
            }
        except Exception as e:
            logger.error(f"Error uploading file: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }

    def list_files(self, username):
        """List all files for a user with enhanced metadata"""
        try:
            response = self.s3.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=f"users/{username}/"
            )
            
            files = []
            folders = set()
            
            if 'Contents' in response:
                for item in response['Contents']:
                    file_key = item['Key']
                    
                    
                    if file_key.endswith('/'):
                        
                        folder_parts = file_key.split('/')
                        if len(folder_parts) > 2:
                            folder_name = folder_parts[-2]  # Get the folder name
                            folders.add(folder_name)
                        continue
                    
                    # Skip the users/{username}/ prefix itself
                    if file_key == f"users/{username}/" or file_key == f"users/{username}":
                        continue
                    
                    try:
                        # Get detailed object info including storage class
                        head_response = self.s3.head_object(Bucket=self.bucket_name, Key=file_key)
                        storage_class = head_response.get('StorageClass', 'STANDARD')
                    except Exception as e:
                        logger.warning(f"Error getting head for object {file_key}: {str(e)}")
                        storage_class = 'STANDARD'
                    
                    # Generate file URL
                    file_url = f"https://{self.bucket_name}.s3.{Config.AWS_REGION}.amazonaws.com/{file_key}"
                    
                    # Extract filename from key
                    path_parts = file_key.split('/')
                    raw_filename = path_parts[-1]
                    
                    # Extract the original filename by removing the UUID prefix
                    # Pattern: uuid_originalfilename.ext
                    if '_' in raw_filename:
                        # Display filename
                        display_filename = raw_filename.split('_', 1)[1]
                    else:
                        display_filename = raw_filename
                    
                    # Determine folder structure
                    if len(path_parts) > 3:  # users/username/folder/filename
                        folder = path_parts[2]
                        folders.add(folder)
                    else:
                        folder = 'root'
                    
                    # Get file type and appropriate icon
                    file_extension = os.path.splitext(display_filename)[1].lower()
                    file_type, icon_class = self._get_file_type_and_icon(file_extension)
                    
                    files.append({
                        'key': file_key,
                        'filename': display_filename,  # Use the display filename
                        'raw_filename': raw_filename,  # Keep the raw filename for reference if needed
                        'url': file_url,
                        'size': item['Size'],
                        'last_modified': item['LastModified'],
                        'storage_class': storage_class,
                        'type': file_type,
                        'icon_class': icon_class,
                        'folder': folder
                    })
            
            # Prepare folder structure for the UI
            folder_list = [{'name': folder, 'count': sum(1 for file in files if file['folder'] == folder)} 
                        for folder in folders]
            
            # Add the root folder if it has files
            root_files_count = sum(1 for file in files if file['folder'] == 'root')
            if root_files_count > 0 and 'root' not in [f['name'] for f in folder_list]:
                folder_list.append({'name': 'root', 'count': root_files_count})
            
            # Sort folders alphabetically
            folder_list.sort(key=lambda x: x['name'])
            
            # Return in the new format with both files and folders
            return {
                'status': 'success',
                'message': 'Files retrieved successfully',
                'data': {
                    'files': files,
                    'folders': folder_list
                }
            }
        except Exception as e:
            logger.error(f"Error listing files: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }

    def delete_file(self, file_key):
        """Delete a file from S3 bucket"""
        try:
            self.s3.delete_object(
                Bucket=self.bucket_name,
                Key=file_key
            )
            
            return {
                'status': 'success',
                'message': 'File deleted successfully'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def generate_presigned_url(self, file_key, expiration=3600):
        """Generate a presigned URL for temporary access"""
        try:
            url = self.s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': file_key
                },
                ExpiresIn=expiration
            )
            
            return {
                'status': 'success',
                'message': 'Presigned URL generated successfully',
                'data': {
                    'url': url,
                    'expires_in': expiration
                }
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def create_folder(self, username, folder_name):
        """Create a new folder in the user's S3 space"""
        try:
            # S3 doesn't have actual folders, so we create an empty object with a trailing slash
            folder_key = f"users/{username}/{folder_name}/"
            
            self.s3.put_object(
                Bucket=self.bucket_name,
                Key=folder_key,
                Body=''
            )
            
            return {
                'status': 'success',
                'message': 'Folder created successfully',
                'data': {
                    'folder_name': folder_name,
                    'folder_key': folder_key
                }
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def change_storage_class(self, file_key, storage_class):
        """Change the storage class of an existing object"""
        try:
            # Copy the object to itself with the new storage class
            self.s3.copy_object(
                Bucket=self.bucket_name,
                CopySource={
                    'Bucket': self.bucket_name,
                    'Key': file_key
                },
                Key=file_key,
                StorageClass=storage_class
            )
            
            return {
                'status': 'success',
                'message': 'Storage class changed successfully',
                'data': {
                    'file_key': file_key,
                    'storage_class': storage_class
                }
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _get_file_type_and_icon(self, extension):
        """Helper method to determine file type and appropriate icon class"""
        # Image files
        if extension in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp']:
            return 'IMAGE', 'fas fa-image file-icon-image'
        # Document files
        elif extension in ['.pdf']:
            return 'PDF', 'fas fa-file-pdf file-icon-pdf'
        elif extension in ['.doc', '.docx', '.txt', '.rtf']:
            return 'DOCUMENT', 'fas fa-file-word file-icon-doc'
        elif extension in ['.xls', '.xlsx', '.csv']:
            return 'SPREADSHEET', 'fas fa-file-excel file-icon-excel'
        elif extension in ['.ppt', '.pptx']:
            return 'PRESENTATION', 'fas fa-file-powerpoint file-icon-ppt'
        # Media files
        elif extension in ['.mp3', '.wav', '.ogg', '.flac']:
            return 'AUDIO', 'fas fa-file-audio file-icon-audio'
        elif extension in ['.mp4', '.webm', '.avi', '.mov']:
            return 'VIDEO', 'fas fa-file-video file-icon-video'
        # Archive files
        elif extension in ['.zip', '.rar', '.7z', '.tar', '.gz']:
            return 'ARCHIVE', 'fas fa-file-archive file-icon-archive'
        # Code files
        elif extension in ['.html', '.css', '.js', '.py', '.java', '.php', '.rb', '.c', '.cpp', '.h', '.cs', '.go']:
            return 'CODE', 'fas fa-file-code file-icon-code'
        # Default
        else:
            return 'OTHER', 'fas fa-file file-icon-other'