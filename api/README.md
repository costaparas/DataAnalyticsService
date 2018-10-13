# API readme
## Introduction
The API server has token authentication enabled.
To run the API server a private key file is required.

## Generate private key file
```bash
# write a new private key to a file called 'my_private_key'.
python generate_private_key.py my_private_key
```
## Run API server
```bash
#Run API server on port 5001, using 'my_private_key' as the private key file.
python api.py --port 5001 my_private_key

#Optionally, enable debugging...
python api.py --port 5001 --debug my_private_key
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
