from pymongo import MongoClient
import json

def save_in_json(data, filename): # Функция сохранения результата запроса в json
    with open(f"files/results/{filename}.json", "w", encoding='utf-8') as r_json:
        r_json.write(json.dumps(data, ensure_ascii=False))


def connect(): # Подключение к БД
    client = MongoClient()
    db = client["test-database"]
    return db.person

def get_from_json(filename): # Достать данные из файла
    items = []
    with open(filename, "r", encoding='utf-8') as f:
        items = json.load(f)
    return items

def insert_many(collection, data): # Заполнить базу имеющимися данными
    collection.insert_many(data)

def sort_by_salary(collection): # 10 самых высокооплачиваемых по убыванию
    persons = []
    for person in collection.find({}, limit=10).sort({'salary': -1}):
        person['_id'] = str(person['_id'])
        persons.append(person)
    return persons

def filter_by_age(collection): # 15 самых высокооплачиваемых по убыванию (моложе 30-ти) 
    persons = []
    for person in collection.find({"age": {"$lt": 30}},
                                limit=15).sort({'salary': -1}):
        person['_id'] = str(person['_id'])
        persons.append(person)
    return persons

def complex_filter_by_city_and_job(collection): # Ищем кто работает в Москве врачом, поваром или учителем (возраст по убыванию) 
    persons = []
    for person in collection.find({"city": "Москва",
                                    "job": {"$in": ['Врач', 'Повар', 'Учитель']}},
                                   limit=10).sort({'age': -1}):
        person['_id'] = str(person['_id'])
        persons.append(person)
    return persons
        
def count_obj(collection): # Люди от 30 до 50, с зп (от 50к до 75к / от 125к до 150к) на 2019-2022 года 
    result = collection.count_documents({
        "age": {"$gt": 30, "$lt": 50}, 
        "year": {"$gte": 2019, "$lte": 2022},
        "$or": [
           {"salary": {"$gt": 50000, "$lte": 75000}}, 
           {"salary": {"$gt": 125000, "$lt": 150000}}]
    })
    return result

# Заполнение базы данными
data = get_from_json('files/task_3_item.json')
insert_many(connect(), data)

# Сохранение файлов
query1 = sort_by_salary(connect())
save_in_json(query1, 'sort_by_salary')

query2 = filter_by_age(connect())
save_in_json(query2, 'filter_by_age')

query3 = complex_filter_by_city_and_job(connect())
save_in_json(query3, 'complex_filter_by_city_and_job')

query4 = count_obj(connect())
save_in_json(query4, 'count_obj')