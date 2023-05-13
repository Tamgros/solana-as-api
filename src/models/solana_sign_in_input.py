from pydantic import BaseModel
from typing import List, Optional

class SolanaSignInInput(BaseModel):
    domain: str
    account: Optional[str]
    statement: Optional[str]
    uri: str
    version: str = "0.1.0"
    chain: str
    nonce: str
    issuedAt: str
    expirationTime: Optional[str]
    notBefore: Optional[str]
    requestId: Optional[str]
    resources: Optional[List[str]]