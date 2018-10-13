# API readme
## Introduction
The API server can be run with token authentication enabled or disabled.
To run the API server with auth enabled, a private key file is required.

## Generate private key file
```bash
# write a new private key to a file called 'my_private_key'.
python generate_private_key.py my_private_key
```
## Run API server
```bash
python api.py --port 5001 my_private_key
```
## Generate an API token
```python
import requests
resp = requests.post("/token/generate", data={
    "username": "user",
    "password": "test1",
})
if resp.status_code == 201:
    token = resp.json["token"]
```
## Validate an API token
## Make authenticated API request with token
```python
# python
import requests
resp = requests.get("http://localhost:5001/movies")
print(resp.json())
```
