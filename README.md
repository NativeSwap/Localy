# 🚀 Localy - Local Network File Sharing App

A beautiful, modern web application for sharing files across your local network. Upload files from any device and download them from any other device on the same network.

## ✨ Features

### Core Features

- 🌐 **Local Network Access** - Access from any device on your network
- 🔐 **Password Protection** - Simple password authentication with 15-minute sessions
- 📁 **Auto File Organization** - Files automatically sorted by type with smart categorization
- 👀 **File Preview** - Preview images, videos, audio, PDFs, and text files in custom modal viewer
- 📱 **Device Detection** - Shows which device uploaded each file (Windows PC, Android Phone, iPhone, etc.)
- 💾 **Storage Info** - Real-time disk usage statistics
- 🎨 **Modern UI** - Beautiful, responsive design with Bootstrap 5 and gradient backgrounds

### Upload Features

- ⬆️ **Drag & Drop Upload** - Easy file uploads with intuitive drag and drop interface
- 📂 **Multi-File Upload** - Select and upload multiple files at once
- 🏷️ **File Name Display** - Shows selected files with truncated names and tooltips
- ⚡ **Real-time Progress** - Upload progress indication

### File Management

- 🗑️ **Bulk Operations** - Select multiple files for batch deletion
- ☑️ **Smart Selection** - Individual checkboxes with Select All/Deselect All controls
- 🔍 **Enhanced Grid View** - 4-column responsive layout with optimized spacing
- 📄 **File Metadata** - Track upload timestamps and device information
- 🔄 **Scroll Preservation** - Maintains scroll position across page refreshes
- ⚠️ **Conflict Handling** - Automatic renaming for duplicate filenames

### User Experience

- 📱 **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- 💬 **Custom Modals** - Purpose-built modal system for better interaction
- 🎯 **Improved Usability** - Larger checkboxes (18px) and better click targets
- 📏 **Text Truncation** - Smart text truncation with tooltips throughout the UI

## 📋 Requirements

- Python 3.7 or higher
- Write access to `/mnt/0E527A38527A249D/Localy/` (configurable)

## 🚀 Quick Start

### Option 1: Virtual Environment (Recommended)

1. **Create and Activate Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/macOS
   # or
   venv\Scripts\activate     # On Windows
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**

   ```bash
   python run.py
   ```

### Option 2: Direct Installation

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**

   ```bash
   python run.py
   ```

   or

   ```bash
   ./run.py
   ```

3. **Access the App**
   - Open your browser and go to: `http://[YOUR-IP]:7017`
   - Enter password: `1234`
   - Start uploading and sharing files!

## ⚙️ Configuration

All settings can be customized in `config.py`:

```python
# Authentication - CHANGE THIS PASSWORD IN PRODUCTION!
PASSWORD = "1234"                   # Default password

# File Upload Settings
MAX_FILE_SIZE_GB = 5               # Maximum file size in GB

# Storage Settings
UPLOAD_BASE_PATH = "/mnt/0E527A38527A249D/Localy"  # Change storage location
UPLOAD_FOLDER = f"{UPLOAD_BASE_PATH}/uploads"

# Server Settings
HOST = "0.0.0.0"                   # Listen on all interfaces
PORT = 7017                        # Server port

# Session Settings
SESSION_TIMEOUT_MINUTES = 15       # Auto-logout after 15 minutes of inactivity
```

## 📂 File Organization

Files are automatically organized into categories:

- **📷 Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`, `.svg`, `.ico`, `.tiff`
- **🎬 Videos**: `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv`, `.flv`, `.webm`, `.m4v`, `.3gp`
- **🎵 Audio**: `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.wma`, `.m4a`, `.opus`
- **📄 Documents**: `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt`, `.xls`, `.xlsx`, `.ppt`, `.pptx`
- **📦 Archives**: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2`, `.xz`
- **📁 Others**: Everything else

## 💡 Usage Guide

### Basic Operations

1. **Login**: Enter password `1234` (configurable in config.py)
2. **Upload Files**:
   - Drag and drop files onto the upload area
   - Or click "Choose Files" to select from file browser
   - Support for multiple file selection
3. **View Files**: Files appear in organized grid layout by category
4. **Preview Files**: Click on file thumbnail to open preview modal
5. **Delete Files**:
   - Single file: Click trash icon and confirm
   - Multiple files: Use checkboxes to select, then bulk delete

### Advanced Features

- **Bulk Selection**: Use "Select All" / "Deselect All" for quick selection
- **File Preview**: Supports images, videos, audio, PDFs, and text files
- **Device Tracking**: See which device uploaded each file
- **Session Management**: Auto-logout after 15 minutes of inactivity

