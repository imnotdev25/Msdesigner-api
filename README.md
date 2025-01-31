# Microsoft Designer API

### Installation

```$ pip3 install MicrosoftDesigner```

### Usage

``` 
$ python3 -m MicrosoftDesigner -h

options:
  -h, --help            show this help message and exit
  --user_id USER_ID     User ID
  --auth_token AUTH_TOKEN
                        Auth Token
  --prompt PROMPT       Prompt
  --save_path FILE_PATH
                        File Path to save the output (optional)
  --file_name FILE_NAME
                        File Name to save the output (optional)
  --resolution RESOLUTION
                        Resolution of the image (optional)
                        (default: 1024x1024, available: 1024x1792, 1792x1024)

```
## Getting Started
- Create a new user account or login [Microsoft Designer](https://designer.microsoft.com/)
- Open the developer tools and go to the network tab
- Create a new image using random text
- Find the request with post method and copy the request headers
- Copy the user id, auth token (Authorization: value) from the request headers
- Run the script with the copied values
- Note: **auth_token will expire after 24 hours**
- Note: **Do not pass resolution other than 1024x1024, 1024x1792, 1792x1024**

```
$ python3 -m MicrosoftDesigner --user_id <user_id> --auth_token <auth_token> --prompt <prompt> --resolution <resolution> --save_path <save_path>

```
### **Python Example**

```

from ssdesigner.gen_images import create_image
create_image(user_id, auth_token, prompt, resolution)

# Image wiil be saved in images folder


```

