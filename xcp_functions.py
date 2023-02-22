import requests
import json

# See https://xchain.io/api 

def get_wallet_assets(address):
    url = f'https://xchain.io/api/balances/{address}'
    response = requests.get(url)
    if response.status_code == 200:
        balance_info = response.json()
        all_wallet_assets = []

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

# Fetch issuer value to see if owner issued token from /api/asset/{asset}
def get_asset_owner(asset):    
    url = f'https://xchain.io/api/asset/{asset}'
    response = requests.get(url)
    asset_description = {}

    if response.status_code == 200:
        asset_info = response.json()
#        print(f'Asset Name: {asset_info["asset"]}')
#        print(f'Estimated Value in USD: {asset_info["estimated_value"]["usd"]}')
#        print(f'Estimated Value in XCP: {asset_info["estimated_value"]["xcp"]}')
#        print(f'Issuer: {asset_info["issuer"]}')
#        print(f'Supply: {asset_info["supply"]}')
#        print(f'Owning Address: {asset_info["owner"]}')
#        print(f'Description: {asset_info["description"]}')
        asset_description = {
            'asset': asset_info["asset"],
            'description': asset_info["description"],
            'owner': asset_info["owner"]
        }
        return(asset_description)
    else:
        print(f'Error: {response.status_code} - {response.reason}')  
    

def get_open_dispenser(asset):
    url = f'https://xchain.io/api/dispensers/{asset}'
    response = requests.get(url)

    if response.status_code == 200:
        dispenser_info = response.json()

        for dispenser in dispenser_info['data']:
            if dispenser["status"] == "10" and dispenser["give_remaining"]  != "0":
                print(f'Asset: {dispenser["asset"]}')
                print(f'Give Quantity: {dispenser["give_quantity"]}')
                print(f'Give Remaining: {dispenser["give_remaining"]}')
                print(type({dispenser["give_remaining"]}))
                # give_int = int(dispenser["give_remaining"])
                # print(f'Give Remaining: {give_int}')
                print(f'Block Index: {dispenser["block_index"]}')
                print(f'Status: {dispenser["status"]}')
                print(f'Satoshi Rate: {dispenser["satoshirate"]}')
                print(f'Satoshi Price: {dispenser["satoshi_price"]}')
                print('\n')
    else:
        print(f'Error: {response.status_code} - {response.reason}')

def get_market_info(asset):
    url = f'https://xchain.io/api/orders/{asset}'
    response = requests.get(url)

    if response.status_code == 200:
        markets_info = response.json()

        for market in markets_info['data']:
            if market["status"] == "open":
                cost = market['give_quantity']
                print(f'You pay with: {asset}')
                print(f'COST: {cost}')
                print(f'You recieve: {market["get_asset"]}')
                print(f'YOU GET: {market["get_quantity"]}')
                print(f'Give Remaining: {market["give_remaining"]}')
                print(f'Block Index: {market["block_index"]}')
                print(f'Expire Index: {market["expire_index"]}')
                print(f'Status: {market["status"]}')
                print('\n')
    else:
        print(f'Error: {response.status_code} - {response.reason}')
    

# get_market_info('DANKROSECASH')
# get_market_info('PEPESABINA')
# #get_market_info('XCP')
# 
# get_open_dispenser('DANKROSECASH')
# get_open_dispenser('XCP')

# get_wallet_assets('1AwS3wRFNCoymKs69BXjAA4VfgWvuKvx4j')

check_address = '1AwS3wRFNCoymKs69BXjAA4VfgWvuKvx4j'

all_wallet_assets = get_wallet_assets(check_address)

# print(all_wallet_assets)
# print(json.dumps(all_wallet_assets, indent=4))
for asset_name in all_wallet_assets:
    asset = asset_name['asset']
    assets_owned_descriptions = get_asset_owner(asset)
    #print(json.dumps(assets_owned_descriptions, indent=4))
    if assets_owned_descriptions['owner'] == check_address:
        # print(json.dumps(assets_owned_descriptions, indent=4))
        if assets_owned_descriptions['description'].lower().endswith('.json'):
            description_url = assets_owned_descriptions['description']
            #print(description_url)
            response = requests.get(description_url)
            if response.status_code == 200:
                description_info = response.json()
                image_url = description_info['image_large']
                #print(image_url)
                data = {
                        "asset": asset,
                        "description_url": description_url,
                        "image_url": image_url
                    }
                #output.append(data)
                print(json.dumps(data))
                print('\n')
            else:
                print(f'Error: {response.status_code} - {response.reason}')

