#!/usr/bin/env python3
"""
Test OpenVoice audio generation
"""

import sys
import os
sys.path.append('/workspace/openvoice')

import torch
from openvoice import se_extractor
from openvoice.api import BaseSpeakerTTS, ToneColorConverter

def test_audio_generation():
    print("Testing OpenVoice audio generation...")
    
    # Configuration
    OPENVOICE_BASE_PATH = '/workspace/openvoice'
    EN_CKPT_BASE = f'{OPENVOICE_BASE_PATH}/checkpoints/base_speakers/EN'
    CKPT_CONVERTER = f'{OPENVOICE_BASE_PATH}/checkpoints/converter'
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    
    try:
        # Load models
        print("Loading models...")
        en_base_speaker_tts = BaseSpeakerTTS(f'{EN_CKPT_BASE}/config.json', device=device)
        en_base_speaker_tts.load_ckpt(f'{EN_CKPT_BASE}/checkpoint.pth')
        
        tone_color_converter = ToneColorConverter(f'{CKPT_CONVERTER}/config.json', device=device)
        tone_color_converter.load_ckpt(f'{CKPT_CONVERTER}/checkpoint.pth')
        
        en_source_default_se = torch.load(f'{EN_CKPT_BASE}/en_default_se.pth').to(device)
        
        print("Models loaded successfully!")
        
        # Test text
        test_text = "Here's an overview of the content: Artificial Intelligence has revolutionized many aspects of our daily lives."
        
        # Generate TTS
        print("Generating TTS...")
        temp_tts_path = "/tmp/test_tts.wav"
        en_base_speaker_tts.tts(test_text, temp_tts_path, speaker='default', language='English')
        print(f"TTS generated: {temp_tts_path}")
        
        # Use reference speaker
        reference_speaker = f"{OPENVOICE_BASE_PATH}/resources/demo_speaker0.mp3"
        print(f"Using reference speaker: {reference_speaker}")
        
        # Extract target speaker embedding
        print("Extracting speaker embedding...")
        target_se, _ = se_extractor.get_se(reference_speaker, tone_color_converter, target_dir='/tmp/processed', vad=True)
        print("Speaker embedding extracted!")
        
        # Convert tone color
        print("Converting tone color...")
        output_path = "/tmp/test_output.wav"
        tone_color_converter.convert(
            audio_src_path=temp_tts_path,
            src_se=en_source_default_se,
            tgt_se=target_se,
            output_path=output_path,
            message="@Test"
        )
        
        print(f"Audio generated successfully: {output_path}")
        
        # Check file size
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"Output file size: {size} bytes")
            return True
        else:
            print("Output file not created!")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_audio_generation()
    if success:
        print("✓ Test completed successfully!")
    else:
        print("✗ Test failed!")