from pydantic import BaseModel
from typing import List, Optional

class SolanaSignInInput(BaseModel):
    domain: str
    account: Optional[str] = None
    statement: Optional[str] = None
    uri: str
    version: str = "1"
    chain: str
    nonce: str
    issuedAt: str
    expirationTime: Optional[str] = None
    notBefore: Optional[str] = None
    requestId: Optional[str] = None
    resources: Optional[List[str]] = None