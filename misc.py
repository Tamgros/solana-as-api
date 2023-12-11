from solders.pubkey import Pubkey
from nacl.signing import SigningKey

sk = SigningKey.generate()

bsk = bytes(sk)

Pubkey.from_bytes(bsk)

Pubkey.from_bytes(b'bullshit')