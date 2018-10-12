# API Readme
## Generate private key file
```bash
# write a new private key to a file called 'my_private_key'.
python api/generate_private_key.py my_private_key
```
## Generate an API token
```bash

# write a new token to a file called 'my_token'.
python api/generate_token.py my_private_key --output my_token
```
## Validate an API token
```bash

# validate the token contained in file 'my_token'.
python api/validate_token.py my_private_key my_token
```
## Run API server with token auth enabled
```bash

python api/api.py --port 5001 --key my_private_key
```
## Make authenticated API request with token
```python
import requests
resp = requests.get("http://localhost:5001")
print(resp.json())
```
