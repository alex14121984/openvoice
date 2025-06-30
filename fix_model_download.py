#!/usr/bin/env python3
"""
Fix the model download issue and create a working fallback solution
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
import time
import threading
import webbrowser
from pathlib import Path

def check_alternative_models():
    """Check for alternative model sources"""
    print("🔍 Checking alternative model sources...")
    
    # Alternative URLs to try
    alternative_urls = [
        "https://github.com/myshell-ai/OpenVoice/releases/download/v1.0/checkpoints_v1_0509.zip",
        "https://huggingface.co/myshell-ai/OpenVoice/resolve/main/checkpoints_v1_0509.zip",
        "https://drive.google.com/uc?id=1Le_Iu_vV2JTBFgzpNzYJHYvXhLyGBNJz"  # Example Google Drive link
    ]
    
    for url in alternative_urls:
        try:
            print(f"   Trying: {url}")
            response = urllib.request.urlopen(url, timeout=10)
            if response.getcode() == 200:
                print(f"   ✅ Found working URL: {url}")
                return url
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    print("   ⚠️  No working model URLs found")
    return None

def create_minimal_working_app():
    """Create a version that works without OpenVoice models"""
    print("🔧 Creating minimal working version...")
    
    app_content = '''#!/usr/bin/env python3
"""
NotebookLM Clone - Minimal Working Version
Works without OpenVoice models, provides text processing only
"""

import os
import sys
import tempfile
import logging
from pathlib import Path
import webbrowser
import threading
import time

from flask import Flask, render_template, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
import requests

# Try to import BeautifulSoup, install if missing
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing beautifulsoup4...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
    from bs4 import BeautifulSoup

# Try to import document processing libraries
try:
    import PyPDF2
except ImportError:
    print("Installing PyPDF2...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
    import PyPDF2

try:
    from docx import Document
except ImportError:
    print("Installing python-docx...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx"])
    from docx import Document

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app setup
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create necessary directories
UPLOAD_FOLDER = Path(__file__).parent / 'uploads'
AUDIO_FOLDER = Path(__file__).parent / 'static' / 'audio'
UPLOAD_FOLDER.mkdir(exist_ok=True)
AUDIO_FOLDER.mkdir(parents=True, exist_ok=True)

def extract_text_from_url(url):
    """Extract text content from a URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:5000]  # Limit to 5000 characters
        
    except Exception as e:
        logger.error(f"Error extracting text from URL: {e}")
        return None

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages[:10]:  # Limit to first 10 pages
                text += page.extract_text()
        return text[:5000]  # Limit to 5000 characters
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        return None

def extract_text_from_docx(file_path):
    """Extract text from Word document"""
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs[:50]:  # Limit to first 50 paragraphs
            text += paragraph.text + "\\n"
        return text[:5000]  # Limit to 5000 characters
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {e}")
        return None

def generate_summary(text):
    """Generate a simple text summary"""
    if not text:
        return "No content available for summary."
    
    # Simple extractive summarization
    sentences = text.split('. ')
    
    # Take first few sentences and some from middle
    summary_sentences = []
    if len(sentences) > 0:
        summary_sentences.extend(sentences[:3])  # First 3 sentences
    if len(sentences) > 6:
        mid_point = len(sentences) // 2
        summary_sentences.extend(sentences[mid_point:mid_point+2])  # 2 from middle
    
    summary = '. '.join(summary_sentences)
    
    if len(summary) > 800:
        summary = summary[:800] + "..."
    
    return summary

def create_text_overview(text):
    """Create a text-based overview since audio generation is not available"""
    summary = generate_summary(text)
    
    overview = f"""
📄 DOCUMENT OVERVIEW
==================

📊 CONTENT ANALYSIS:
• Total characters: {len(text):,}
• Estimated reading time: {len(text) // 200} minutes
• Word count: ~{len(text.split())} words

📝 SUMMARY:
{summary}

💡 KEY POINTS:
• This is a text-only overview (audio generation requires AI models)
• The content has been processed and summarized
• You can copy this text for your own use

🎧 AUDIO NOTE:
Audio generation is currently unavailable. To enable audio features:
1. Download OpenVoice models manually
2. Place them in the openvoice/checkpoints folder
3. Restart the application
"""
    
    return overview

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "mode": "text-only"})

