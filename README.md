# solana-as-api

This repo provides references for a few simple flows

1. Body signature
    1. Sign a message with your solana keys client side 
    2. Add the message into the body of an API request
    3. Verify the signature 
2. Header Sig
    1. Same as body signature, except the authorization token is within the headers - "Authorization: bearer \<token\>"

https://github.com/Tamgros/solana-as-api/blob/1ec3e438774cdf3f7bf2558b2a975cf8b0dae098/make_signed_header.py#L40

3. Oauth type flow (pictured below)
    1. Send tx to Solana
        * this could include a value transfer
    2. recieve the tx hash back
    3. Send tx hash to server signed to show the api request was made by the same entity that submitted the Solana tx
    * This is a great use case for Solana because 
        * latency really affects UX 
        * Tx finality is important because an off protocol API response will be triggered. A rollback would be bad



![alt text](https://github.com/Tamgros/solana-as-api/blob/solana_package/assets/1_WP1iB-f6lJl_4YsvTsw2Og.png)


Get all NFTs from a wallet
https://solanacookbook.com/references/nfts.html#candy-machine-v1

solana-keygen new --outfile ~/.config/solana/burner3.json

https://developer.token.io/seasons_rest_api_doc/content/e-rest/jwt_auth.htm