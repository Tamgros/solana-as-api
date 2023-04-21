from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import JWTError, jwt
# from passlib.context import CryptContext
from pydantic import BaseModel
from nacl.signing import SigningKey

# ALGORITHM = "EdDSA"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
signing_key = SigningKey.generate()

class Token(BaseModel):
    access_token: str
    token_type: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

data = {
    "sub": "user",
    "exp": datetime.utcnow() + ACCESS_TOKEN_EXPIRE_MINUTES
}
}


to_encode = data.copy()
if expires_delta:
    expire = datetime.utcnow() + expires_delta
else:
    expire = datetime.utcnow() + timedelta(minutes=15)
to_encode.update({"exp": expire})
# encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
encoded_jwt = signing_key.sign(to_encode.encode())

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    # encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    encoded_jwt = signing_key.sign(to_encode.encode())
    return encoded_jwt