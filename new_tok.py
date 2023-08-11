import requests
import json
from urllib.parse import urljoin
from urllib.parse import urlparse
import os
from dotenv import load_dotenv

load_dotenv()

def shorten_link(token,url):
    url_shorten = "https://api-ssl.bitly.com/v4/shorten"
    headers = {
        "Authorization": f"{token}"
    }

    payload = {
        "long_url": f"{url}"
    }

    response = requests.post(url_shorten, headers = headers, json = payload)
    response.raise_for_status()
    return response.json()['link']

def count_clicks(token, link):
    payload = {"unit": "day", "units": "-1"}
    
    headers = {
        "Authorization": f"{token}"
    }
    
    parsed = urlparse(link)
    full_url = 'https://api-ssl.bitly.com/v4/bitlinks/' + parsed.netloc + parsed.path +  '/clicks/summary'
    response = requests.get(full_url, headers = headers, params=payload)
    response.raise_for_status()
    return response.json()['total_clicks']

def is_bitlink(url):
    parsed = urlparse(url)
    if 'bit.ly' in parsed.netloc:
        return True
    return False

if __name__ == '__main__':
    url = input("Vvdeite link: ")
    token = os.environ["TOKEN"]
    if is_bitlink(url):
        try:
            counts = count_clicks(token, url)
        except requests.exceptions.HTTPError:
            input("Fake bitlink!!!")
            exit(1)
        print(counts)
    else:
        try:
            bitlink = shorten_link(token, url)
        except requests.exceptions.HTTPError:
            input("Wrong url!!!")
            exit(1)
        print('Битлинк', shorten_link(token, url))




