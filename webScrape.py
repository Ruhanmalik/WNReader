import requests
from bs4 import BeautifulSoup
import re
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

def main():
    # Get URL from user
    url = input("Enter the URL of the page: ")
    scrape(url)
    clean_text("output.txt")

main()