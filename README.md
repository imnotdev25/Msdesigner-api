# Microsoft Designer API

A Python library for generating images using Microsoft Designer's API.

### Installation

```bash
pip install microsoftdesigner
```

### Configuration

Create a `.env` file in your project root with:

```env
USER_ID=your_user_id_here
AUTH_TOKEN=your_auth_token_here
```

### Command Line Usage

```bash
python -m microsoftdesigner --help

options:
  -h, --help            show this help message and exit
  --user_id USER_ID     User ID (or set MSDESIGNER_USER_ID env var)
  --auth_token AUTH_TOKEN
                        Authentication token (or set MSDESIGNER_AUTH_TOKEN env var)
  --prompt PROMPT       Image generation prompt
  --save_path SAVE_PATH
                        Path to save generated images (default: images)
  --resolution {1024x1024,1024x1792,1792x1024}
                        Image resolution (default: 1024x1024)
  --boost_count BOOST_COUNT
                        Boost count for generation quality (default: 1)
  --seed SEED          Random seed for reproducible results (optional)
```

### Python Usage

Basic example:
```python
from microsoftdesigner.gen_images import create_img
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

# Get credentials from environment
user_id = os.getenv("USER_ID") 
auth_token = os.getenv("AUTH_TOKEN")

# Generate images
image_paths = create_img(
    user_id=user_id,
    auth_token=auth_token,
    prompt="a beautiful sunset over mountains",
    save_path="images",      # Optional: defaults to 'images'
    resolution="1024x1024",  # Optional: 1024x1024, 1024x1792, 1792x1024
    boost_count=1,          # Optional: enhance generation quality (default: 1)
    seed=42                 # Optional: set for reproducible results
)

# Example output: list of paths like
# ['images/1024x1024/123e4567-e89b-12d3-a456-426614174000.jpg',
#  'images/1024x1024/987fcdeb-51d3-12d3-a456-426614174000.jpg', ...]
print(f"Generated images saved to: {image_paths}")
```

## Getting Started

1. Create/login to your [Microsoft Designer](https://designer.microsoft.com/) account
2. Open browser developer tools (F12) and go to Network tab
3. Generate an image using any prompt in Microsoft Designer
4. In the Network tab, find the POST request to `/DallE.ashx`
5. From the request headers, copy:
   - `UserId` header value → set as USER_ID
   - `Authorization` header value → set as AUTH_TOKEN
6. Save these values in your .env file or pass them directly to the API

### Important Notes

- **Authentication**: Auth tokens expire after 24 hours - you'll need to refresh them
- **Resolutions**: Only use supported resolutions:
  - Square: 1024x1024
  - Portrait: 1024x1792
  - Widescreen: 1792x1024
- **File Organization**: Generated images are automatically saved in resolution-specific subfolders:
  ```
  images/
  ├── 1024x1024/
  ├── 1024x1792/
  └── 1792x1024/
  ```
- **Error Handling**: The API will return an empty list if you've run out of credits (403 error)

