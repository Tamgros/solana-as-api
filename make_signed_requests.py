import solana
from solders.keypair import Keypair
from nacl.signing import SigningKey, VerifyKey

import requests
import json
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey 
import base64

from dotenv import load_dotenv
import os

import asyncio
from solana.rpc.async_api import AsyncClient

load_dotenv()

RPC_CLIENT = os.getenv('RPC_CLIENT')

# https://pynacl.readthedocs.io/en/latest/signing/
# Generate a new random signing key
signing_key = SigningKey.generate()

# Sign a message with the signing key
signed = signing_key.sign(b"Attack at Dawn")


# Encode byte data to a base64 string
signed_str = base64.b64encode(signed).decode('utf-8')
signing_key_bytes = signing_key.verify_key.encode()
verify_key_str = base64.b64encode(signing_key_bytes).decode('utf-8')
signed_message_str = base64.b64encode(signed.message).decode('utf-8')
signed_signature_str = base64.b64encode(signed.signature).decode('utf-8')

# Create JSON object with the encoded byte data
json_data = {
    'verify_key_str': verify_key_str,
    'signed_message': signed_message_str,
    'signed_signature': signed_signature_str
}


# Convert JSON object to string
json_string = json.dumps(json_data)



url = 'http://localhost:3333/poke'
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data=json_string, headers=headers)

response.text
# Handle response
if response.status_code == 200:
    print("Request successful!")
    print(response.json())
else:
    print(f"Request failed with status code {response.status_code}")

verify_key_bytes = base64.b64decode(verify_key_str)
signed_message_bytes = base64.b64decode(signed_message_str)
signed_signature_bytes = base64.b64decode(signed_signature_str)

verify_key = VerifyKey(verify_key_bytes)

verify_key.verify(signed_message_bytes, signed_signature_bytes)


url_secure = 'http://localhost:3333/secure'
response_secure = requests.get(url_secure, data=json_string, headers=headers)

response_secure.text
# Handle response_secure
if response_secure.status_code == 200:
    print("Request successful!")
    print(response_secure.json())
else:
    print(f"Request failed with status code {response.status_code}")