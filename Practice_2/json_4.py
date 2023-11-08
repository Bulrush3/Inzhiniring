# подключаем библиотеки
import json
import pickle

# функция обновления цены у товара
def update_price(product, price_info):
    method = price_info["method"]
    if method == "sum":
        product["price"] += price_info["param"]
    elif method == "sub":
        product["price"] -= price_info["param"]
    elif method == "percent+":
        product["price"] *= (1 + price_info["param"])
    elif method == "percent-":
        product["price"] *= (1 - price_info["param"])

    product["price"] = round(product["price"], 2)



with open("files/products_60.pkl", "rb") as f:
    products = pickle.load(f)

with open("files/price_info_60.json") as f:
    price_info = json.load(f)

# print(price_info)

# необходимо сопоставить объект с товаром и объект с информацией, как обновить ему цену
# разложим в карту информацию об обновлении цен

price_info_dict = dict() # name -> {name,method,param}

for item in price_info:
    price_info_dict[item["name"]] = item

# print(products)
# теперь можем пропустить через нашу функцию обновления все товары
for product in products:
    # получаем по ключу (имени товара) объект с информацией
    current_price_info = price_info_dict[product["name"]]
    update_price(product, current_price_info)

# print(products)

# запишем полученный результат
with open("files/products_updated.pkl", "wb") as f:
    f.write(pickle.dumps(products))
