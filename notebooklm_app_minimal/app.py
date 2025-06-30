#!/usr/bin/env python3
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
            text += paragraph.text + "\n"
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
        webbrowser.open('http://localhost:12001')
        print("📱 Browser opened at http://localhost:12001")
    except:
        print("📱 Please open http://localhost:12001 in your browser")

if __name__ == '__main__':
    print("🎵 NotebookLM Clone - Text-Only Mode")
    print("=" * 50)
    print("🔧 Running in text-only mode (no audio generation)")
    print("📱 Browser will open automatically at http://localhost:12001")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 50)
    
    # Start browser opener
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    try:
        app.run(host='0.0.0.0', port=12001, debug=False)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        input("Press Enter to exit...")