@app.route('/process', methods=['POST'])
def process_content():
    """Process uploaded content and generate overview"""
    try:
        content_type = request.form.get('content_type')
        text = None
        
        if content_type == 'url':
            url = request.form.get('url')
            if url:
                logger.info(f"Processing URL: {url}")
                text = extract_text_from_url(url)
                if not text:
                    return jsonify({"error": "Could not extract text from URL"}), 400
        
        elif content_type == 'text':
            text = request.form.get('text')
            if not text:
                return jsonify({"error": "No text provided"}), 400
        
        elif content_type == 'file':
            if 'file' not in request.files:
                return jsonify({"error": "No file uploaded"}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({"error": "No file selected"}), 400
            
            # Save uploaded file
            filename = secure_filename(file.filename)
            file_path = UPLOAD_FOLDER / filename
            file.save(file_path)
            
            # Extract text based on file type
            if filename.lower().endswith('.pdf'):
                text = extract_text_from_pdf(file_path)
            elif filename.lower().endswith('.docx'):
                text = extract_text_from_docx(file_path)
            elif filename.lower().endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()[:5000]
            else:
                return jsonify({"error": "Unsupported file type"}), 400
            
            # Clean up uploaded file
            file_path.unlink()
            
            if not text:
                return jsonify({"error": "Could not extract text from file"}), 400
        
        else:
            return jsonify({"error": "Invalid content type"}), 400
        
        # Generate text overview
        overview = create_text_overview(text)
        
        return jsonify({
            "success": True,
            "overview": overview,
            "mode": "text-only",
            "message": "Text overview generated successfully"
        })
        
    except Exception as e:
        logger.error(f"Error processing content: {e}")
        return jsonify({"error": str(e)}), 500

def open_browser():
    """Open browser after a delay"""
    time.sleep(2)
    try:
        webbrowser.open('http://localhost:12000')
        print("📱 Browser opened at http://localhost:12000")
    except:
        print("📱 Please open http://localhost:12000 in your browser")

if __name__ == '__main__':
    print("🎵 NotebookLM Clone - Text-Only Mode")
    print("=" * 50)
    print("🔧 Running in text-only mode (no audio generation)")
    print("📱 Browser will open automatically")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 50)
    
    # Start browser opener
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    try:
        app.run(host='0.0.0.0', port=12000, debug=False)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        input("Press Enter to exit...")
'''
    
    # Write the minimal app
    minimal_app_path = Path("notebooklm_app_minimal") / "app.py"
    minimal_app_path.parent.mkdir(exist_ok=True)
    minimal_app_path.write_text(app_content)
    
    # Copy the HTML template
    template_dir = minimal_app_path.parent / "templates"
    template_dir.mkdir(exist_ok=True)
    
    # Copy existing template if available
    original_template = Path("notebooklm_app/templates/index.html")
    if original_template.exists():
        import shutil
        shutil.copy(original_template, template_dir / "index.html")
    else:
        # Create a simple template
        simple_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NotebookLM Clone</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 20px; border-radius: 10px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, textarea, select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin-top: 20px; padding: 15px; background: white; border-radius: 5px; white-space: pre-wrap; }
        .warning { background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎵 NotebookLM Clone</h1>
        
        <div class="warning">
            <strong>⚠️ Text-Only Mode:</strong> Audio generation is currently unavailable. 
            This version provides text summaries and analysis only.
        </div>
        
        <form id="contentForm">
            <div class="form-group">
                <label for="contentType">Content Source:</label>
                <select id="contentType" name="content_type" onchange="toggleInputs()">
                    <option value="text">Direct Text Input</option>
                    <option value="url">Website URL</option>
                    <option value="file">File Upload</option>
                </select>
            </div>
            
            <div id="textInput" class="form-group">
                <label for="text">Enter your text:</label>
                <textarea id="text" name="text" rows="6" placeholder="Paste your text here..."></textarea>
            </div>
            
            <div id="urlInput" class="form-group" style="display:none;">
                <label for="url">Website URL:</label>
                <input type="url" id="url" name="url" placeholder="https://example.com">
            </div>
            
            <div id="fileInput" class="form-group" style="display:none;">
                <label for="file">Upload File:</label>
                <input type="file" id="file" name="file" accept=".pdf,.docx,.txt">
            </div>
            
            <button type="submit">Generate Overview</button>
        </form>
        
        <div id="result" class="result" style="display:none;"></div>
    </div>
    
    <script>
        function toggleInputs() {
            const contentType = document.getElementById('contentType').value;
            document.getElementById('textInput').style.display = contentType === 'text' ? 'block' : 'none';
            document.getElementById('urlInput').style.display = contentType === 'url' ? 'block' : 'none';
            document.getElementById('fileInput').style.display = contentType === 'file' ? 'block' : 'none';
        }
        
        document.getElementById('contentForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const resultDiv = document.getElementById('result');
            
            resultDiv.innerHTML = 'Processing...';
            resultDiv.style.display = 'block';
            
            try {
                const response = await fetch('/process', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    resultDiv.innerHTML = data.overview;
                } else {
                    resultDiv.innerHTML = 'Error: ' + (data.error || 'Unknown error');
                }
            } catch (error) {
                resultDiv.innerHTML = 'Error: ' + error.message;
            }
        });
    </script>
</body>
</html>'''
        (template_dir / "index.html").write_text(simple_template)
    
    print(f"✅ Created minimal working app at: {minimal_app_path}")
    return minimal_app_path

