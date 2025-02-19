import argparse
import sys
import time

import httpx
from microsoftdesigner.constants import HEADERS, PARAMS, MS_BASE_URL
from microsoftdesigner.logger import logger
from microsoftdesigner.utils import clean_urls, download_images, get_urls_from_html, get_bing_id, get_random_boundary


def create_img(user_id: str, auth_token: str, prompt: str, save_path: str = 'images',
               resolution: str = '1024x1024') -> list:
    """
    Generate image using Microsoft Designer API
    :param user_id: User ID
    :param auth_token: Auth Token ( Bearer ey... )
    :param prompt: Prompt
    :param save_path: Save Path
    :param resolution: Resolution (1024x1024, 1024x1792, 1792x1024)
    :return: Image Path
    """
    random_boundry = get_random_boundary()
    data = (f'-----------------------------{random_boundry}\r\n'
            f'Content-Disposition: form-data; name="dalle-caption"\r\n\r\n{prompt}\r\n'
            f'-----------------------------{random_boundry}\r\n'
            f'Content-Disposition: form-data; name="dalle-scenario-name"\r\n'
            f'\r\nTextToImage\r\n'
            f'-----------------------------{random_boundry}\r\n'
            f'Content-Disposition: form-data; name="dalle-batch-size"\r\n'
            f'\r\n4\r\n'
            f'-----------------------------{random_boundry}\r\n'
            f'Content-Disposition: form-data; name="dalle-image-response-format"\r\n'
            f'\r\nUrlWithBase64Thumbnail\r\n'
            f'-----------------------------{random_boundry}\r\n'
            f'Content-Disposition: form-data; name="dalle-seed"\r\n'
            f'\r\n104'
            f'-----------------------------{random_boundry}\r\n'
            f'Content-Disposition: form-data; name="ClientFlights"\r\n'
            f'\r\nEnableBICForDALLEFlight\r\n'
            f'-----------------------------{random_boundry}\r\n'
            f'Content-Disposition: form-data; name="dalle-hear-back-in-ms"\r\n'
            f'\r\n1000\r\n'
            f'-----------------------------{random_boundry}\r\n'
            f'Content-Disposition: form-data; name="dalle-include-b64-thumbnails"\r\n'
            f'\r\ntrue\r\n'
            f'-----------------------------{random_boundry}\r\n'
            f'Content-Disposition: form-data; name="dalle-aspect-ratio-scaling-factor-b64-thumbnails"\r\n'
            f'\r\n0.3\r\n'
            f'-----------------------------{random_boundry}\r\n'
            f'Content-Disposition: form-data; name="dalle-image-size"\r\n'
            f'\r\n{resolution}\r\n'
            f'\r\n-----------------------------{random_boundry}--\r\n')
    headers = HEADERS.copy()
    headers['Authorization'] = auth_token
    headers['UserId'] = user_id
    headers['Content-Type'] = f'multipart/form-data; boundary=---------------------------{random_boundry}'
    try:
        with httpx.Client() as client:
            response = client.post(MS_BASE_URL, params=PARAMS, data=data, headers=headers, timeout=60)
            if response.status_code == 200:
                client.close()
                poll_url = response.json()['polling_response']['polling_meta_data']['poll_url']
                logger.info(f"Poll URL: {poll_url}")
                bing_id = get_bing_id(poll_url)
                logger.info(f"Bing ID: {bing_id}")
                time.sleep(3)
                image_paths = _create_img(bing_id, save_path)
                logger.info(f"Image Paths: {image_paths}")
                return image_paths

            else:
                client.close()
                logger.error(f"Error: {response.status_code}, {response.text}")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise Exception(f"Error: {e}") from e


def _create_img(bing_id: str, save_path: str) -> list:
    """
    Generate image using Microsoft Designer API
    :param bing_id: Bing ID
    :return: Image Path
    """
    BING_URL = f'https://www.bing.com/images/create/async/results/{bing_id}'
    max_attempts = 5
    attempts = 0
    while attempts < max_attempts:
        with httpx.Client() as client:
            response = client.get(BING_URL, timeout=10)
            if response.status_code == 200:
                html = response.text
                if len(html) > 0:
                    logger.info(f"HTML: {html}")
                    urls = get_urls_from_html(html)
                    urls = clean_urls(urls)
                    image_paths = download_images(urls, save_path)
                    client.close()
                    return image_paths
                else:
                    logger.error(f"HTML length is 0, trying again... Attempt: {attempts}")
                    attempts += 1
                    time.sleep(3)  # Wait for 3 seconds before retrying
            else:
                logger.error(f"Error: {response.status_code}, {response.text}")
                attempts += 1
                time.sleep(3)  # Wait for 3 seconds before retrying

    raise Exception("Failed to get a successful response after 5 attempts")


def main():
    parser = argparse.ArgumentParser(description="Generate images using Microsoft Designer API")
    parser.add_argument("--user_id", help="User ID", required=True)
    parser.add_argument("--auth_token", help="Auth Token", required=True)
    parser.add_argument("--prompt", help="Prompt", required=True)
    parser.add_argument("--save_path", help="Save Path", required=False)
    parser.add_argument("--resolution", help="Resolution (1024x1024, 1024x1792, 1792x1024)", required=False)
    args = parser.parse_args()
    user_id = args.user_id
    auth_token = args.auth_token
    prompt = args.prompt
    save_path = args.save_path
    resolution = args.resolution

    if not args.user_id or not args.auth_token or not args.session_id or not args.prompt:
        logger.error(
            "Please provide all the required arguments. Run 'python -m microsoftdesigner --help' for more info.")
        sys.exit(1)
    create_img(user_id, auth_token, prompt, save_path, resolution)


if __name__ == "__main__":
    main()
