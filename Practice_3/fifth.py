import json
import os
import urllib.request
from bs4 import BeautifulSoup

max_price = 0
min_price = 999999999
count_price = 0
sum_price = 0
machete_counter = 0

freq = {}
items = []
url = "https://www.huntworld.ru/catalog/okhota_i_sportivnaya_strelba/nozhi_i_instrumenty/?PAGEN_1="
for i in range(1, 12):
    html_content = urllib.request.urlopen(url + str(i+1)).read() 
    soup = BeautifulSoup(html_content, "html.parser")
    
    knifes = soup.find_all("div", attrs={"class":"card-container"})

    for knife in knifes:
        item = {}

        item['name'] = knife.find_all("a", attrs={"product-preview__name no-link"})[0].get_text()
        item['price'] = int(knife.find_all("span", attrs={"class": "price-num"})[0].get_text().replace(" ", ""))
        item['href'] = knife.find_all("a", attrs={"product-preview__name no-link"})[0]["href"]
        item['rating'] = float(knife.find_all("div", attrs={"class": "product-preview__rate"})[0].get_text())
        try:
            item['reviews'] = int(knife.find_all("div", attrs={"class": "product-preview__count-review"})[0].get_text())
        except IndexError:
            item['reviews'] = 0

        items.append(item)

        count_price += 1
        sum_price += item['price']
        max_price = max(item['price'], max_price)
        min_price = min(item['price'], min_price)
        if "Мачете" in item['name']:
            machete_counter += 1 

average_price = round(sum_price / count_price, 2)

with open("files/results/fifth_result.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(items, indent=2, ensure_ascii=False))

sorted_data = sorted(items, key=lambda x: x["reviews"], reverse=True)
with open("files/results/fifth_result_sorted.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(sorted_data, indent=2, ensure_ascii=False))
    
filtered_data = list(filter(lambda x: x["rating"] >= 4.5, items))
with open("files/results/fifth_result_filtered.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(filtered_data, indent=2, ensure_ascii=False))

with open("files/results/fifth_stats.json", "w") as file:
    file.write(json.dumps(
        {
            "sum_price": sum_price,
            "min_price": min_price,
            "max_price": max_price,
            "average_price": average_price
        },
        indent=2))

with open("files/results/fifth_freq.json", "w") as file:
    file.write(json.dumps({"Frequency_of_Machete" : machete_counter}, indent=2))

            