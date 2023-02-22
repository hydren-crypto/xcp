import requests
import json
import convertapi
import os
import argparse

convertapi.api_secret = os.environ.get('CONVERTAPI_API_SECRET')
print(f'Convert API Secret: {convertapi.api_secret}')

def get_wallet_assets(address):
    print(f'Fetching Wallet Assets for {address} - step 0')
    url = f'https://xchain.io/api/balances/{address}'
    response = requests.get(url)
    if response.status_code == 200:
        balance_info = response.json()
        all_wallet_assets = []
        print(f'Fetching Wallet Assets for {address}')

        for balance in balance_info['data']:
            asset = {
                'asset': balance['asset'],
                'quantity': balance['quantity'],
                'asset_longname': balance['asset_longname'],
                'description': balance['description'],
            }
            all_wallet_assets.append(asset)
        return all_wallet_assets
    else:
        print(f'Error: {response.status_code} - {response.reason}')

def get_asset_owner(asset):    
    url = f'https://xchain.io/api/asset/{asset}'
    response = requests.get(url)
    asset_description = {}

    if response.status_code == 200:
        asset_info = response.json()
        asset_description = {
            'asset': asset_info["asset"],
            'description': asset_info["description"],
            'owner': asset_info["owner"]
        }
        return(asset_description)
    else:
        print(f'Error: {response.status_code} - {response.reason}')  

def get_description_urls(check_address):
    # This fetches the description JSON and parses out the image_url field
    all_wallet_assets = get_wallet_assets(check_address)
    output = []
    print(f'Check if Wallet Owner is Owner of Asset')
    for asset_name in all_wallet_assets:
        asset = asset_name['asset']
        assets_owned_descriptions = get_asset_owner(asset)

        if assets_owned_descriptions['owner'] == check_address:
            if assets_owned_descriptions['description'].lower().endswith('.json'):
                description_url = assets_owned_descriptions['description']
                response = requests.get(description_url)
                if response.status_code == 200:
                    description_info = response.json()
                    image_url = description_info['image_large']
                    asset_desc_img_url = {
                            "asset": asset,
                            "description_url": description_url,
                            "image_url": image_url
                        }
                    output.append(asset_desc_img_url)
                    print(json.dumps(asset_desc_img_url))
                    # print('\n')
                else:
                    print(f'Error: {response.status_code} - {response.reason}')
    # Save the output to a JSON file
    with open('asset_desc_img_url.json', 'w') as outfile:
        json.dump(asset_desc_img_url, outfile)
    return output

def save_images(asset_desc_img_urls):
    if not os.path.exists('images'):
        os.mkdir('images')
    for asset_desc_img_url in asset_desc_img_urls:
        # separate the asset value and image_url value
        asset = asset_desc_img_url['asset']
        image_url = asset_desc_img_url['image_url']
        image_filename = image_url.rsplit('/', 1)[1]
        full_filename = asset + '-' + image_filename
        with open('images/' + full_filename, 'wb') as f:
            f.write(requests.get(image_url).content)
    files = os.listdir('images')

    for file in files:
        # get the full filename
        print(f'Processing: {file}')
        full_filename = os.path.join('images', file)

        # get the file extension from the filename
        file_extension = file.rsplit('.', 1)[1]

        # convert the file to webp
        convertapi.convert('webp', {'File': full_filename}, from_format=file_extension).save_files('images')

def main():
    # Define parser and add arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--wallet', help='The wallet address to check')

    # Parse arguments
    args = parser.parse_args()

    # Assign arguments to variables
    check_address = args.wallet

    # check_address = '1AwS3wRFNCoymKs69BXjAA4VfgWvuKvx4j'
    print(f'Checking address: {check_address} for assets')
    asset_desc_img_urls = get_description_urls(check_address)
    print(f'Preparing for image download and conversion')
    # print(json.dumps(asset_desc_img_urls, indent=4))
    save_images(asset_desc_img_urls)

if __name__ == '__main__':
    main()