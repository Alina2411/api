import os
from dotenv import load_dotenv
import argparse
import requests
from urllib.parse import urlparse


def shorten_link(token, link):
    url = "https://api-ssl.bitly.com/v4/shorten"
    params = { "long_url": link }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, headers=headers, json=params)
    response.raise_for_status()
    return response.json()['id']


def count_clicks(token, bitlink):
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    params = { "unit": 'month',
              "units": -1,}
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(token, bitlink):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    token = os.environ['BITLY_TOKEN']
    parser = argparse.ArgumentParser(
        description='Описание что делает программа'
    )
    parser.add_argument('--link', help='Введите ссылку:')
    args = parser.parse_args()
    parse_url = urlparse(args.link)
    parse_url = f"{parse_url.netloc}{parse_url.path}"
    try:
        if is_bitlink(token, parse_url):
            print(count_clicks(token, parse_url))
        else:
            print(shorten_link(token, args.link))
    except requests.exceptions.HTTPError:
        print("Неправильная ссылка, проверьте свою ссылку")


if __name__ == "__main__":
    main()