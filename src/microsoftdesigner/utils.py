import os
import random
from urllib.parse import urlparse, urlunparse
from uuid import uuid4

from bs4 import BeautifulSoup
from httpx import Client
from microsoftdesigner.logger import logger


def get_urls_from_html(html: str) -> list:
    soup = BeautifulSoup(html, 'html.parser')
    logger.info(f"Found {len(soup.find_all('img', {'data-src': True}))} urls")
    return [img['data-src'] for img in soup.find_all('img', {'data-src': True})]


def clean_urls(urls: list) -> list:
    parsed_urls = [urlparse(url) for url in urls]
    logger.info(f"Before url cleaning: {len(parsed_urls)}")
    return [urlunparse(parsed_url._replace(query="")) for parsed_url in parsed_urls]


def download_images(urls: list, save_path: str) -> list:
    os.makedirs(save_path, exist_ok=True)
    client = Client()
    img_paths = []
    for url in urls:
        resp = client.get(url, timeout=10)
        with open(f"{save_path}/{uuid4()}.jpg", "wb") as f:
            f.write(resp.content)
            f.close()
        img_paths.append(f.name)
    return img_paths


def get_bing_id(url: str) -> str:
    return urlparse(url).path.split("/")[-1]


def get_random_boundary() -> str:
    return str(random.randint(10 ** 27, 10 ** 28 - 1))
