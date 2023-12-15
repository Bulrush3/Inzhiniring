from pymongo import MongoClient
import json
import pickle


def connect(): # Подключение к БД
    client = MongoClient()
    db = client["test-database"]
    return db.person

def load_data_pickle(file_name):
    items = []
    with open(file_name, 'rb') as f:
        data = pickle.load(f)

        for row in data:
            items.append(row)

    return items

def insert_many(collection, data): # Заполнить базу имеющимися данными
    collection.insert_many(data)

def save_in_json(data, filename): # Функция сохранения результата запроса в json
    with open(f"files/results/2/{filename}.json", "w", encoding='utf-8') as r_json:
        r_json.write(json.dumps(data, ensure_ascii=False))

def delete_by_salary(collection):
    result = collection.delete_many({
        "$or": [
            {"salary": {"$lt": 25000}},
            {"salary": {"$gt": 175000}}
        ]
    })
    print(result)

def update_age(collection):
    result = collection.update_many({}, {
        "$inc": {"age": 1}
    })
    print(result)

def increase_salary_by_job(collection):
    filter = {
        "job": {"$in": ["Психолог","Косметолог","Оператор call-центра"]}
    }
    update = {
        "$mul": {
            "salary": 1.05
        }
    }

    result = collection.update_many(filter, update)
    print(result)

def increase_salary_by_city(collection):
    filter = {
        "city": {"$in": ["Краков","Льейда","Душанбе"]}
    }
    update = {
        "$mul": {
            "salary": 1.07
        }
    }

    result = collection.update_many(filter, update)
    print(result)

def increase_salary_by_CityAgeJob(collection):
    filter = {
        "city": {"$nin": ["Овьедо","Севилья","Мурсия"]},
        "job": {"$in": ["Водитель","Строитель","Учитель"]},
        "age": {"$in": [22, 65, 43]}
    }
    update = {
        "$mul": {
            "salary": 1.1
        }
    }

    result = collection.update_many(filter, update)
    print(result)

def custom_delete(collection):
    result = collection.delete_many({
        "city": {"$in": ["Махадаонда","Загреб"]},
        "age": {"$lt": 18},
        "age": {"$gt": 22}
    })
    print(result)

data = load_data_pickle('files/task_2_item.pkl')
# insert_many(connect(), data)

# delete_by_salary(connect())
# update_age(connect())
# increase_salary_by_job(connect())
# increase_salary_by_city(connect())
# increase_salary_by_CityAgeJob(connect())
# custom_delete(connect())
