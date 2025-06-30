#!/usr/bin/env python3
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
        print("\n🎉 Setup complete! You can now run the application.")
        print("Use the Start_NotebookLM_Clone script for your platform.")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
    
    input("\nPress Enter to exit...")
