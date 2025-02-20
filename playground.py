import os
from typing import Dict, Literal
from microsoftdesigner.gen_images import create_img
from dotenv import load_dotenv

load_dotenv()

ResolutionType = Literal['square', 'widescreen', 'portrait']

RESOLUTIONS: Dict[ResolutionType, str] = {
    'square': '1024x1024',
    'portrait': '1024x1792', 
    'widescreen': '1792x1024'  # Fixed typo in 'portrait'
}

ACTIONS = [
    "sitting",
    "riding",
    "laying",
]

PROMPTS = [f"anime girl {action} on an exercise ball in a room with exercise balls" for action in ACTIONS ]

DEFAULT_NUM_IMAGES = 40

def generate_images(
    prompt: str,
    resolution_type: ResolutionType = 'widescreen',
) -> None:
    """
    Generate images using Microsoft Designer API.
    
    Args:
        prompt: The text prompt for image generation
        resolution_type: Type of resolution from RESOLUTIONS
        num_images: Number of images to generate
    """
    user_id = os.getenv("USER_ID")
    auth_token = os.getenv("AUTH_TOKEN")

    if not user_id or not auth_token:
        raise ValueError("USER_ID and AUTH_TOKEN must be set in .env file")
    
    # for _ in range(num_images):
    resolution = RESOLUTIONS[resolution_type]
    create_img(user_id, auth_token, prompt, resolution=resolution)

if __name__ == "__main__":
    prompt = PROMPTS[1]
    generate_images(prompt)
