from bs4 import BeautifulSoup
import json
counter = 0
socks_counter = 0
sum_rating = 0
max_rating = 0
min_rating = 999999999

def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        text = ""
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'xml')

        for clothes in site.find_all("clothing"):
            item = {}
            for el in clothes.contents:
                if el.name is None:
                    continue
                elif el.name == "price" or el.name == "reviews":
                    item[el.name] = int(el.get_text().strip())
                elif el.name == "rating":
                    item[el.name] = float(el.get_text().strip())
                elif el.name == "new":
                    item[el.name] = el.get_text().strip() == "+"
                elif el.name == "exclusive" or el.name == "sporty":
                    item[el.name] = el.get_text().strip() == "yes"
                else:
                    item[el.name] = el.get_text().strip()

            global counter
            counter += 1
            global sum_rating
            sum_rating += item['rating']
            global max_rating
            global min_rating
            max_rating = max(item['rating'], max_rating)
            min_rating = min(item['rating'], min_rating)

            items.append(item)
            # print(items)
            # input()
    return items

items = []
for i in range(1, 101):
    items = handle_file(f'files/zip_var_60_4/{i}.xml')
    # items.append(result)

average_rating = round(sum_rating / counter, 2)

print("BonusStatistics:", 
      "MAX - " + str(max_rating), 
      "MIN - " + str(min_rating), 
      "SUM - " + str(sum_rating), 
      "AVG - " + str(average_rating), sep = "\n")

items = sorted(items, key=lambda x: x['price'], reverse=True)

with open("files/results/4/fourth.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

filtered_items = []
for item in items:
    if item["reviews"] > 500000:
        filtered_items.append(item)

with open("files/results/4/filtered_fourth.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(filtered_items, ensure_ascii=False))

for item in items:
    if item['category'] == "Socks":
        socks_counter += 1
print(f"Позиций 'Носки' у нас тут: {socks_counter}")
print("Нефильтрованные:", len(items)," \nФильтрованные:", len(filtered_items), sep = " ")
