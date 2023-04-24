import solana
from solders.keypair import Keypair
from solana.rpc.async_api import AsyncClient
from solana.rpc.api import Client
from solana.transaction import Transaction
from solders.system_program import TransferParams, transfer

from nacl.signing import SigningKey, VerifyKey

import requests
import json
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey 
import base64

from dotenv import load_dotenv
import os

import asyncio


load_dotenv()

RPC_CLIENT = os.getenv('RPC_CLIENT')
KEPAIR_PATH = os.getenv('KEYPAIR_PATH')

with open(KEYPAIR_PATH, "r") as json_file:
    sender_json = json.load(json_file)
    sender_private_bytes = bytes(sender_json)
    sender = Keypair.from_bytes(sender_private_bytes)


with open('/Users/mattsorg/.config/solana/burner3.json', "r") as json_file:
    reciever_json = json.load(json_file)
    reciever_private_bytes = bytes(reciever_json)
    reciever = Keypair.from_bytes(reciever_private_bytes)









async def main():
    async with AsyncClient(RPC_CLIENT) as client:
        res = await client.is_connected()
    print(res)  # True

    # sender, receiver = Keypair.from_seed(leading_zeros + [1]), Keypair.from_seed(leading_zeros + [2])

    txn = solana.transaction.Transaction().add(transfer(TransferParams(
    from_pubkey=sender.pubkey(), to_pubkey=receiver.pubkey(), lamports=1000)))

    client.send_transaction(txn, sender).value
    Signature(
        1111111111111111111111111111111111111111111111111111111111111111,
    )




from solana.transaction import Keypair
import json

# Create a new keypair
KEYPAIR_PATH='/Users/mattsorg/.config/solana/burner.json'



with open(KEYPAIR_PATH, "r") as json_file:
    keypair_data = json.load(json_file)

private_key_bytes = bytes(keypair_data["privateKey"])
keypair = Keypair.from_bytes(private_key_bytes)

kpfj = Keypair.from_json(json.loads(f.read()))

bytes.fromhex()

# Get the private key as raw bytes
private_key_bytes = keypair.secret_key

# Convert raw bytes to hexadecimal string
private_key_hex = private_key_bytes.hex()

# Convert raw bytes to Base58 string
private_key_base58 = keypair.secret_key_base58()

# Convert back from hexadecimal string to raw bytes
private_key_bytes_from_hex = bytes.fromhex(private_key_hex)

# Convert back from Base58 string to raw bytes
private_key_bytes_from_base58 = Keypair.from_secret_key(private_key_base58).secret_key

# Verify conversions
assert private_key_bytes == private_key_bytes_from_hex
assert private_key_bytes == private_key_bytes_from_base58

# Print the different formats
print("Private key as raw bytes:", private_key_bytes)
print("Private key as hexadecimal string:", private_key_hex)
print("Private key as Base58 string:", private_key_base58)



with open('/Users/mattsorg/.config/solana/burner3.json', "r") as json_file:
    reciever_json = json.load(json_file)

reciever_private_bytes = bytes(reciever_json)
reciever = Keypair.from_bytes(reciever_private_bytes)