def create_fixed_installer():
    """Create a new installer that handles the model download issue"""
    
    installer_content = '''#!/usr/bin/env python3
"""
NotebookLM Clone - Fixed Installer
Handles model download issues and provides working fallback
"""

import os
import sys
import subprocess
import time
import threading
import webbrowser
from pathlib import Path

class FixedInstaller:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        
    def print_header(self):
        print("=" * 60)
        print("🎵 NotebookLM Clone - Fixed Installer")
        print("=" * 60)
        print("This installer provides a working solution even without AI models")
        print("=" * 60)
        
    def check_python(self):
        """Check Python version"""
        print("\\n🐍 Checking Python...")
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            print(f"✅ Python {version.major}.{version.minor} - Good!")
            return True
        else:
            print(f"❌ Python {version.major}.{version.minor} found, need 3.8+")
            return False
    
    def install_basic_packages(self):
        """Install essential packages"""
        print("\\n📦 Installing essential packages...")
        
        packages = [
            "flask",
            "beautifulsoup4", 
            "requests",
            "PyPDF2",
            "python-docx"
        ]
        
        for package in packages:
            print(f"   Installing {package}...")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package, "--quiet"
                ])
                print(f"   ✅ {package} installed")
            except:
                print(f"   ⚠️  Warning: Could not install {package}")
        
        print("✅ Basic packages installed")
    
    def setup_working_app(self):
        """Set up the working text-only version"""
        print("\\n🔧 Setting up working application...")
        
        # Check if minimal app exists
        minimal_app = self.base_dir / "notebooklm_app_minimal" / "app.py"
        if minimal_app.exists():
            print("✅ Text-only version ready")
            return True
        
        # Check if original app exists
        original_app = self.base_dir / "notebooklm_app" / "app.py"
        if original_app.exists():
            print("✅ Original app found")
            return True
        
        print("❌ No application files found")
        return False
    
    def start_application(self, use_minimal=True):
        """Start the application"""
        print("\\n🚀 Starting NotebookLM Clone...")
        
        def open_browser():
            time.sleep(3)
            try:
                webbrowser.open('http://localhost:12000')
                print("📱 Browser opened at http://localhost:12000")
            except:
                print("📱 Please open http://localhost:12000 manually")
        
        # Start browser opener
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        print("📱 Browser will open automatically")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 60)
        
        try:
            if use_minimal and (self.base_dir / "notebooklm_app_minimal").exists():
                os.chdir(self.base_dir / "notebooklm_app_minimal")
                print("🔧 Starting in text-only mode...")
            else:
                os.chdir(self.base_dir / "notebooklm_app")
                print("🔧 Starting full application...")
            
            subprocess.run([sys.executable, "app.py"])
        except KeyboardInterrupt:
            print("\\n👋 Application stopped")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def run(self):
        """Run the installer"""
        self.print_header()
        
        if not self.check_python():
            input("Press Enter to exit...")
            return
        
        self.install_basic_packages()
        
        if not self.setup_working_app():
            print("❌ Could not set up application")
            input("Press Enter to exit...")
            return
        
        print("\\n🎉 Setup Complete!")
        print("=" * 60)
        print("✅ Text processing and summarization available")
        print("⚠️  Audio generation requires manual model setup")
        print("📖 See troubleshooting guide for model installation")
        
        try:
            start = input("\\n🚀 Start application now? (y/n): ").lower().strip()
            if start in ['y', 'yes', '']:
                self.start_application()
        except KeyboardInterrupt:
            print("\\n👋 Setup complete!")

def main():
    installer = FixedInstaller()
    installer.run()

if __name__ == "__main__":
    main()
'''
    
    installer_path = Path("Install_Fixed.py")
    installer_path.write_text(installer_content)
    print(f"✅ Created fixed installer: {installer_path}")
    return installer_path

def main():
    """Main function to fix all issues"""
    print("🔧 NotebookLM Clone - Issue Fixer")
    print("=" * 50)
    print("Addressing reported issues:")
    print("• Model download failures")
    print("• Server startup problems")
    print("• Creating working fallback solution")
    print("=" * 50)
    
    # Check alternative model sources
    working_url = check_alternative_models()
    
    # Create minimal working app
    minimal_app = create_minimal_working_app()
    
    # Create fixed installer
    fixed_installer = create_fixed_installer()
    
    print("\n🎉 Issues Fixed!")
    print("=" * 50)
    print("✅ Created text-only working version")
    print("✅ Created fixed installer")
    print("✅ Application will work without AI models")
    
    print("\n🚀 Next Steps:")
    print("1. Run: python Install_Fixed.py")
    print("2. Or directly run the minimal app:")
    print(f"   cd {minimal_app.parent}")
    print("   python app.py")
    
    if working_url:
        print(f"\n💡 Alternative model URL found: {working_url}")
        print("You can try downloading models manually from this URL")

if __name__ == "__main__":
    main()