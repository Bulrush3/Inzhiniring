from bs4 import BeautifulSoup
import json
counter = 0
matrix_counter = 0
sum_bonus = 0
max_bonus = 0
min_bonus = 999999999

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

            global counter
            counter += 1
            global sum_bonus
            sum_bonus += item['bonus']
            global max_bonus
            global min_bonus
            max_bonus = max(item['bonus'], max_bonus)
            min_bonus = min(item['bonus'], min_bonus)
            
            # print(item)
            items.append(item)
    return items

items = []
for i in  range(1,76):
    items = handle_file(f'files/zip_var_60_2/{i}.html')
    # print(items)

average_bonus = round(sum_bonus / counter, 2)

print("ViewsStatistics:", 
      "MAX - " + str(max_bonus), 
      "MIN - " + str(min_bonus), 
      "SUM - " + str(sum_bonus), 
      "AVG - " + str(average_bonus), sep = "\n")

items = sorted(items, key=lambda x: x['price'], reverse=True)

with open("files/results/2/second.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

filtered_items = []
for item in items:
    if item["price"] > 100000:
        filtered_items.append(item)

with open("files/results/2/second_filtered.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(filtered_items, ensure_ascii=False))

for item in items:
    try:
        if item['matrix']:
            matrix_counter += 1
    except KeyError:
        continue


print(f"Телефоны, где упоминается матрица: {matrix_counter}", f"Телефоны, где не упоминается матрица: {counter - matrix_counter}", sep = "\n")
print("Нефильтрованные:", len(items)," \nФильтрованные:", len(filtered_items), sep = " ")