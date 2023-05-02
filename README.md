# solana-as-api

This repo provides references for a few simple flows

1. Body signature
    1. Sign a message with your solana keys client side 
    2. Add the message into the body of an API request
    3. Verify the signature 

https://github.com/Tamgros/solana-as-api/blob/7b92f1756aea0d15433fa94d3d7705d53323fe03/make_signed_requests.py#L37-L41

2. Header Sig
    1. Same as body signature, except the authorization token is within the headers - "Authorization: bearer \<token\>"

https://github.com/Tamgros/solana-as-api/blob/7b92f1756aea0d15433fa94d3d7705d53323fe03/make_signed_header.py#L40-L43

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

Next steps, TODOs:
* JWT type format
* token gating flow
    * Some tokens represent different rate limits. How do you queue if there is ever a capacity reached?
    * AMM?
* Token tx flow
* Utilize the usage field of NFTs for access rights
