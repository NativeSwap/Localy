# Configuration file for Local File Sharing App

# Authentication - CHANGE THIS PASSWORD IN PRODUCTION!
PASSWORD = "1234"

# File Upload Settings
MAX_FILE_SIZE_GB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_GB * 1024 * 1024 * 1024  # Convert to bytes

# Storage Settings
UPLOAD_BASE_PATH = "/mnt/0E527A38527A249D/Localy"
UPLOAD_FOLDER = f"{UPLOAD_BASE_PATH}/uploads"

# Server Settings
HOST = "0.0.0.0"
PORT = 7017
DEBUG = False

# Security Settings
SESSION_TIMEOUT_MINUTES = 15
MAX_LOGIN_ATTEMPTS = 5

# File Categories
FILE_CATEGORIES = {
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff'],
    'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp'],
    'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
    'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx', '.csv'],
    'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
    'others': []  # Everything else goes here
}

# Preview Settings
PREVIEWABLE_IMAGES = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']
PREVIEWABLE_VIDEOS = ['.mp4', '.webm', '.ogg']
PREVIEWABLE_AUDIO = ['.mp3', '.wav', '.ogg', '.m4a']
PREVIEWABLE_DOCUMENTS = ['.pdf', '.txt'] 