import requests
from bs4 import BeautifulSoup

# Use a more specific User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

# Get URL from user
url = input("Enter the URL of the page: ")

try:
    # Fetch the page
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()  # Raise an exception for non-200 status codes

    # Parse the HTML
    soup = BeautifulSoup(r.text, 'html.parser')
    c = soup.find("div", id="chr-content", class_="chr-c")

    if c:
        # Extract only the text from <p> tags, excluding ad divs
        paragraphs = c.find_all('p')
        chapter_text = '\n'.join(p.get_text(strip=True) for p in paragraphs if not p.find_parent('div', id=lambda x: x and x.startswith('pf-')))
        if chapter_text.strip():
            print(f"Chapter Content:\n{chapter_text}")
        else:
            print("Error: No chapter text found in the content")
    else:
        print("Error: Could not find the chapter content")

except requests.exceptions.RequestException as e:
    print(f"Error: Failed to fetch page - {e}")