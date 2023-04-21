from fastapi import FastAPI, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from nacl.signing import VerifyKey, SignedMessage
from nacl.exceptions import BadSignatureError
from typing import Annotated
from pydantic import BaseModel
import uvicorn
import base64
import json

app = FastAPI()


class Creds(BaseModel):
    verify_key_str: str
    signed_message: str
    signed_signature: str

    class Config:
        arbitrary_types_allowed = True


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
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )    


@app.get("/secure")
async def secure_route(token: str = Depends(verify_signature)):
    return {"message": "Secure route accessed", "token": token}



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