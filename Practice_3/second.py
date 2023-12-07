from bs4 import BeautifulSoup
import json
import help

def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        text = ""
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')
        products = site.find_all("div", attrs={"class": "product-item"})
        for product in products:
            item = {}
            item['id'] = product.a["data-id"]
            item['link'] = product.find_all('a')[1]["href"]
            item['image'] = product.find_all('img')[0]['src']
            item['flash_drive'] = product.find_all('span')[0].get_text().strip()
            item['price'] = int(product.find_all('price')[0].get_text().replace(" ", ""). replace("₽", ""))
            item['bonus'] = int(product.strong.get_text().split()[2])
            props = product.ul.find_all("li")
            for prop in props:
                item[prop['type']] = prop.get_text().strip()

            items.append(item)
    return items

items = []
for i in  range(1,76):
    items = handle_file(f'files/zip_var_60_2/{i}.html')
    # print(items)

# Расчет статистики
bonus_values = list(map(lambda x: x['bonus'], items))
# print(bonus_values)
bonus_stat = help.count_stats(bonus_values)
with open("files/results/2/bonus_stat.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(bonus_stat, ensure_ascii=False))

# Сортировка
items = sorted(items, key=lambda x: x['price'], reverse=True)
with open("files/results/2/second_sorted.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

# Фильтрация
filtered_items = []
for item in items:
    if item["price"] > 100000:
        filtered_items.append(item)

with open("files/results/2/second_filtered.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(filtered_items, ensure_ascii=False))

matrix_values = []
for item in items:
    try:
        matrix_values.append(item['matrix'])
    except KeyError:
        matrix_values.append(None)

matrix_freq = help.freq_values(matrix_values, 'matrix')

with open("files/results/2/matrix_freq.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(matrix_freq, ensure_ascii=False))
