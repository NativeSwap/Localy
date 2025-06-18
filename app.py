
import shutil
import json
from datetime import datetime, timedelta
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify, session, abort
from werkzeug.utils import secure_filename
import config
import secrets

app = Flask(__name__)
# Generate a secure secret key
app.secret_key = secrets.token_hex(32)
app.config['MAX_CONTENT_LENGTH'] = config.MAX_FILE_SIZE_BYTES
app.config['PERMANENT_SESSION_LIFETIME'] = 900  # 15 minutes in seconds

# Security and cache headers
@app.after_request
def add_headers(response):
    # Security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data:;"
    
    # Cache headers for static assets
    if request.endpoint == 'static':
        # Cache static files for 1 year
        response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
        response.headers['Expires'] = (datetime.now() + timedelta(days=365)).strftime('%a, %d %b %Y %H:%M:%S GMT')
    elif request.endpoint in ['download_file', 'preview_file']:
        # Cache downloaded/preview files for 1 hour (since they might be updated)
        response.headers['Cache-Control'] = 'public, max-age=3600'
        response.headers['Expires'] = (datetime.now() + timedelta(hours=1)).strftime('%a, %d %b %Y %H:%M:%S GMT')
    else:
        # Don't cache dynamic pages
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    
    return response

def validate_session():
    """Validate user session and check timeout"""
    if not session.get('authenticated'):
        return False
    
    # Check session timeout
    last_activity = session.get('last_activity')
    if last_activity:
        last_activity = datetime.fromisoformat(last_activity)
        if datetime.now() - last_activity > timedelta(seconds=900):  # 15 minutes
            session.clear()
            return False
    
    # Update last activity
    session['last_activity'] = datetime.now().isoformat()
    return True

def validate_filename(filename):
    """Validate filename for security"""
    if not filename or len(filename) > 255:
        return False
    
    # Check for path traversal attempts
    if '..' in filename or '/' in filename or '\\' in filename:
        return False
    
    # Check for invalid characters
    invalid_chars = '<>:"|?*\x00'
    if any(char in filename for char in invalid_chars):
        return False
    
    return True

def validate_category(category):
    """Validate category parameter"""
    if not category:
        return False
    
    # Only allow known categories
    valid_categories = list(config.FILE_CATEGORIES.keys())
    return category in valid_categories

def safe_path_join(base_path, *paths):
    """Safely join paths and prevent directory traversal"""
    full_path = Path(base_path)
    for path in paths:
        if not path or '..' in path or '/' in str(path) or '\\' in str(path):
            raise ValueError("Invalid path component")
        full_path = full_path / path
    
    # Ensure the final path is within the base directory
    try:
        full_path.resolve().relative_to(Path(base_path).resolve())
    except ValueError:
        raise ValueError("Path traversal attempt detected")
    
    return full_path

def create_upload_directories():
    """Create upload directories if they don't exist"""
    base_path = Path(config.UPLOAD_FOLDER)
    base_path.mkdir(parents=True, exist_ok=True)
    
    for category in config.FILE_CATEGORIES.keys():
        category_path = base_path / category
        category_path.mkdir(exist_ok=True)

def get_metadata_file_path():
    """Get the path to the file metadata JSON file"""
    return Path(config.UPLOAD_FOLDER) / "file_metadata.json"

