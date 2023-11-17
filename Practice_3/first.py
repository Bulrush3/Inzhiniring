from bs4 import BeautifulSoup
import json
import re
parking_counter = 0
counter = 0
sum_views = 0
max_views = 0
min_views = 999999999

def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        text = ""
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')
        item = dict()
        item['city'] = site.find_all("", string=re.compile('Город:'))[0].get_text().replace("Город: ", "").strip()
        item['building'] = site.find_all("h1")[0].get_text().replace("Строение:", "").strip()
        
        address_index = site.find_all("p", attrs={"class":'address-p'})[0].get_text().split("Индекс:")
        item['address'] = address_index[0].replace("Улица:", "").strip()
        item['index'] = address_index[1].strip()
        
        item['floors'] = int(site.find_all("span", attrs={"class": "floors"})[0].get_text().split(":")[1])
        item['year'] = int(site.find_all("span", attrs={"class": "year"})[0].get_text().replace("Построено в ", ""))
        item['parking'] = site.find_all("span", string=re.compile('Парковка:'))[0].get_text().split(":")[1].strip()
        item['image'] = site.find_all("img")[0]["src"]
        item['rating'] = float(site.find_all("span", string=re.compile('Рейтинг:'))[0].get_text().split(":")[1].strip())
        item['views'] = int(site.find_all("span", string=re.compile('Просмотры:'))[0].get_text().split(":")[1].strip())
        global counter
        counter += 1
        global sum_views
        sum_views += item['views']
        global max_views
        global min_views
        max_views = max(item['views'], max_views)
        min_views = min(item['views'], min_views)
        
        return(item)
        
items = []
for i in range(1, 1000):
    result = handle_file(f'files/zip_var_60_1/{i}.html')
    items.append(result)

average_views = round(sum_views / counter, 2)

print("ViewsStatistics:", 
      "MAX - " + str(max_views), 
      "MIN - " + str(min_views), 
      "SUM - " + str(sum_views), 
      "AVG - " + str(average_views), sep = "\n")

items = sorted(items, key=lambda x: x['year'], reverse=True)

with open("files/results/1/first.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

filtered_items = []
for item in items:
    if item["year"] > 1950:
        filtered_items.append(item)

with open("files/results/1/first_filtered.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(filtered_items, ensure_ascii=False))

for item in items:
    if item['parking'] == "есть":
        parking_counter += 1
print(f"Зданий с парковками: {parking_counter}", f"Зданий без парковок: {counter - parking_counter}", sep = "\n")
print("Нефильтрованные:", len(items)," \nФильтрованные:", len(filtered_items))