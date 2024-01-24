import argparse
import asyncio
import os
import random
import string
import sys
import time
from functools import partial
from typing import Union

from httpx import AsyncClient, Client

MS_BASE_URL = "https://designerapp.officeapps.live.com/designerapp/DallE.ashx"
HEADERS = {
    'authority': 'designerapp.officeapps.live.com',
    'accept': 'application/json, text/plain, */*',
    'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryzdakYnMWm0iQFcfO',
    'origin': 'https://designer.microsoft.com',
    'referer': 'https://designer.microsoft.com/',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',

}

PARAMS = {
    'action': 'GetDallEImagesCogSci'
}


def debug(debug_file, text_var):
    """helper function for debug"""
    with open(f"{debug_file}", "a", encoding="utf-8") as f:
        f.write(str(text_var))
        f.write("\n")


class CreateImg:
    def __init__(self, user_id: str, auth_token: str, session_id: str, debug_file: Union[str, None] = None, quiet: bool = False):
        self.user_id = user_id
        self.auth_token = auth_token
        self.session_id = session_id
        self.debug_file = debug_file
        self.headers = HEADERS
        self.client = Client(headers=self.headers)
        self.params = PARAMS
        self.url = MS_BASE_URL
        if self.debug_file:
            self.debug = partial(debug, self.debug_file)
        self.quiet = quiet

    def gen_images(self, prompt: str) -> str:
        if not self.quiet:
            print("Sending request to Microsoft Designer API...")
        if self.debug_file:
            self.debug("Sending request to Microsoft Designer API...")

        try:
            data = f'------WebKitFormBoundaryzdakYnMWm0iQFcfO\r\nContent-Disposition: form-data; name="dalle-caption"\r\n\r\n{prompt}\r\n------WebKitFormBoundaryzdakYnMWm0iQFcfO\r\nContent-Disposition: form-data; name="dalle-scenario-name"\r\n\r\nTextToImage\r\n------WebKitFormBoundaryzdakYnMWm0iQFcfO\r\nContent-Disposition: form-data; name="dalle-batch-size"\r\n\r\n1\r\n------WebKitFormBoundaryzdakYnMWm0iQFcfO\r\nContent-Disposition: form-data; name="dalle-image-response-format"\r\n\r\nUrlWithBase64Thumbnail\r\n------WebKitFormBoundaryzdakYnMWm0iQFcfO\r\nContent-Disposition: form-data; name="dalle-seed"\r\n\r\n112\r\n------WebKitFormBoundaryzdakYnMWm0iQFcfO--\r\n'
            headers = self.headers
            headers['userid'] = self.user_id
            headers['authorization'] = self.auth_token
            headers['sessionid'] = self.session_id
            response = self.client.post(
                self.url,
                params=self.params,
                data=data,
                timeout=60,
            )
            if not self.quiet:
                print(f"Response: {response.status_code}")
            if self.debug_file:
                self.debug(f"Response: {response.status_code}")
            if response.status_code == 200:
                img = response.json()['image_urls_thumbnail'][0]['ImageUrl']
                self.client.close()
                return img
            else:
                return f"Something went wrong. Please try again later. Error::: {response} \n If you think this is a bug, please report it at github.com/imnotdev25/Msdesigner-api/issues"
        except Exception as e:
            if not self.quiet:
                print(f"Error: {e}")
            if self.debug_file:
                self.debug(f"Error: {e}")
            return f"Something went wrong. Please try again later. Error::: {e} \n If you think this is a bug, please report it at github.com/imnotdev25/Msdesigner-api/issues"

    def save_images(self,
                    link: str,
                    save_path: str,
                    file_name: str) -> None:
        if not self.quiet:
            print("Saving image...")
        if self.debug_file:
            self.debug("Saving image...")

        try:
            fn = f"{file_name}" if file_name else f"{int(time.time())}.png"
            path = f"{save_path}" if save_path else os.mkdir("images")
            response = self.client.get(link)
            if response.status_code == 200:
                with open(f"{path}/{fn}", "wb") as f:
                    f.write(response.content)
                    f.close()
                    self.debug(f"Image saved at {os.path.abspath(f.name)}")
            else:
                if not self.quiet:
                    print(f"Something went wrong. Please try again later. Error::: {response}")
                if self.debug_file:
                    self.debug(f"Something went wrong. Please try again later. Error::: {response}")
        except Exception as e:
            if not self.quiet:
                print(f"Error while saving image.{e}")
            if self.debug_file:
                self.debug(f"Error while saving image: {e}")


