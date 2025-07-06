import requests
from bs4 import BeautifulSoup
import re
from kokoro import KPipeline
import soundfile as sf
import os
# Use a more specific User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}



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
        else:
            print("Error: Could not find the tag you inputted")

    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch page - {e}")

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

    pipeline = KPipeline(lang_code='a')
    try:
        # Read the text file
        with open(text, "r", encoding="utf-8") as f:
            text = f.read()

            voice = 'af_sarah'
            speed = 1.0

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
        
    except Exception as e:
        print(f"Error in TTS conversion: {e}")
        return None

def main():
    # Get URL from user
    url = input("Enter the URL of the page: ")
    scrape(url)
    
    # Check if output.txt exists and convert to audio
    if os.path.exists("output.txt"):
        print("Converting text to audio...")
        tts("output.txt")
    else:
        print("No output.txt file found. Please run the scraper first.")

main()