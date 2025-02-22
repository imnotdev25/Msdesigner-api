import os
import random
from uuid import uuid4

from httpx import Client


def download_images(urls: list, save_path: str = 'images', resolution: str = '1024x1024') -> list:
    """
    Download images from URLs and save them to specified path
    :param urls: List of image URLs to download
    :param save_path: Base directory path to save images
    :param resolution: Resolution for folder organization (1024x1024, 1024x1792, 1792x1024)
    :return: List of saved image file paths
    """
    # Create resolution-specific folder
    folder_path = os.path.join(save_path, resolution)
    os.makedirs(folder_path, exist_ok=True)

    client = Client()
    img_paths = []
    for url in urls:
        resp = client.get(url, timeout=10)
        with open(f"{folder_path}/{uuid4()}.jpg", "wb") as f:
            f.write(resp.content)
            f.close()
        img_paths.append(f.name)
    return img_paths


def get_random_boundary() -> str:
    """
    Generate a random WebKit-style boundary for multipart form data
    :return: Random boundary string
    """
    timestamp = int(random.random() * 1000000000)
    return f"WebKitFormBoundary{''.join(['abcdef'[int(i) % 6] for i in str(timestamp)])}"
