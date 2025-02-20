import uuid

# Base URL for Microsoft Designer's DALL-E API
MS_BASE_URL = "https://designerapp.officeapps.live.com/designerapp/DallE.ashx"

# Default headers for API requests
HEADERS = {
    'Host': 'designerapp.officeapps.live.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://designer.microsoft.com/',
    'ClientId': f'{str(uuid.uuid4())}',
    'ContainerId': f'{str(uuid.uuid4())}',
    'SessionId': f'{str(uuid.uuid4())}',
    'HostApp': 'DesignerApp',
    'ClientName': 'DesignerApp',
    'Origin': 'https://designer.microsoft.com',
    'Connection': 'keep-alive',
    'FileToken': f'{str(uuid.uuid4())}',
}

# Query parameters for the API endpoint
PARAMS = {'action': 'GetDallEImagesCogSci'}

# Valid resolutions
VALID_RESOLUTIONS = {'1024x1024', '1024x1792', '1792x1024'}