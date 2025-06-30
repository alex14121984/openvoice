# NotebookLM Clone - AI Audio Overview Generator

A local web application that mimics Google's NotebookLM functionality, allowing users to upload content and generate AI-powered audio overviews using OpenVoice TTS.

## 🚀 Features

- **Multi-Input Support**: Upload URLs, files (PDF, DOCX, TXT), or paste text directly
- **Intelligent Summarization**: Automatically generates concise summaries of your content
- **AI Audio Overview**: Creates natural-sounding audio narration using OpenVoice TTS
- **Web Interface**: Clean, responsive UI similar to NotebookLM
- **Real-time Processing**: Live feedback during content processing and audio generation

## 📋 Requirements

### System Dependencies
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y ffmpeg libavcodec-dev libavformat-dev libavutil-dev libswscale-dev libswresample-dev

# macOS
brew install ffmpeg

# Windows
# Download ffmpeg from https://ffmpeg.org/download.html
```

### Python Dependencies
```bash
pip install -r requirements.txt
```

## 🛠️ Setup Instructions

1. **Clone OpenVoice Repository**:
```bash
git clone https://github.com/myshell-ai/OpenVoice.git openvoice
cd openvoice
```

2. **Download OpenVoice Models**:
```bash
# Download V1 checkpoints
wget https://myshell-public-repo-hosting.s3.amazonaws.com/openvoice/checkpoints_v1_0509.zip
unzip checkpoints_v1_0509.zip
```

3. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the Application**:
```bash
python app.py
```

5. **Access the Web Interface**:
   - Open your browser to `http://localhost:12000`

## 🎵 Extending Audio Length

The current audio is limited to ~8 seconds due to text truncation for faster processing. To extend:

1. **Edit `app.py`** - Modify the `generate_audio_overview()` function:
```python
# Change this line (around line 144):
if len(overview_text) > 150:
    overview_text = overview_text[:150] + "."

# To this for longer audio:
if len(overview_text) > 500:  # or any length you prefer
    overview_text = overview_text[:500] + "."
```

2. **For even longer content**, modify the `generate_summary()` function to return more sentences:
```python
# Change this line (around line 120):
sentences = sentences[:3]  # Limit to 3 sentences

# To this:
sentences = sentences[:10]  # Or any number you prefer
```

## 🔧 Customization Options

### Voice Customization
- Replace the reference speaker file in OpenVoice to change the voice
- Modify the TTS parameters in `generate_audio_overview()`

### Content Processing
- Adjust summarization length in `generate_summary()`
- Modify content extraction logic for different file types
- Add support for additional file formats

### UI Customization
- Edit `templates/index.html` to modify the interface
- Customize CSS styles and layout
- Add new features or input methods

## 📁 Project Structure

```
notebooklm_app/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Web interface
└── README.md          # This file

openvoice/             # OpenVoice TTS models (separate download)
├── checkpoints/       # Pre-trained models
└── ...               # OpenVoice source code
```

## 🎯 What Makes This More Than Just TTS

This is a complete NotebookLM clone that includes:

1. **Content Intelligence**: Automatically extracts and summarizes content from various sources
2. **Multi-modal Input**: Handles URLs, documents, and text with intelligent parsing
3. **Context-Aware Summaries**: Generates meaningful overviews, not just reading text
4. **Professional Audio**: Uses advanced voice cloning for natural-sounding narration
5. **Web Application**: Complete user interface for easy interaction

## 🚀 Next Steps

- Add support for multiple voices/speakers
- Implement longer audio generation with chapters
- Add real-time streaming audio generation
- Support for more file formats (PowerPoint, Excel, etc.)
- Integration with cloud storage services

## 📝 License

This project combines multiple open-source components. Please check individual licenses for OpenVoice and other dependencies.