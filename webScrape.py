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
            text = c.get_text(strip=True)
            with open("output.txt", "w", encoding="utf-8") as f:
                f.write(text)
        else:
            print("Error: Could not complete the request")

    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch page - {e}")


def main():
    # Get URL from user
    url = input("Enter the URL of the page: ")
    scrape(url)

main()