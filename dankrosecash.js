import requests

asset = 'DANKROSECASH'
url = f'https://xchain.io/api/asset/{asset}'
response = requests.get(url)
if response.status_code == 200:
    asset_info = response.json()
    print(f'Asset Name: {asset_info["asset"]}')
    print(f'Estimated Value in USD: {asset_info["estimated_value"]["usd"]}')
    print(f'Estimated Value in XCP: {asset_info["estimated_value"]["xcp"]}')
    print(f'Issuer: {asset_info["issuer"]}')
    print(f'Supply: {asset_info["supply"]}')
else:
    print(f'Error: {response.status_code} - {response.reason}')

url = f'https://xchain.io/api/orders/{asset}'
response = requests.get(url)
if response.status_code == 200:
    order_info = response.json()
    open_orders = 0
    filled_orders = 0
    for order in sorted(order_info["data"], key=lambda x: 0 if x["get_asset"] == "DANKROSECASH" else 1):
        if order["status"] == "open":
            open_orders += 1
            print(f'You pay with: {order["get_asset"]}')
            print(f'Get Quantity: {order["get_quantity"]}')
            print(f'Get Remaining: {order["get_remaining"]}')
            print(f'You recieve: {order["give_asset"]}')
            print(f'Give Quantity: {order["give_quantity"]}')
            print(f'Give Remaining: {order["give_remaining"]}')
            print(f'Block Index: {order["block_index"]}')
            print(f'Expire Index: {order["expire_index"]}')
            print(f'Status: {order["status"]}')
            print("\n")
        elif order["status"] == "filled":
            filled_orders += 1
    print("NUMBER OF OPEN MARKETS:", open_orders)
    print("NUMBER OF CLOSED MARKETS:", filled_orders)
else:
    print(f'Error: {response.status_code} - {response.reason}')
