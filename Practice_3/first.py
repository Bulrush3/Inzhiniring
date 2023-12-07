from bs4 import BeautifulSoup
import json
import re
import help



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
        return(item)
        
items = []
for i in range(1, 1000):
    result = handle_file(f'files/zip_var_60_1/{i}.html')
    items.append(result)

# Расчет статистики
views_values = list(map(lambda x: x['views'], items))
# print(views_values)
statistics = help.count_stats(views_values)
with open("files/results/1/views_stats.json", "w") as r_json:
    r_json.write(json.dumps(statistics, indent=2))
    
# Сортировка
items = sorted(items, key=lambda x: x['year'], reverse=True)
with open("files/results/1/sorted_buildings.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

#Фильтрация зданий по критерию: построено не раньше 1950 года
filtered_items = []
for item in items:
    if item["year"] > 1950:
        filtered_items.append(item)
with open("files/results/1/filtered_buildings.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(filtered_items, ensure_ascii=False))

# Расчет частоты меток в поле 'parking'
parking_values = list(map(lambda x: x['parking'], items))
parking_counts = help.freq_values(parking_values, 'parking')
# print(type_counts)
with open("files/results/1/parking_availability.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(parking_counts, ensure_ascii=False))
