from bs4 import BeautifulSoup
import json
virgo_counter = 0
counter = 0
sum_radius = 0
max_radius = 0
min_radius = 999999999

def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        text = ""
        for row in file.readlines():
            text += row

        star = BeautifulSoup(text, 'xml').star
        item = dict()

        item['name'] = star.find_all('name')[0].get_text().strip()
        item['constellation'] = star.find_all('constellation')[0].get_text().strip()
        item['spectral-class'] = star.find_all('spectral-class')[0].get_text().strip()
        item['radius'] = int(star.find_all('radius')[0].get_text().strip().split()[0])
        item['rotation(days)'] = float(star.find_all('rotation')[0].get_text().strip().split()[0])
        item['age(billion_years)'] = float(star.find_all('age')[0].get_text().strip().split()[0])
        item['distance(million_km)'] = float(star.find_all('distance')[0].get_text().strip().split()[0])
        item['absolute-magnitude(million_km)'] = float(star.find_all('absolute-magnitude')[0].get_text().strip().split()[0])
        
        global counter
        counter += 1
        global sum_radius
        sum_radius += item['radius']
        global max_radius
        global min_radius
        max_radius = max(item['radius'], max_radius)
        min_radius = min(item['radius'], min_radius)

        return item

items = []
for i in range(1, 500):
    result = handle_file(f'files/zip_var_60_3/{i}.xml')
    items.append(result)

average_radius = round(sum_radius / counter, 2)

print("radiusStatistics:", 
      "MAX - " + str(max_radius), 
      "MIN - " + str(min_radius), 
      "SUM - " + str(sum_radius), 
      "AVG - " + str(average_radius), sep = "\n")

items = sorted(items, key=lambda x: x['distance(million_km)'], reverse=True)

with open("files/results/3/third.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

filtered_items = []
for item in items:
    if item["age(billion_years)"] > 1.0:
        filtered_items.append(item)

with open("files/results/3/third_filtered.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(filtered_items, ensure_ascii=False))

for item in items:
    if item['constellation'] == "Дева":
        virgo_counter += 1
print(f"Звезд в созвездии 'Дева': {virgo_counter}")
print("Нефильтрованные:", len(items)," \nФильтрованные:", len(filtered_items))