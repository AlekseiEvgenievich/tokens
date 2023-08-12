import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv


def shorten_link(token, url):
    url_shorten = "https://api-ssl.bitly.com/v4/shorten"
    headers = {
        "Authorization": token
    }
    payload = {
        "long_url": url
    }
    response = requests.post(url_shorten, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, link):
    payload = {"unit": "day", "units": "-1"}
    headers = {
        "Authorization": token
    }
    parsed = urlparse(link)
    site = 'https://api-ssl.bitly.com/v4/bitlinks/'
    summary = '/clicks/summary'
    full_url = f"{site}{parsed.netloc}{parsed.path}{summary}"
    response = requests.get(full_url, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(url, token):
    headers = {
        "Authorization": token
    }
    parsed = urlparse(url)
    site = 'https://api-ssl.bitly.com/v4/bitlinks/'
    full_url = f"{site}{parsed.netloc}{parsed.path}"
    response = requests.get(full_url, headers=headers)
    if response.ok:
        return True
    return False


if __name__ == '__main__':
    load_dotenv()
    url = input("Vvdeite link: ")
    token = os.environ["BITTLY_TOKEN"]
    if is_bitlink(url, token):
        try:
            counts = count_clicks(token, url)
            print(counts)
        except requests.exceptions.HTTPError:
            print("Вы ввели неверный битлинк")
    else:
        try:
            bitlink = shorten_link(token, url)
            print('Битлинк', bitlink)
        except requests.exceptions.HTTPError:
            print("Вы ввели неправильную ссылку")
