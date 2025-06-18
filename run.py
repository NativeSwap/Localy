#!/usr/bin/env python3
"""
Localy - Local File Sharing Web Application
Run this script to start the server.
"""

import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from app import app, create_upload_directories
    import config
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please make sure all dependencies are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)


def main():
    """Main function to start the application"""
    try:
        # Create upload directories
        create_upload_directories()
        
        print("=" * 60)
        print("🚀 LOCALY SERVER STARTING...")
        print("=" * 60)
        print(f"📂 Upload Directory: {config.UPLOAD_FOLDER}")
        print(f"🌐 Server URL: http://{config.HOST}:{config.PORT}")
        print(f"🔑 Password: {config.PASSWORD}")
        print(f"📦 Max File Size: {config.MAX_FILE_SIZE_GB} GB")
        print("=" * 60)
        print("💡 Access from any device on your local network!")
        print("💡 Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Start the Flask application
        app.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG,
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 