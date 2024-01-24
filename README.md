# Microsoft Designer API

### Installation

```bash pip3 install MicrosoftDesigner```

### Usage

``` 
$ python3 -m MicrosoftDesigner -h

options:
  -h, --help            show this help message and exit
  --user_id USER_ID     User ID
  --auth_token AUTH_TOKEN
                        Auth Token
  --session_id SESSION_ID
                        Session ID
  --prompt PROMPT       Prompt
  --save_path FILE_PATH
                        File Path to save the output (optional)
  --file_name FILE_NAME
                        File Name to save the output (optional)

```
## Getting Started
- Create a new user account or login [Microsoft Designer](https://designer.microsoft.com/)
- Open the developer tools and go to the network tab
- Create a new image using random text
- Find the request with post method and copy the request headers
- Copy the user id, auth token and session id from the request headers
- Run the script with the copied values

```
$ python3 -m MicrosoftDesigner --user_id <user_id> --auth_token <auth_token> --session_id <session_id> --prompt <prompt> --save_path <save_path> --file_name <file_name>

```
