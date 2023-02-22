
**goal 1**

find which assets are listed as ORDERS for cards that are NOT XCP or BITCOIN

XCP and BTC dispenser to dex arb


**goal 2**

pull down a specified wallets assets, look at those assets to determine if the wallet owner owns the asset.
If so, fetch the assets description field and look for a json file, and extract the image_large value. 

Example:

Asset Name: BITMAPWOJAK
Description: 'https://easyasset.art/j/w5t4md/BITMAPWOJAK.json' 
BITMAPWOJACK { "image_large": "https://arweave.net/jB6kA6ksfVx65iqJKXkpjRcADDRQnk-neStaT1LjOW4/w5t4md_image.png" }

We will then push the image to compress or die for conversion to webp format, and then inscribe the webp asset. 

The next phase will be to rewrite the description URL on the input asset with the description for the inscription.