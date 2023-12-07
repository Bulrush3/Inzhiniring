import pickle
import msgpack
import json
from connecting import connect_to_db


def load_data_msgpack(file_name):
    # items = []
    with open(file_name, 'rb') as data_file:
        data_loaded = msgpack.load(data_file, raw=False)  # Указываем raw=False для чтения данных в человеко-читаемом формате
        for row in data_loaded:
            row['category'] = row.get('category', 'no')
    return data_loaded

def parse_upd_methods(data):
    items = []
    with open(data, 'r', encoding='utf-8') as file:
        data_js = json.load(file)
        for i in data_js:
            items.append(i)
    return items

def delete_by_name(db, name):
    cursor = db.cursor()
    cursor.execute('DELETE FROM products WHERE name = ?', [name])
    db.commit()

def update_price_by_precent(db, name, precent):
    cursor = db.cursor()
    cursor.execute('UPDATE products SET price = ROUND((price * (1 + ?)), 2) WHERE name = ?', [precent, name])
    cursor.execute('UPDATE products SET version = version +1 WHERE  name = ?', [name])
    db.commit()

def quantity_add(db, name, quantity):
    cursor = db.cursor()
    res = cursor.execute('UPDATE products SET quantity = (quantity + ?) WHERE (name = ?) AND ((quantity + ?)> 0)', [quantity, name, quantity])
    if res.rowcount > 0:
        cursor.execute('UPDATE products SET version = version +1 WHERE  name = ?', [name])
        db.commit()

def price_abs(db, name, value):
    cursor = db.cursor()
    res = cursor.execute('UPDATE products SET price = (price + ?) WHERE (name = ?) AND ((price + ?)> 0)', [value, name, value])
    if res.rowcount > 0:
        cursor.execute('UPDATE products SET version = version +1 WHERE  name = ?', [name])
        db.commit()

def available(db, name, value):
    cursor = db.cursor()
    cursor.execute('UPDATE products SET isAvailable = ? WHERE (name = ?)', [value, name])
    cursor.execute('UPDATE products SET version = version +1 WHERE  name = ?', [name])
    db.commit()

def handle_update(db, update_items):
    for item in update_items:
        match item['method']:
            case 'remove':
                print(f'Удалено {item["name"]}')
                delete_by_name(db, item["name"])
            case 'price_percent':
                print(f"Изменить на процент {item['name']} {item['param']}")
                update_price_by_precent(db, item['name'], item['param'])
            case 'price_abs':
                print(f"Изменение цены {item['name']} {item['param']}")
                price_abs(db, item['name'], item['param'])
            case 'available':
                print(f"Изменение доступности {item['name']} {item['param']}")
                available(db, item['name'], item['param'])
            case 'quantity_add':
                print(f"Изменение количества {item['name']} {item['param']}")
                quantity_add(db, item['name'], item['param'])
            case 'quantity_sub':
                print(f"Изменение количества {item['name']} {item['param']}")
                quantity_add(db, item['name'], item['param'])

def most_update(db, limit):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT * FROM products ORDER BY version DESC LIMIT ?
        """,[limit])
    items = []
    for row in result.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    
    return items

def min_max(db):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT
            SUM(price) as sum_price,
            AVG(price) as avg_price,
            MIN(price) as min_price,
            MAX(price) as max_price,
            SUM(quantity) as sum_quantity,
            AVG(quantity) as avg_quantity,
            MIN(quantity) as min_quantity,
            MAX(quantity) as max_quantity,
            SUM(views) as sum_views,
            AVG(views) as avg_views,
            MIN(views) as min_views,
            MAX(views) as max_views
        FROM products
        """)
    items = dict(result.fetchone())
    cursor.close()

    return items

# анализ остатков (сумма, мин, макс, среднее) для каждой группы товаров
def analyze_quality(db):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT category, AVG(quantity) as avg_price
        FROM products
        GROUP BY category
        """)
    items = dict(result.fetchall())
    cursor.close()

    return items

def second_query(db):
    cursor = db.cursor()
    result = cursor.execute("""
            SELECT name, price, fromCity               
            FROM products
            GROUP BY fromCity
        """)
    items = []
    for row in result.fetchall():
        item = dict(row)
        items.append(item)

    cursor.close()

    return items

def insert_data(db, data):
    cursor = db.cursor()

    cursor.executemany("""
        INSERT INTO products (name, price, quantity, fromCity, isAvailable, views, category)
        VALUES(
            :name, :price, :quantity, :fromCity, :isAvailable, :views, :category
            )
    """, data)

    db.commit()

data = load_data_msgpack('files/task_4_var_60_product_data.msgpack')

db = connect_to_db("files/test_db3")

methods = parse_upd_methods('files/task_4_var_60_update_data.json')

# Обновления
# handle_update(db, methods)

top = most_update(db, 10) # топ обновляемых товаров
with open("files/results/4/most_update.json", "w", encoding="utf-8") as r_json:
    r_json.write(json.dumps(top, ensure_ascii=False))

analysis = min_max(db) # анализ цен товаров (сумма, мин, макс, среднее) для каждой группы и кол-во товаров в группе
with open("files/results/4/min_max.json", "w", encoding="utf-8") as r_json:
    r_json.write(json.dumps(analysis, ensure_ascii=False))

city_alphabet = second_query(db) # название, цена товара - сортировка по городам
with open("files/results/4/alphabet_city.json", "w", encoding="utf-8") as r_json:
    r_json.write(json.dumps(city_alphabet, ensure_ascii=False))

residue_analysis = analyze_quality(db) # анализ остатков
with open("files/results/4/quality_analysis.json", "w", encoding="utf-8") as r_json:
    r_json.write(json.dumps(residue_analysis, ensure_ascii=False))

# insert_data(db, data)