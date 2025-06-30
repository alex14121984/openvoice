#!/usr/bin/env python3
"""
Setup script for creating a standalone NotebookLM Clone application
"""

import os
import sys
import shutil
import subprocess
import urllib.request
import zipfile
from pathlib import Path

def download_models():
    """Download OpenVoice models if not present"""
    print("📥 Downloading OpenVoice models...")
    
    models_url = "https://myshell-public-repo-hosting.s3.amazonaws.com/openvoice/checkpoints_v1_0509.zip"
    models_zip = "checkpoints_v1_0509.zip"
    
    if not os.path.exists("openvoice/checkpoints"):
        os.makedirs("openvoice/checkpoints", exist_ok=True)
        
        # Download models
        print(f"Downloading from {models_url}...")
        urllib.request.urlretrieve(models_url, models_zip)
        
        # Extract models
        print("Extracting models...")
        with zipfile.ZipFile(models_zip, 'r') as zip_ref:
            zip_ref.extractall("openvoice/")
        
        # Clean up
        os.remove(models_zip)
        print("✅ Models downloaded and extracted")
    else:
        print("✅ Models already present")

def create_portable_package():
    """Create a portable package with all dependencies"""
    print("📦 Creating portable package...")
    
    # Create package directory
    package_dir = Path("NotebookLM_Clone_Portable")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    
    package_dir.mkdir()
    
    # Copy application files
    app_dir = package_dir / "app"
    app_dir.mkdir()
    
    # Copy notebooklm_app
    shutil.copytree("notebooklm_app", app_dir / "notebooklm_app")
    
    # Copy OpenVoice models (if they exist)
    if Path("openvoice/checkpoints").exists():
        shutil.copytree("openvoice", app_dir / "openvoice")
    
    # Copy documentation
    shutil.copy("PROJECT_SUMMARY.md", package_dir / "README.md")
    
    # Create simple batch/shell scripts for different platforms
    create_launch_scripts(package_dir)
    
    # Create requirements and setup info
    create_setup_files(package_dir)
    
    print(f"✅ Portable package created in: {package_dir}")
    return package_dir

def create_launch_scripts(package_dir):
    """Create launch scripts for different platforms"""
    
    # Windows batch file
    windows_script = package_dir / "Start_NotebookLM_Clone.bat"
    windows_script.write_text("""@echo off
echo Starting NotebookLM Clone...
cd app\\notebooklm_app
python launcher.py
pause
""")
    
    # Linux/Mac shell script
    unix_script = package_dir / "Start_NotebookLM_Clone.sh"
    unix_script.write_text("""#!/bin/bash
echo "Starting NotebookLM Clone..."
cd app/notebooklm_app
python3 launcher.py
""")
    
    # Make shell script executable
    os.chmod(unix_script, 0o755)
    
    print("✅ Launch scripts created")

def create_setup_files(package_dir):
    """Create setup and instruction files"""
    
    # Create simple setup instructions
    setup_instructions = package_dir / "SETUP_INSTRUCTIONS.txt"
    setup_instructions.write_text("""
NotebookLM Clone - Setup Instructions
====================================

QUICK START:
1. Make sure Python 3.8+ is installed on your system
2. Double-click the appropriate launcher for your system:
   - Windows: Start_NotebookLM_Clone.bat
   - Linux/Mac: Start_NotebookLM_Clone.sh

FIRST TIME SETUP:
1. Install Python dependencies:
   - Open terminal/command prompt in the app/notebooklm_app folder
   - Run: pip install -r requirements.txt

2. Install system dependencies (Linux/Mac):
   - sudo apt install ffmpeg (Ubuntu/Debian)
   - brew install ffmpeg (Mac with Homebrew)

3. For Windows users:
   - Download ffmpeg from https://ffmpeg.org/download.html
   - Add ffmpeg to your system PATH

USAGE:
- The application will start a web server on http://localhost:12000
- Your browser should open automatically
- Upload documents, paste URLs, or enter text to generate audio overviews
- Generated audio files can be played in the browser or downloaded

TROUBLESHOOTING:
- If models are missing, download them from:
  https://myshell-public-repo-hosting.s3.amazonaws.com/openvoice/checkpoints_v1_0509.zip
- Extract to app/openvoice/checkpoints/
- Check app/notebooklm_app/app.log for error messages

For detailed documentation, see README.md
""")
    
    # Create a simple installer script
    installer_script = package_dir / "install_dependencies.py"
    installer_script.write_text("""#!/usr/bin/env python3
import subprocess
import sys
import os

def install_dependencies():
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "app/notebooklm_app/requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    return True

if __name__ == "__main__":
    print("NotebookLM Clone - Dependency Installer")
    print("=" * 40)
    
    if install_dependencies():
        print("\\n🎉 Setup complete! You can now run the application.")
        print("Use the Start_NotebookLM_Clone script for your platform.")
    else:
        print("\\n❌ Setup failed. Please check the error messages above.")
    
    input("\\nPress Enter to exit...")
""")

def create_executable():
    """Create standalone executable using PyInstaller"""
    print("🔨 Creating standalone executable...")
    
    try:
        # Create PyInstaller spec file
        spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['notebooklm_app/launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('notebooklm_app/templates', 'templates'),
        ('notebooklm_app/static', 'static'),
    ],
    hiddenimports=[
        'flask',
        'torch',
        'librosa',
        'faster_whisper',
        'beautifulsoup4',
        'requests',
        'PyPDF2',
        'python-docx',
        'numpy',
        'scipy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NotebookLM_Clone',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""
        
        with open("notebooklm_standalone.spec", "w") as f:
            f.write(spec_content)
        
        # Run PyInstaller
        subprocess.run([
            sys.executable, "-m", "PyInstaller", 
            "--clean", 
            "notebooklm_standalone.spec"
        ], check=True)
        
        print("✅ Executable created in dist/ folder")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating executable: {e}")
        print("Creating portable package instead...")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🎵 NotebookLM Clone - Standalone Setup")
    print("=" * 50)
    
    # Download models
    download_models()
    
    # Try to create executable first
    executable_created = create_executable()
    
    # Always create portable package as backup
    package_dir = create_portable_package()
    
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    
    if executable_created:
        print("✅ Standalone executable created in dist/NotebookLM_Clone")
        print("   Just run the executable to start the application!")
    
    print(f"✅ Portable package created in: {package_dir}")
    print("   Follow the instructions in SETUP_INSTRUCTIONS.txt")
    
    print("\n📋 What you get:")
    print("- Complete web application with modern UI")
    print("- Support for URLs, PDFs, DOCX, and text input")
    print("- High-quality audio generation using OpenVoice")
    print("- No internet required after setup")
    print("- Cross-platform compatibility")

if __name__ == "__main__":
    main()