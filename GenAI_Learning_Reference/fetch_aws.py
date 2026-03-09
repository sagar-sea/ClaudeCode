import urllib.request
import re
from bs4 import BeautifulSoup

url = "https://aws.amazon.com/what-is/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('https://aws.amazon.com/what-is/') and href != "https://aws.amazon.com/what-is/":
            # only keep the main category link without query parameters or fragments
            base_link = href.split('?')[0].split('#')[0]
            if base_link.startswith('https://aws.amazon.com/what-is/'):
                links.add(base_link)
    
    for link in sorted(links):
        print(link)
except Exception as e:
    print("Error:", e)
