# API readme
## Introduction
The API server supports token authentication.
## Generate private key file
```bash
# write a new private key to a file called 'my_private_key'.
python generate_private_key.py my_private_key
```
## Generate an API token
```bash

# write a new token to a file called 'my_token'.
python generate_token.py my_private_key --output my_token
```
```bash

# optionally specify a token lifetime

# generate a token valid for 3600 seconds (1 hour)
python generate_token.py my_private_key --output my_token --lifetime 3600
```
## Validate an API token
```bash

# validate the token contained in file 'my_token'.
python validate_token.py my_private_key my_token
```
## Run API server with token auth enabled
```bash

python api.py --port 5001 --key my_private_key
```
## Make authenticated API request with token
```python
# python
import requests
resp = requests.get("http://localhost:5001/movies")
print(resp.json())
```
