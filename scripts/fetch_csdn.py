#!/usr/bin/env python3
import urllib.request
from bs4 import BeautifulSoup
import sys

def fetch_csdn(url):
    req = urllib.request.Request(
        url, 
        headers={"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
    )
    try:
        html = urllib.request.urlopen(req).read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find(id="content_views")
        if content:
            print(content.get_text().strip())
        else:
            print("Error: Could not find 'content_views' div. The page layout might have changed or access was denied.")
    except Exception as e:
        print(f"Error fetching URL: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_csdn.py <csdn_url>")
        sys.exit(1)
    fetch_csdn(sys.argv[1])
