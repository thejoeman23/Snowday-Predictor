from pathlib import Path
import sys

from bs4 import BeautifulSoup
import requests

if __name__ == "__main__" and __package__ is None:
    sys.path.append(str(Path(__file__).resolve().parents[2]))

base = "https://www.snowdaypredictor.com/prediction/"

def find_prediction(soup):
    for span in soup.find_all("span"):
        if "%" in span.text:
            return span.text[:-1]  # Remove the '%' sign

def fetch_prediction(location_slug):
    if not location_slug:
        raise ValueError("Location slug cannot be empty.")

    url = base + location_slug + "-on"
    response = requests.get(url, timeout=15)
    soup = BeautifulSoup(response.content, "html.parser")
    return find_prediction(soup)


if __name__ == "__main__":
    print(fetch_prediction("owen-sound"))