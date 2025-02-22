import argparse
import os
import sys
from venv import logger

from dotenv import load_dotenv
from microsoftdesigner.constants import VALID_RESOLUTIONS
from microsoftdesigner.gen_images import create_img

load_dotenv()

parser = argparse.ArgumentParser(description="Generate images using Microsoft Designer API")
parser.add_argument("--user_id", required=False, help="User ID", default=os.getenv("MSDESIGNER_USER_ID"), )
parser.add_argument("--auth_token", required=False, help="Authentication token",
    default=os.getenv("MSDESIGNER_AUTH_TOKEN"), )
parser.add_argument("--prompt", required=True, help="Image generation prompt")
parser.add_argument("--save_path", default="images", help="Path to save generated images")
parser.add_argument("--resolution", default="1024x1024", choices=VALID_RESOLUTIONS, help="Image resolution", )
parser.add_argument("--boost_count", type=int, default=1, help="Boost count")
parser.add_argument("--seed", type=int, default=None,
    help="Seed for reproducible generations (random if not provided)", )

args = parser.parse_args()

user_id = args.user_id
auth_token = args.auth_token

if not user_id:
    parser.error("Please provide --user_id argument or set MSDESIGNER_USER_ID environment variable.")
if not auth_token:
    parser.error("Please provide --auth_token argument or set MSDESIGNER_AUTH_TOKEN environment variable.")

try:
    image_paths = create_img(user_id, auth_token, args.prompt, save_path=args.save_path, resolution=args.resolution,
        boost_count=args.boost_count, seed=args.seed, )
    logger.info(f"Generated images saved to: {image_paths}")
except Exception as e:
    logger.error(f"Failed to generate images: {str(e)}")
    sys.exit(1)
