import solana
from solders.keypair import Keypair
from nacl.signing import SigningKey, VerifyKey
from datetime import datetime, timedelta

import requests
import json
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey 
import base64

import sys
import os
from os.path import dirname
sys.path.append(dirname(os.getcwd() + '/src/models'))
sys.path.append('/src/models')
import src.models.solana_sign_in_input


from src.models.solana_sign_in_input import SolanaSignInInput

import os
import dotenv 


dotenv.load_dotenv()
signing_key = SigningKey.generate()

# Sign a message with the signing key

sign_in_dict = {
    "domain": os.getenv("RPC_CLIENT"),
    # "account": Optional[str]
    "statement": "Attack at Dawn",
    "uri": os.getenv('API_ENDPOINT'),
    "version": "1",
    "chain": os.getenv("CHAIN_ID"),
    "nonce": "1",
    "issuedAt": str(datetime.now()),
    "expirationTime": str(datetime.now() + timedelta(minutes = 10))

    # "notBefore": Optional[str]
    # "requestId": Optional[str]
    # "resources": Optional[List[str]]
}

test = SolanaSignInInput(
    
    domain = os.getenv("RPC_CLIENT"),
    statement = "Attack at Dawn",
    uri = os.getenv('API_ENDPOINT'),
    version = "1",
    chain = os.getenv("CHAIN_ID"),
    nonce = "1",
    issuedAt = str(datetime.now()),
    expirationTime = str(datetime.now() + timedelta(minutes = 10))
    
)


sign_in_with_solana_format = SolanaSignInInput(
    **sign_in_dict
)

# signed = signing_key.sign(b"Attack at Dawn")
b_signed = bytes(str(sign_in_dict), 'utf-8')
signed = signing_key.sign(b_signed)

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



url = os.getenv('API_ENDPOINT')
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'bearer {verify_key_str}.{signed_message_str}.{signed_signature_str}',
    'x-signature': f'{signed_message_str}'
}
response = requests.get(url, headers=headers)

response.text
# Handle response
if response.status_code == 200:
    print("Request successful!")
    print(response.json())
else:
    print(f"Request failed with status code {response.status_code}")




public_key_b64, signed_message_b64 = f'{verify_key_str}.{signed_message_str}'.split(".")

# Decode the base64 encoded public key and signed message
public_key_bytes = base64.b64decode(verify_key_str)
signed_message_bytes = base64.b64decode(signed_message_str)
signed_sig_bytes = base64.b64decode(signed_signature_str)

print(public_key_bytes)
print(signed_message_bytes)
# Create a VerifyKey object using the public key bytes
verify_key = VerifyKey(public_key_bytes)
print('vk')
print(verify_key)

# Verify the message and return the original message
message = verify_key.verify(signed_message_bytes, signed_sig_bytes)
message

verify_key.verify(signed_message_bytes)


if '' is not None:
    print('hello')