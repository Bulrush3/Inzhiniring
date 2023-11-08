import json
import msgpack
import os

with open('files/products_60.json') as f:
    data = json.load(f)

    products = {}

    for item in data:
        if item['name'] in products:
            products[item['name']].append(item['price'])
        else:
            products[item['name']] = list()
            products[item['name']].append(item['price'])

    # print(products)

    res_dict = []

    for name, prices in products.items():
        sum_price = 0
        max_price = prices[0]
        min_price = prices[0] 
        size = len(prices)
        for price in prices:
            sum_price += price
            max_price = max(max_price, price)
            min_price = min(min_price, price)
        
        avg_price = sum_price / size

        res_dict.append({
            "name": name,
            "max": max_price,
            "min": min_price,
            "avr": avg_price
        })

    print(res_dict)

    with open("files/products_result.json", "w") as r_json:
        r_json.write(json.dumps(res_dict))

    with open("files/products_result.msgpack", "wb") as r_msgpack:
        r_msgpack.write(msgpack.dumps(res_dict))

print(f"json    = {os.path.getsize('files/products_result.json')}")
print(f"msgpack = {os.path.getsize('files/products_result.msgpack')}")