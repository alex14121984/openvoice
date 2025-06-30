#!/usr/bin/env python3
"""
NotebookLM-like Application with OpenVoice Integration
A web application that allows users to upload sources and generate audio overviews
"""

import os
import sys
import tempfile
import logging
from pathlib import Path

# Add OpenVoice to path
sys.path.append('/workspace/openvoice')

from flask import Flask, render_template, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
import requests
from bs4 import BeautifulSoup
import torch

# OpenVoice imports
from openvoice import se_extractor
from openvoice.api import BaseSpeakerTTS, ToneColorConverter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['OUTPUT_FOLDER'] = '/tmp/outputs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# OpenVoice configuration
OPENVOICE_BASE_PATH = '/workspace/openvoice'
EN_CKPT_BASE = f'{OPENVOICE_BASE_PATH}/checkpoints/base_speakers/EN'
ZH_CKPT_BASE = f'{OPENVOICE_BASE_PATH}/checkpoints/base_speakers/ZH'
CKPT_CONVERTER = f'{OPENVOICE_BASE_PATH}/checkpoints/converter'

# Global variables for models
en_base_speaker_tts = None
zh_base_speaker_tts = None
tone_color_converter = None
en_source_default_se = None
device = None

def initialize_openvoice():
    """Initialize OpenVoice models"""
    global en_base_speaker_tts, zh_base_speaker_tts, tone_color_converter, en_source_default_se, device
    
    try:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        logger.info(f"Using device: {device}")
        
        # Load models
        en_base_speaker_tts = BaseSpeakerTTS(f'{EN_CKPT_BASE}/config.json', device=device)
        en_base_speaker_tts.load_ckpt(f'{EN_CKPT_BASE}/checkpoint.pth')
        
        zh_base_speaker_tts = BaseSpeakerTTS(f'{ZH_CKPT_BASE}/config.json', device=device)
        zh_base_speaker_tts.load_ckpt(f'{ZH_CKPT_BASE}/checkpoint.pth')
        
        tone_color_converter = ToneColorConverter(f'{CKPT_CONVERTER}/config.json', device=device)
        tone_color_converter.load_ckpt(f'{CKPT_CONVERTER}/checkpoint.pth')
        
        # Load speaker embeddings
        en_source_default_se = torch.load(f'{EN_CKPT_BASE}/en_default_se.pth').to(device)
        
        logger.info("OpenVoice models initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize OpenVoice: {e}")
        return False

def extract_text_from_url(url):
    """Extract text content from a URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
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

def extract_text_from_file(file_path):
    """Extract text content from uploaded file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content[:5000]  # Limit to 5000 characters
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        return None

def generate_summary(text):
    """Generate a summary of the text content"""
    # Simple extractive summarization - take first few sentences
    sentences = text.split('. ')
    summary_sentences = sentences[:5]  # Take first 5 sentences for longer overview
    summary = '. '.join(summary_sentences)
    
    if len(summary) > 600:
        summary = summary[:600] + "..."
    
    return summary

def generate_audio_overview(text, output_path):
    """Generate audio overview using OpenVoice (simplified version)"""
    try:
        logger.info("Starting audio generation...")
        if not en_base_speaker_tts:
            raise Exception("OpenVoice TTS model not initialized")
        
        # Generate summary
        summary = generate_summary(text)
        logger.info(f"Generated summary: {summary[:100]}...")
        
        # Create a more engaging overview text
        overview_text = f"Here's an overview of the content: {summary}"
        
        # Allow longer audio - up to 500 characters for ~30-45 seconds of audio
        if len(overview_text) > 500:
            overview_text = overview_text[:500] + "."
        
        logger.info(f"Overview text: {overview_text}")
        
        # Generate TTS directly to output path (using default voice)
        logger.info("Generating TTS...")
        en_base_speaker_tts.tts(overview_text, output_path, speaker='default', language='English')
        logger.info("TTS generated successfully")
        
        # Check if output file was created
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            logger.info(f"Audio file created successfully: {size} bytes")
            return True
        else:
            logger.error("Output audio file was not created")
            return False
            
    except Exception as e:
        logger.error(f"Error generating audio overview: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_source():
    """Handle source upload (URL, file, or text)"""
    try:
        source_type = request.form.get('source_type')
        text_content = None
        
        if source_type == 'url':
            url = request.form.get('url')
            if not url:
                return jsonify({'error': 'URL is required'}), 400
            
            text_content = extract_text_from_url(url)
            if not text_content:
                return jsonify({'error': 'Failed to extract content from URL'}), 400
                
        elif source_type == 'file':
            if 'file' not in request.files:
                return jsonify({'error': 'No file uploaded'}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if file and file.filename.endswith('.txt'):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                text_content = extract_text_from_file(file_path)
                os.remove(file_path)  # Clean up
                
                if not text_content:
                    return jsonify({'error': 'Failed to read file content'}), 400
            else:
                return jsonify({'error': 'Only .txt files are supported'}), 400
                
        elif source_type == 'text':
            text_content = request.form.get('text')
            if not text_content:
                return jsonify({'error': 'Text content is required'}), 400
        else:
            return jsonify({'error': 'Invalid source type'}), 400
        
        # Generate audio overview
        audio_filename = f"overview_{int(torch.randint(0, 1000000, (1,)).item())}.wav"
        audio_path = os.path.join(app.config['OUTPUT_FOLDER'], audio_filename)
        
        success = generate_audio_overview(text_content, audio_path)
        
        if not success:
            return jsonify({'error': 'Failed to generate audio overview'}), 500
        
        # Generate summary for display
        summary = generate_summary(text_content)
        
        return jsonify({
            'success': True,
            'summary': summary,
            'audio_url': url_for('get_audio', filename=audio_filename),
            'text_preview': text_content[:500] + "..." if len(text_content) > 500 else text_content
        })
        
    except Exception as e:
        logger.error(f"Error in upload_source: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/audio/<filename>')
def get_audio(filename):
    """Serve generated audio files"""
    try:
        audio_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(audio_path):
            return send_file(audio_path, mimetype='audio/wav')
        else:
            return jsonify({'error': 'Audio file not found'}), 404
    except Exception as e:
        logger.error(f"Error serving audio: {e}")
        return jsonify({'error': 'Error serving audio file'}), 500

@app.route('/download/<filename>')
def download_audio(filename):
    """Download audio files"""
    try:
        audio_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(audio_path):
            return send_file(audio_path, as_attachment=True, download_name=f"notebooklm_overview_{filename}")
        else:
            return jsonify({'error': 'Audio file not found'}), 404
    except Exception as e:
        logger.error(f"Error downloading audio: {e}")
        return jsonify({'error': 'Error downloading audio file'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'openvoice_initialized': en_base_speaker_tts is not None,
        'device': device
    })

if __name__ == '__main__':
    # Initialize OpenVoice
    if not initialize_openvoice():
        logger.error("Failed to initialize OpenVoice. Exiting.")
        sys.exit(1)
    
    # Run the app
    app.run(host='0.0.0.0', port=12000, debug=True)