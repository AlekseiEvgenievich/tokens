import requests
from urllib.parse import urlparse
import os
import sys
import argparse
from dotenv import load_dotenv


def shorten_link(token, url):
    short_url = "https://api-ssl.bitly.com/v4/shorten"
    headers = {
        "Authorization": token
    }
    payload = {
        "long_url": url
    }
    response = requests.post(short_url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, link):
    payload = {"unit": "day", "units": "-1"}
    headers = {
        "Authorization": token
    }
    parse_array = urlparse(link)
    site = 'https://api-ssl.bitly.com/v4/bitlinks/'
    summary = '/clicks/summary'
    full_url = f"{site}{parse_array.netloc}{parse_array.path}{summary}"
    response = requests.get(full_url, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(url, token):
    headers = {
        "Authorization": token
    }
    parse_array = urlparse(url)
    site = 'https://api-ssl.bitly.com/v4/bitlinks/'
    full_url = f"{site}{parse_array.netloc}{parse_array.path}"
    response = requests.get(full_url, headers=headers)
    return response.ok


def createParser ():
    parser = argparse.ArgumentParser(description='Программа предназначена для сокращения ссылок с использованием сервиса Bitly, а также подсчета количества переходов по сокращенной ссылке.')
    parser.add_argument('link')
    return parser


if __name__ == '__main__':
    load_dotenv()
    parser = createParser()
    args = parser.parse_args(sys.argv[1:])
    url = args.link
    token = os.environ["BITLY_TOKEN"]
    if is_bitlink(url, token):
        try:
            counts = count_clicks(token, url)
            print('По вашей ссылки прошли: {} раз(а)'.format(counts))
        except requests.exceptions.HTTPError:
            print("Вы ввели неверный битлинк")
    else:
        try:
            bitlink = shorten_link(token, url)
            print('Битлинк:', bitlink)
        except requests.exceptions.HTTPError:
            print("Вы ввели неправильную ссылку")