class CreateImgAsync(CreateImg):
    def __init__(self, user_id: str, auth_token: str, session_id: str, debug_file: Union[str, None] = None,
                 quiet: bool = False):
        super(CreateImg, self).__init__(user_id, auth_token, session_id, debug_file, quiet)
        self.client = AsyncClient(headers=self.headers)
        self.url = MS_BASE_URL
        if self.debug_file:
            self.debug = partial(debug, self.debug_file)

    async def async_gen_images(self, prompt: str) -> str:
        if not self.quiet:
            print("Sending request to Microsoft Designer API...")
        if self.debug_file:
            self.debug("Sending request to Microsoft Designer API...")

        try:
            data = f'------WebKitFormBoundaryzdakYnMWm0iQFcfO\r\nContent-Disposition: form-data; name="dalle-caption"\r\n\r\n{prompt}\r\n------WebKitFormBoundaryzdakYnMWm0iQFcfO\r\nContent-Disposition: form-data; name="dalle-scenario-name"\r\n\r\nTextToImage\r\n------WebKitFormBoundaryzdakYnMWm0iQFcfO\r\nContent-Disposition: form-data; name="dalle-batch-size"\r\n\r\n1\r\n------WebKitFormBoundaryzdakYnMWm0iQFcfO\r\nContent-Disposition: form-data; name="dalle-image-response-format"\r\n\r\nUrlWithBase64Thumbnail\r\n------WebKitFormBoundaryzdakYnMWm0iQFcfO\r\nContent-Disposition: form-data; name="dalle-seed"\r\n\r\n112\r\n------WebKitFormBoundaryzdakYnMWm0iQFcfO--\r\n'
            headers = self.headers
            headers['userid'] = self.user_id
            headers['authorization'] = self.auth_token
            headers['sessionid'] = self.session_id
            response = await self.client.post(
                self.url,
                params=self.params,
                data=data,
                timeout=60,
            )
            if not self.quiet:
                print(f"Response: {response.status_code}")
            if self.debug_file:
                self.debug(f"Response: {response.status_code}")
            if response.status_code == 200:
                img = response.json()['image_urls_thumbnail'][0]['ImageUrl']
                await self.client.aclose()
                return img
            else:
                return f"Something went wrong. Please try again later. Error::: {response} \n If you think this is a bug, please report it at github.com/imnotdev25/Msdesigner-api/issues"
        except Exception as e:
            if not self.quiet:
                print(f"Error: {e}")
            if self.debug_file:
                self.debug(f"Error: {e}")
            return f"Something went wrong. Please try again later."

    async def async_save_images(self,
                                link: str,
                                save_path: str,
                                file_name: str) -> None:
        if not self.quiet:
            print("Saving image...")
        if self.debug_file:
            self.debug("Saving image...")

        try:
            fn = f"{file_name}" if file_name else f"{int(time.time())}.png"
            path = f"{save_path}" if save_path else os.mkdir("images")
            response = await self.client.get(link)
            if response.status_code == 200:
                with open(f"{path}/{fn}", "wb") as f:
                    f.write(response.content)
                    f.close()
                    self.debug(f"Image saved at {os.path.abspath(f.name)}")
            else:
                if not self.quiet:
                    print(f"Something went wrong. Please try again later. Error::: {response}")
                if self.debug_file:
                    self.debug(f"Something went wrong. Please try again later. Error::: {response}")

        except Exception as e:
            if not self.quiet:
                print(f"Error while saving image.{e}")
            if self.debug_file:
                self.debug(f"Error while saving image: {e}")


def main():
    parser = argparse.ArgumentParser(description="Generate images using Microsoft Designer API")
    parser.add_argument("--user_id", help="User ID", required=True)
    parser.add_argument("--auth_token", help="Auth Token", required=True)
    parser.add_argument("--session_id", help="Session ID", required=True)
    parser.add_argument("--prompt", help="Prompt", required=True)
    parser.add_argument("--save_path", help="Save Path", required=False)
    parser.add_argument("--file_name", help="File Name", required=False)
    parser.add_argument("--debug_file", help="Debug File", required=False)
    parser.add_argument("--quiet", help="Quiet", required=False)
    args = parser.parse_args()
    user_id = args.user_id
    auth_token = args.auth_token
    session_id = args.session_id
    prompt = args.prompt
    save_path = args.save_path
    file_name = args.file_name
    debug_file = args.debug_file
    quiet = args.quiet
    if quiet:
        quiet = True
    else:
        quiet = False
    if debug_file:
        debug_file = debug_file
    else:
        debug_file = None
    if save_path:
        save_path = save_path
    else:
        save_path = "images"
    if file_name:
        file_name = file_name
    else:
        file_name = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(5))

    if not args.user_id or not args.auth_token or not args.session_id or not args.prompt:
        print("Please provide all the required arguments.")
        sys.exit(1)

    if not args.asyncio:
        image_generator = CreateImg(user_id, auth_token, session_id, debug_file, quiet)
        image_link = image_generator.gen_images(prompt)
        image_generator.save_images(image_link, save_path, file_name)
    else:
        image_generator = CreateImgAsync(user_id, auth_token, session_id, debug_file, quiet)
        image_link = asyncio.run(image_generator.async_gen_images(prompt))
        asyncio.run(image_generator.async_save_images(image_link, save_path, file_name))


if __name__ == "__main__":
    main()