def load_file_metadata():
    """Load file metadata from JSON file"""
    metadata_file = get_metadata_file_path()
    if metadata_file.exists():
        try:
            with open(metadata_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_file_metadata(metadata):
    """Save file metadata to JSON file"""
    metadata_file = get_metadata_file_path()
    try:
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    except IOError as e:
        print(f"Error saving metadata: {e}")

def add_file_metadata(filename, category, device_info):
    """Add metadata for a new file"""
    if not validate_filename(filename) or not validate_category(category):
        return
    
    metadata = load_file_metadata()
    file_key = f"{category}/{filename}"
    metadata[file_key] = {
        'uploaded_at': datetime.now().isoformat(),
        'device': device_info,
        'category': category,
        'filename': filename
    }
    save_file_metadata(metadata)

def remove_file_metadata(filename, category):
    """Remove metadata for a deleted file"""
    if not validate_filename(filename) or not validate_category(category):
        return
    
    metadata = load_file_metadata()
    file_key = f"{category}/{filename}"
    if file_key in metadata:
        del metadata[file_key]
        save_file_metadata(metadata)

def get_file_metadata(filename, category):
    """Get metadata for a specific file"""
    if not validate_filename(filename) or not validate_category(category):
        return {}
    
    metadata = load_file_metadata()
    file_key = f"{category}/{filename}"
    return metadata.get(file_key, {})

def get_file_category(filename):
    """Determine which category a file belongs to based on its extension"""
    if not validate_filename(filename):
        return None
    
    file_ext = Path(filename).suffix.lower()
    
    for category, extensions in config.FILE_CATEGORIES.items():
        if category != 'others' and file_ext in extensions:
            return category
    return 'others'

def get_file_info(filepath):
    """Get file information including size, date, etc."""
    try:
        stat = filepath.stat()
        category = get_file_category(filepath.name)
        if not category:
            return None
        
        metadata = get_file_metadata(filepath.name, category)
        
        return {
            'name': filepath.name,
            'size': stat.st_size,
            'size_readable': format_file_size(stat.st_size),
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'category': category,
            'extension': filepath.suffix.lower(),
            'is_previewable': is_file_previewable(filepath.name),
            'device': metadata.get('device', 'Unknown'),
            'uploaded_at': metadata.get('uploaded_at', '')
        }
    except (OSError, ValueError):
        return None

def format_file_size(size_bytes):
    """Convert bytes to human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def is_file_previewable(filename):
    """Check if file can be previewed in browser"""
    if not validate_filename(filename):
        return False
    
    file_ext = Path(filename).suffix.lower()
    return (file_ext in config.PREVIEWABLE_IMAGES or 
            file_ext in config.PREVIEWABLE_VIDEOS or 
            file_ext in config.PREVIEWABLE_AUDIO or 
            file_ext in config.PREVIEWABLE_DOCUMENTS)

def get_client_info(request):
    """Extract client device information from request headers"""
    user_agent = request.headers.get('User-Agent', '')
    device_info = "Unknown Device"
    
    # Simple device detection based on User-Agent
    if 'iPhone' in user_agent:
        device_info = "iPhone"
    elif 'iPad' in user_agent:
        device_info = "iPad"
    elif 'Android' in user_agent:
        if 'Mobile' in user_agent:
            device_info = "Android Phone"
        else:
            device_info = "Android Tablet"
    elif 'Windows' in user_agent:
        device_info = "Windows PC"
    elif 'Macintosh' in user_agent:
        device_info = "Mac"
    elif 'Linux' in user_agent:
        device_info = "Linux PC"
    
    return device_info

@app.route('/')
def index():
    if not validate_session():
        return redirect(url_for('login'))
    return redirect(url_for('files'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password', '').strip()
        
        # Rate limiting check (simple in-memory, could use Redis for production)
        client_ip = request.environ.get('REMOTE_ADDR', 'unknown')
        login_attempts = session.get('login_attempts', 0)
        
        if login_attempts >= 5:
            flash('Too many failed attempts. Please try again later.', 'error')
            return render_template('login.html')
        
        if password == config.PASSWORD:
            session.clear()  # Clear any existing session data
            session['authenticated'] = True
            session['last_activity'] = datetime.now().isoformat()
            session.permanent = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('files'))
        else:
            session['login_attempts'] = login_attempts + 1
            flash('Invalid password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Successfully logged out!', 'success')
    return redirect(url_for('login'))

@app.route('/files')
@app.route('/files/<category>')
def files(category=None):
    if not validate_session():
        return redirect(url_for('login'))
    
    if category and not validate_category(category):
        abort(404)
    
    create_upload_directories()
    
    files_by_category = {}
    upload_path = Path(config.UPLOAD_FOLDER)
    
    # Get files from all categories or specific category
    categories_to_scan = [category] if category else config.FILE_CATEGORIES.keys()
    
    for cat in categories_to_scan:
        if not validate_category(cat):
            continue
            
        try:
            cat_path = safe_path_join(config.UPLOAD_FOLDER, cat)
            if cat_path.exists():
                files_in_category = []
                for file_path in cat_path.iterdir():
                    if file_path.is_file() and validate_filename(file_path.name):
                        file_info = get_file_info(file_path)
                        if file_info:
                            files_in_category.append(file_info)
                
                if files_in_category:
                    files_by_category[cat] = sorted(files_in_category, key=lambda x: x['modified'], reverse=True)
        except ValueError:
            continue  # Skip invalid paths
    
    return render_template('files.html', 
                         files_by_category=files_by_category,
                         current_category=category,
                         categories=config.FILE_CATEGORIES.keys(),
                         max_size_gb=config.MAX_FILE_SIZE_GB)

@app.route('/upload', methods=['POST'])
def upload_file():
    if not validate_session():
        return redirect(url_for('login'))
    
    if 'file' not in request.files:
        flash('No file selected!', 'error')
        return redirect(url_for('files'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected!', 'error')
        return redirect(url_for('files'))
    
    if file and file.filename:
        original_filename = file.filename
        filename = secure_filename(original_filename)
        
        # Additional validation
        if not validate_filename(filename):
            flash('Invalid filename!', 'error')
            return redirect(url_for('files'))
        
        category = get_file_category(filename)
        if not category:
            flash('Invalid file type!', 'error')
            return redirect(url_for('files'))
        
        try:
            # Create category directory if it doesn't exist
            category_path = safe_path_join(config.UPLOAD_FOLDER, category)
            category_path.mkdir(parents=True, exist_ok=True)
            
            # Handle filename conflicts
            file_path = category_path / filename
            counter = 1
            original_stem = file_path.stem
            original_suffix = file_path.suffix
            
            while file_path.exists():
                new_filename = f"{original_stem}_{counter}{original_suffix}"
                if not validate_filename(new_filename):
                    break
                file_path = category_path / new_filename
                counter += 1
                
                # Prevent infinite loop
                if counter > 9999:
                    flash('Too many files with similar names!', 'error')
                    return redirect(url_for('files'))
            
            file.save(file_path)
            device_info = get_client_info(request)
            add_file_metadata(file_path.name, category, device_info)
            flash(f'File "{file_path.name}" uploaded successfully from {device_info}!', 'success')
            
        except (ValueError, OSError) as e:
            flash(f'Error uploading file: Invalid path or permissions', 'error')
        except Exception as e:
            flash(f'Error uploading file: {str(e)}', 'error')
    
    return redirect(url_for('files'))

@app.route('/download/<category>/<filename>')
def download_file(category, filename):
    if not validate_session():
        return redirect(url_for('login'))
    
    if not validate_category(category) or not validate_filename(filename):
        abort(404)
    
    try:
        file_path = safe_path_join(config.UPLOAD_FOLDER, category, filename)
        
        if file_path.exists() and file_path.is_file():
            return send_file(file_path, as_attachment=True)
        else:
            abort(404)
    except ValueError:
        abort(404)

@app.route('/preview/<category>/<filename>')
def preview_file(category, filename):
    if not validate_session():
        return redirect(url_for('login'))
    
    if not validate_category(category) or not validate_filename(filename):
        abort(404)
    
    try:
        file_path = safe_path_join(config.UPLOAD_FOLDER, category, filename)
        
        if file_path.exists() and file_path.is_file() and is_file_previewable(filename):
            return send_file(file_path)
        else:
            abort(404)
    except ValueError:
        abort(404)

@app.route('/delete/<category>/<filename>', methods=['POST'])
def delete_file(category, filename):
    if not validate_session():
        return redirect(url_for('login'))
    
    if not validate_category(category) or not validate_filename(filename):
        abort(404)
    
    try:
        file_path = safe_path_join(config.UPLOAD_FOLDER, category, filename)
        
        if file_path.exists() and file_path.is_file():
            file_path.unlink()
            remove_file_metadata(filename, category)
            flash(f'File "{filename}" deleted successfully!', 'success')
        else:
            flash('File not found!', 'error')
    except ValueError:
        flash('Invalid file path!', 'error')
    except Exception as e:
        flash(f'Error deleting file: {str(e)}', 'error')
    
    return redirect(url_for('files'))

@app.route('/api/storage-info')
def storage_info():
    """Get storage information"""
    if not validate_session():
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        upload_path = Path(config.UPLOAD_FOLDER)
        total_size = 0
        file_count = 0
        
        if upload_path.exists():
            for file_path in upload_path.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
                    file_count += 1
        
        # Get disk usage of the mount point
        disk_usage = shutil.disk_usage(config.UPLOAD_BASE_PATH)
        
        return jsonify({
            'total_files': file_count,
            'total_size': total_size,
            'total_size_readable': format_file_size(total_size),
            'disk_total': disk_usage.total,
            'disk_used': disk_usage.used,
            'disk_free': disk_usage.free,
            'disk_total_readable': format_file_size(disk_usage.total),
            'disk_used_readable': format_file_size(disk_usage.used),
            'disk_free_readable': format_file_size(disk_usage.free)
        })
    except Exception as e:
        return jsonify({'error': 'Storage information unavailable'}), 500

if __name__ == '__main__':
    create_upload_directories()
    print(f"Starting Local File Sharing Server...")
    print(f"Access URL: http://{config.HOST}:{config.PORT}")
    print(f"Upload directory: {config.UPLOAD_FOLDER}")
    print(f"Password: {config.PASSWORD}")
    print(f"Max file size: {config.MAX_FILE_SIZE_GB} GB")
    
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG) 