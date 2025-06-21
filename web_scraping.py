import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0'
}


#use a webnovel from https://novelbin.me/
url = input("Enter the URL of the page: ")
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
c = soup.find('div').text
if c:
    print(c)
else:
    print("Error:Could not find the chapter content")