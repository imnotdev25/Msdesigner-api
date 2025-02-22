import json
import random
import time

import httpx
from microsoftdesigner.constants import HEADERS, PARAMS, MS_BASE_URL, VALID_RESOLUTIONS
from microsoftdesigner.logger import logger
from microsoftdesigner.utils import download_images, get_random_boundary


def create_img(user_id: str, auth_token: str, prompt: str, *, save_path: str = 'images', resolution: str = '1024x1024',
               boost_count: int = 1, seed: int = None) -> list:
    """
    Generate image using Microsoft Designer API
    :param user_id: User ID
    :param auth_token: Auth Token ( Bearer ey... )
    :param prompt: Prompt
    :param save_path: Path to save generated images
    :param resolution: Resolution (1024x1024, 1024x1792, 1792x1024)
    :param boost_count: Boost count
    :param seed: Seed for reproducible generations (random if None)
    :return: List of image paths
    """
    if resolution not in VALID_RESOLUTIONS:
        raise ValueError(f"Invalid resolution. Must be one of: {', '.join(VALID_RESOLUTIONS)}")

    # Use random seed if none provided
    if seed is None:
        seed = random.randint(1, 10000)

    details = {'prompt': prompt, 'save_path': save_path, 'resolution': resolution, 'boost_count': boost_count,
        'seed': seed}

    logger.info(f"Generating image with details: {json.dumps(details, indent=2)}")

    # Initial request data format
    def create_form_data(boundary: str, prompt: str, resolution: str, boost_count: int, seed: int, *,
                         poll_url: str = None) -> str:

        data_parts = [('dalle-caption', prompt), ('dalle-scenario-name', 'TextToImage'), ('dalle-batch-size', '4'),
            ('dalle-last-prompt', ''), ('dalle-last-user-prompt', ''),
            ('dalle-image-response-format', 'UrlWithBase64Thumbnail'), ('dalle-seed', str(seed)),
            ('dalle-boost-count', str(boost_count)), ('ClientFlights', 'EnableBICForDALLEFlight'),
            ('dalle-hear-back-in-ms', '1000'), ('dalle-include-b64-thumbnails', 'true'),
            ('dalle-aspect-ratio-scaling-factor-b64-thumbnails', '0.3'), ('dalle-image-size', resolution), ]

        if poll_url:
            data_parts.append(('dalle-poll-url', poll_url))

        data = []
        for name, value in data_parts:
            data.append(f'------{boundary}')
            data.append(f'Content-Disposition: form-data; name="{name}"')
            data.append('')
            data.append(value)

        data.append(f'------{boundary}--')
        return '\r\n'.join(data)

    # Setup headers
    boundary = get_random_boundary()
    headers = HEADERS.copy()
    headers['Authorization'] = auth_token
    headers['UserId'] = user_id
    headers['Content-Type'] = f'multipart/form-data; boundary=----{boundary}'

    try:
        with httpx.Client() as client:
            # Initial request
            initial_data = create_form_data(boundary, prompt, resolution, boost_count, seed)
            response = client.post(MS_BASE_URL, params=PARAMS, data=initial_data, headers=headers, timeout=60)

            if response.status_code == 403:
                logger.error("Initial request failed with 403: Likely ran out of credits.")
                return []
            if response.status_code != 200:
                logger.error(f"Initial request failed: {response.status_code}, {response.text}")
                raise Exception(f"Failed to start generation. Status code: {response.status_code}")
            current_response = response.json()
            # Remove base64 thumbnail to reduce log size
            if 'image_urls_thumbnail' in current_response:
                for img in current_response['image_urls_thumbnail']:
                    if 'Thumbnail' in img:
                        img['Thumbnail'] = "[Base64 data removed]"
            # logger.debug(f"{} response data: {current_response}" if attempts == 0: "Initial" else "")

            max_attempts = 30
            attempts = 0

            while attempts < max_attempts:
                # Check for image URLs in current response
                if ('image_urls_thumbnail' in current_response and current_response['image_urls_thumbnail'] and len(
                    current_response['image_urls_thumbnail']) > 0):

                    image_urls = [img['ImageUrl'] for img in current_response['image_urls_thumbnail'] if
                                  img.get('ImageUrl')]

                    if image_urls:
                        logger.info(f"Found {len(image_urls)} images")
                        return download_images(image_urls, save_path, resolution)

                # Get polling interval from response
                poll_interval = 2.0  # default 2 seconds
                if ('polling_response' in current_response and 'polling_meta_data' in current_response[
                    'polling_response']):
                    poll_data = current_response['polling_response']['polling_meta_data']
                    poll_interval = poll_data.get('poll_interval', 2000) / 1000

                logger.info(f"Images not ready yet, attempt {attempts + 1}/{max_attempts}")
                attempts += 1
                time.sleep(poll_interval)

                # Create poll data with same format as initial request
                poll_boundary = get_random_boundary()
                poll_headers = headers.copy()
                poll_headers['Content-Type'] = f'multipart/form-data; boundary=----{poll_boundary}'

                poll_url = None
                if ('polling_response' in current_response and 'polling_meta_data' in current_response[
                    'polling_response']):
                    poll_url = current_response['polling_response']['polling_meta_data'].get('poll_url')

                poll_data = create_form_data(poll_boundary, prompt, resolution, boost_count, seed, poll_url=poll_url)

                # Make poll request
                response = client.post(MS_BASE_URL, params=PARAMS, data=poll_data, headers=poll_headers, timeout=60)

                if response.status_code != 200:
                    logger.error(f"Poll request failed: {response.status_code}, {response.text}")
                    raise Exception(f"Failed to poll. Status code: {response.status_code}")
                current_response = response.json()
                # Remove base64 thumbnail to reduce log size
                if 'image_urls_thumbnail' in current_response:
                    for img in current_response['image_urls_thumbnail']:
                        if 'Thumbnail' in img:
                            img['Thumbnail'] = "[Base64 data removed]"
                logger.info(f"Poll response data: {current_response}")

            raise Exception(f"Failed to get images after {max_attempts} attempts")

    except Exception as e:
        logger.error(f"Error during image generation: {str(e)}")
        raise Exception from e