### Network Access

1. **Find Your IP Address**:

   ```bash
   ip addr show | grep inet
   ```

2. **Access from Mobile/Other Devices**:

   - Use your computer's IP address
   - Example: `http://192.168.1.100:7017`

3. **Firewall Configuration**:

   ```bash
   # Ubuntu/Debian
   sudo ufw allow 7017

   # CentOS/RHEL
   sudo firewall-cmd --permanent --add-port=7017/tcp
   sudo firewall-cmd --reload
   ```

## 🛠️ Technical Details

### Dependencies

- **Flask**: Web framework
- **Werkzeug**: WSGI utilities and file upload handling
- **Jinja2**: Template engine

### File Storage

- **Metadata**: Stored in JSON format alongside files
- **Organization**: Automatic categorization and directory structure
- **Conflict Resolution**: Automatic filename numbering for duplicates

### UI Components

- **Bootstrap 5**: CSS framework for responsive design
- **Custom Modals**: Purpose-built modal system replacing Bootstrap modals
- **JavaScript**: Enhanced interactivity and AJAX operations

## 🛡️ Security Notes

- ⚠️ **Local Network Only**: This app is designed for local network use
- 🔑 **Simple Authentication**: Password is stored in plain text in config.py
- 🚫 **No Internet Exposure**: Don't expose this server to the internet without additional security
- ⏰ **Session Management**: 15-minute timeout for security
- 📁 **File Access**: Only uploaded files are accessible through the web interface

## 🗂️ File Structure

```
Localy/
├── app.py                    # Main Flask application
├── config.py                 # Configuration settings
├── run.py                    # Startup script
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation
├── venv/                     # Virtual environment (if used)
├── templates/                # HTML templates
│   ├── base.html             # Base template with navigation
│   ├── login.html            # Authentication page
│   └── files.html            # Main file management interface
├── static/                   # Static assets (if any)
└── /mnt/0E527A38527A249D/Localy/uploads/  # File storage
    ├── images/               # Image files
    ├── videos/               # Video files
    ├── audio/                # Audio files
    ├── documents/            # Document files
    ├── archives/             # Archive files
    ├── others/               # Other file types
    └── .metadata/            # JSON metadata files
```

## 🐛 Troubleshooting

### Common Issues

**Permission Denied Error**:

```bash
sudo chown -R $USER:$USER /mnt/0E527A38527A249D/Localy
sudo chmod -R 755 /mnt/0E527A38527A249D/Localy
```

**Port Already in Use**:

- Change `PORT = 7017` to another port in config.py
- Check for existing processes: `lsof -i :7017`

**Can't Access from Other Devices**:

- Check firewall settings: `sudo ufw status`
- Ensure all devices are on the same network
- Verify the server is binding to `0.0.0.0` not `127.0.0.1`

**File Upload Issues**:

- Check available disk space
- Verify file size is under the 5GB limit
- Check browser console for JavaScript errors

**Modal/UI Issues**:

- Clear browser cache
- Disable browser extensions that might interfere
- Try a different browser

### Running in Background

**Using nohup**:

```bash
nohup python run.py > server.log 2>&1 &
```

**Using systemd (Linux)**:

```bash
# Create service file
sudo nano /etc/systemd/system/localy.service

# Add service configuration
[Unit]
Description=Localy File Sharing
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/home/sourov/NodeProject/Localy
ExecStart=/home/sourov/NodeProject/Localy/venv/bin/python run.py
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl enable localy
sudo systemctl start localy
```

## 🔄 Updates and Changelog

### Recent Improvements

- ✅ **Custom Modal System**: Replaced Bootstrap modals with custom implementation
- ✅ **Enhanced Bulk Operations**: Improved checkbox selection and bulk delete
- ✅ **Better Grid Layout**: Optimized to 4-column layout for better spacing
- ✅ **Text Truncation**: Added tooltips for long file names
- ✅ **Session Management**: 15-minute auto-logout functionality
- ✅ **Device Detection**: Enhanced device identification system
- ✅ **Scroll Preservation**: Maintains scroll position across page refreshes
- ✅ **Conflict Resolution**: Automatic handling of duplicate filenames

## 📞 Support

If you encounter any issues:

1. Check the console output for error messages
2. Verify file permissions on the upload directory
3. Ensure the port is not blocked by firewall
4. Check the `server.log` file if running in background

---

🎉 **Enjoy seamless file sharing across your local network with Localy!**
