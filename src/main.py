from fastapi import FastAPI, Depends, Request, Header, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from nacl.signing import VerifyKey, SignedMessage
from nacl.exceptions import BadSignatureError
from solders.pubkey import Pubkey
from typing import Annotated, List, Optional
from pydantic import BaseModel
import uvicorn
import base64
import json

import solana 

from src.models.solana_sign_in_input import SolanaSignInInput

import sys
import os
import dotenv

dotenv.load_dotenv()

app = FastAPI()

NONCES = {}



def check_address_nonce(solana_signin_input):
    # takes in the SolanaSignIn dict and checks to make sure the nonce isn't duped
    # if it isn't duped, add it to the dict to make sure that this current signin isn't duped
    if 'account' in solana_signin_input:
        account = solana_signin_input['account']
    else:
        account = None
        # sys.exit('something')
        return True
    nonce = solana_signin_input['nonce']

    if account in NONCES:
        #fail if nonce already here
        if nonce in NONCES['account']:
            return False

        NONCES['account'] = set(nonce)
    else:
        NONCES['account'].add(nonce)
    
    return True

class Creds(BaseModel):
    verify_key_str: str
    signed_message: str
    signed_signature: str

    class Config:
        arbitrary_types_allowed = True

def verify_valid_solana_address(address):
    try:
        b_address = bytes(address)
        Pubkey.from_bytes(b_address)
        return True 
    except:
        return False


# def verify_sig(verify_key_bytes, signed):
#     # Create a VerifyKey object from a hex serialized public key
#     verify_key = VerifyKey(verify_key_bytes)

#     verify_key.verify(signed)
#     return verify_key.verify(signed.message, signed.signature)


def verify_signature(auth: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        # Decode the public key and message from the token
        public_key_b64, signed_message_b64 = auth.credentials.split(".")

        # Decode the base64 encoded public key and signed message
        public_key_bytes = base64.urlsafe_b64decode(public_key_b64)
        signed_message = base64.urlsafe_b64decode(signed_message_b64)

        # Create a VerifyKey object using the public key bytes
        verify_key = VerifyKey(public_key_bytes)

        # Verify the message and return the original message
        message = verify_key.verify(signed_message)

        return message.decode()

    except (ValueError, BadSignatureError):
        raise HTTPException(
            # status_code=status.HTTP_401_UNAUTHORIZED,
            status_code=404,
            detail="Invalid authentication credentials",
        )    


def verify_header(authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        # Decode the public key and message from the token
        print(authorization.credentials)
        public_key_b64, signed_message_b64, signed_signature_b64 = authorization.credentials.split(".")

        # Decode the base64 encoded public key and signed message
        public_key_bytes = base64.urlsafe_b64decode(public_key_b64)
        signed_message = base64.urlsafe_b64decode(signed_message_b64)
        signed_signature = base64.urlsafe_b64decode(signed_signature_b64)

        # Create a VerifyKey object using the public key bytes
        verify_key = VerifyKey(public_key_bytes)

        # Verify the message and return the original message
        message = verify_key.verify(signed_message, signed_signature)

        return message.decode()

    except (ValueError, BadSignatureError):
        raise HTTPException(
            # status_code=status.HTTP_401_UNAUTHORIZED,
            status_code=401,
            detail="Invalid authentication credentials",
        )    

# def sign_in_with_solana(authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
#     try:
#         # Decode the public key and message from the token
#         print(authorization.credentials)
#         public_key_b64, signed_message_b64, signed_signature_b64 = authorization.credentials.split(".")

#         # Decode the base64 encoded public key and signed message
#         public_key_bytes = base64.urlsafe_b64decode(public_key_b64)
#         signed_message = base64.urlsafe_b64decode(signed_message_b64)
#         signed_signature = base64.urlsafe_b64decode(signed_signature_b64)

#         # Create a VerifyKey object using the public key bytes
#         verify_key = VerifyKey(public_key_bytes)

#         # Verify the message and return the original message
#         message = verify_key.verify(signed_message, signed_signature)

#         return message.decode()

#     except (ValueError, BadSignatureError):
#         raise HTTPException(
#             # status_code=status.HTTP_401_UNAUTHORIZED,
#             status_code=401,
#             detail="Invalid authentication credentials",
#         )

def sign_in_with_solana(
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    x_signature: Optional[str] = Header()
    
):
    try:
        # Decode the public key and message from the token
        print(authorization.credentials)
        public_key_b64, signed_message_b64, signed_signature_b64 = authorization.credentials.split(".")

        # Decode the base64 encoded public key and signed message
        public_key_bytes = base64.urlsafe_b64decode(public_key_b64)
        signed_message = base64.urlsafe_b64decode(signed_message_b64)
        signed_signature = base64.urlsafe_b64decode(signed_signature_b64)

        # Create a VerifyKey object using the public key bytes
        verify_key = VerifyKey(public_key_bytes)

        # Verify the message and return the original message
        message = verify_key.verify(signed_message, signed_signature)

        print("the dict: ")

        message_str = message.decode()
        print(eval(message_str))
        sign_in_information = eval(message_str)


        # Run through the expectations of inputs
        assert sign_in_information['domain'] == os.getenv('RPC_CLIENT'), ""
        if 'account' in sign_in_information:
            assert sign_in_information['account'] == public_key_bytes.decode(), "the public key does not match"
        
        assert sign_in_information['chain'] == os.getenv('CHAIN_ID'), "chain selection doesn't match"

        #TODO: Some sort of nonce storage to prevent replay
        assert check_address_nonce(sign_in_information), "tx nonce already used"

        assert verify_valid_solana_address(public_key_bytes), "not a valid public key"

        return  {
            "signature": message.decode(),
        }

    except (ValueError, BadSignatureError):
        raise HTTPException(
            # status_code=status.HTTP_401_UNAUTHORIZED,
            status_code=401,
            detail="Invalid authentication credentials",
        )    

    # TODO: checks
    # print('check signin header')
    # print(x_signature)
    # print(authorization)
    sig_decode = base64.b64decode(credentials.signed_message)


@app.get("/secure")
async def secure_route(token: Annotated[str, Depends(verify_signature)]):
    print(token)
    return {"message": "Secure route accessed", "token": token}


@app.get("/secure_header", dependencies=[Depends(verify_header)])
async def secure_route():
    return {"message": "Secure header accessed", "token": "token_placeholder"}


# @app.get("/sign-in-with-solana", dependencies=[Depends(sign_in_with_solana)])
@app.get("/sign-in-with-solana")
async def sign_in_with_solana(sol_headers: dict = Depends(sign_in_with_solana)): 
    # print(authorization)
    print(sol_headers['signature'])
    print(sol_headers)

    return None


# def poke(credentials: Annotated[Creds, Depends(verify_sig)]):
@app.post("/poke")
async def poke(credentials: Creds) -> bool:

    verify_key_bytes = base64.b64decode(credentials.verify_key_str)
    signed_message_bytes = base64.b64decode(credentials.signed_message)
    signed_signature_bytes = base64.b64decode(credentials.signed_signature)

    verify_key = VerifyKey(verify_key_bytes)
    
    try: 
        verify_key.verify(signed_message_bytes, signed_signature_bytes)
        return True
    except:
        return False




PORT = 3333
def start():
    uvicorn.run(
        "src.main:app", 
        # host="localhost", 
        port=PORT, 
        reload=True,
        server_header=False
    )