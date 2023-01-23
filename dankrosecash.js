import requests
import json

def get_dankrose_market():
    # Make GET request to /api/orders/{asset} endpoint
    response = requests.get("https://xchain.io/api/orders/DANKROSECASH")
    data = json.loads(response.text)

    # Filter results to only include orders that reference DANKROSECASH as give_asset or get_asset and have a status of "open"
    dankrose_orders = [order for order in data['data'] if (order['give_asset'] == "DANKROSECASH" or order['get_asset'] == "DANKROSECASH") and order["status"] == "open"]

    buy_prices = []
    for order in dankrose_orders:
        if order['give_asset'] == "DANKROSECASH":
            price = float(order['get_remaining']) / float(order['give_quantity'])
            remaining = order['give_remaining']
            buy_prices.append({"token": order['get_asset'], "price": price, "remaining": remaining})
    buy_prices = sorted(buy_prices, key=lambda x: x["price"])
    for price in buy_prices:
        print(f"Buy {price['remaining']} {price['token']} for {price['price']} DANKROSECASH. Remaining DANKROSECASH: {price['remaining']}")
    print("\n")
    sell_prices = []
    for order in dankrose_orders:
        if order['get_asset'] == "DANKROSECASH":
            price = float(order['get_quantity']) / float(order['give_remaining'])
            remaining = order['give_remaining']
            sell_prices.append({"token": order['give_asset'], "price": price, "remaining": remaining})
    sell_prices = sorted(sell_prices, key=lambda x: x["price"])
    for price in sell_prices:
        print(f"Sell {price['remaining']} DANKROSECASH for 1 {price['token']}. Remaining {price['token']}: {price['remaining']}")

get_dankrose_market()
