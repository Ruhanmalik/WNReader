from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
from kokoro import KPipeline
import soundfile as sf
import os
import torch

app = Flask(__name__)
CORS(app)

# Removed MPS fallback as it might cause issues with Kokoro TTS

@app.route('/api/audio', methods=['GET'])
def get_audio():
    if os.path.exists('output_audio.wav'):
        return send_file('output_audio.wav', mimetype='audio/wav')
    else:
        return jsonify({'error': 'Audio file not found'}), 404

@app.route('/api/audio/status', methods=['GET'])
def get_audio_status():
    exists = os.path.exists('output_audio.wav')
    return jsonify({
        'exists': exists,
        'timestamp': os.path.getmtime('output_audio.wav') if exists else None
    })

@app.route('/api/url', methods=['POST'])
def get_url():
    data = request.json
    url = data.get('url', '').strip()



    if not url:
        return jsonify({'message' : 'URL is required'})
    if not url.startswith(('https://', 'http://')):
        url = 'https://' + url

    result = scrape(url)

    if os.path.exists("output.txt"):
        audio = tts("output.txt")

    if audio:
        return jsonify({'message' : 'Successfully converted text to audio'})
    elif result:
        return jsonify({'message' : 'Successfully scraped the URL but audio conversion failed'})
    else:
        return jsonify({'message' : 'Failed to scrape the URL'})


def scrape(url):
    try:
        r = requests.get(url)
        # Parse the HTML
        soup = BeautifulSoup(r.text, 'html.parser')
        c = soup.find("div", id="showReading")

        if c:
            text = clean_text(c.text)
            with open("output.txt", "w", encoding="utf-8") as f:
                f.write(text)

            clean_text("output.txt")
            return True 
        else:
            print("Error: Could not find the tag you inputted")
            return False

    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch page - {e}")
        return False
        
def clean_text(text):
    # Remove excessive whitespace and newlines
    text = re.sub(r'\s+', ' ', text.strip())
    # Replace censored words (e.g., "F * ck" -> "Fuck")
    text = re.sub(r'F\s*\*\s*ck', 'Fuck', text)
    # Remove or replace special characters that might disrupt TTS
    text = re.sub(r'[^\w\s.,!?]', '', text)
    # Normalize punctuation spacing (e.g., "Pain!So" -> "Pain! So")
    text = re.sub(r'([!?.])(\w)', r'\1 \2', text)  # Capture word character in group 2
    return text

def tts(text):
    """
    Convert text file to audio using Kokoro TTS
    """
        
    print("Converting text to audio...")

    # Check device availability
    if torch.backends.mps.is_available():
        device = "mps"
        print(f"✅ MPS (Apple Silicon GPU) is available - using device: {device}")
    else:
        device = "cpu"
        print(f"❌ MPS not available - using device: {device}")

    # Additional device info
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    print(f"MPS available: {torch.backends.mps.is_available()}")
    
    try:
        pipeline = KPipeline(lang_code='a', device=device)
        print(f"✅ KPipeline initialized with device: {device}")
    except Exception as e:
        print(f"❌ Error initializing KPipeline with device {device}: {e}")
        # Fallback to CPU if MPS fails
        device = "cpu"
        pipeline = KPipeline(lang_code='a', device=device)
        print(f"🔄 Fallback to CPU device: {device}")

    try:
        # Read the text file
        with open(text, "r", encoding="utf-8") as f:
            text = f.read()

            voice = 'af_sarah'
            speed = 1.0

            print(f"🎤 Generating audio with voice: {voice}, speed: {speed}")
            
            try:
                generator = pipeline(text, voice=voice, speed=speed)
                audio_segments = []

                for i, (gs, ps, audio) in enumerate(generator):
                    audio_segments.append(audio)
                    sf.write(f'chunk_{i}.wav', audio, 24000)

                # Combine all chunks into one file using FFmpeg
                print("Combining audio chunks...")
                
                # Create a file list for FFmpeg
                with open('filelist.txt', 'w') as f:
                    for i in range(len(audio_segments)):
                        f.write(f"file 'chunk_{i}.wav'\n")
                
                # Use FFmpeg to concatenate all chunks
                os.system('ffmpeg -f concat -safe 0 -i filelist.txt -c copy output_audio.wav')
                
                # Clean up temporary files
                for i in range(len(audio_segments)):
                    if os.path.exists(f'chunk_{i}.wav'):
                        os.remove(f'chunk_{i}.wav')
                
                if os.path.exists('filelist.txt'):
                    os.remove('filelist.txt')
                
                print("Audio successfully combined into output_audio.wav")
                return True
                
            except RuntimeError as e:
                if "Output channels > 65536 not supported at the MPS device" in str(e):
                    print(f"⚠️ MPS channel limit error detected: {e}")
                    print("🔄 Retrying with CPU device...")
                    
                    # Retry with CPU
                    pipeline = KPipeline(lang_code='a', device="cpu")
                    generator = pipeline(text, voice=voice, speed=speed)
                    audio_segments = []

                    for i, (gs, ps, audio) in enumerate(generator):
                        audio_segments.append(audio)
                        sf.write(f'chunk_{i}.wav', audio, 24000)

                    # Combine all chunks into one file using FFmpeg
                    print("Combining audio chunks with CPU...")
                    
                    # Create a file list for FFmpeg
                    with open('filelist.txt', 'w') as f:
                        for i in range(len(audio_segments)):
                            f.write(f"file 'chunk_{i}.wav'\n")
                    
                    # Use FFmpeg to concatenate all chunks
                    os.system('ffmpeg -f concat -safe 0 -i filelist.txt -c copy output_audio.wav')
                    
                    # Clean up temporary files
                    for i in range(len(audio_segments)):
                        if os.path.exists(f'chunk_{i}.wav'):
                            os.remove(f'chunk_{i}.wav')
                    
                    if os.path.exists('filelist.txt'):
                        os.remove('filelist.txt')
                    
                    print("Audio successfully combined into output_audio.wav using CPU")
                    return True
                else:
                    raise e
        
    except Exception as e:
        print(f"Error in TTS conversion: {e}")
        return None

@app.route('/')
def home():
    return jsonify({"Message": "Your flask server is running"})
if __name__ == '__main__':
    app.run(debug=True, port=5000)