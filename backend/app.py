from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
from kokoro import KPipeline
import soundfile as sf
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/url', methods=['POST'])
def get_url():
    data = request.json
    url = data.get('url', '').strip()

    if not url:
        return jsonify({'message' : 'URL is required'})
    if not url.startswith(('https://', 'http://')):
        url = 'https://' + url

    result = scrape(url)

    if result:
        return jsonify({'message' : 'Successfully scraped the URL'})
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

@app.route('/')
def home():
    return jsonify({"Message": "Your flask server is running"})
if __name__ == '__main__':
    app.run(debug=True, port=5000)