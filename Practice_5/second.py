from pymongo import MongoClient
import json
import msgpack


def connect(): # Подключение к БД
    client = MongoClient()
    db = client["test-database"]
    return db.person

def load_data_msgpack(file_name):
    with open(file_name, 'rb') as data_file:
        data_loaded = msgpack.load(data_file, raw=False)  # Указываем raw=False для чтения данных в человеко-читаемом формате
    return data_loaded

def insert_many(collection, data): # Заполнить базу имеющимися данными
    collection.insert_many(data)

def save_in_json(data, filename): # Функция сохранения результата запроса в json
    with open(f"files/results/2/{filename}.json", "w", encoding='utf-8') as r_json:
        r_json.write(json.dumps(data, ensure_ascii=False))

def get_stat_by_salary(collection):
    q = [
            {
                "$group": {
                    "_id": "result",
                    "max": {"$max": "$salary"},
                    "min": {"$min": "$salary"},
                    "avg": {"$avg": "$salary"},
                    }}
    ]

    results = []
    for stat in collection.aggregate(q):
        results.append(stat)
    
    save_in_json(results, 'get_stat_by_salary')
    

def get_amount_by_jobs(collection):
    q = [
            {
                "$group": {
                    "_id": "$job",
                    "count": {"$sum": 1},
                    }},
                    {
                        "$sort": {
                            "count": -1
                        }
                    }
    ]

    results = []
    for stat in collection.aggregate(q):
        results.append(stat)
    
    save_in_json(results, 'get_amount_by_jobs')


def get_salary_stat_by_column(collection, column_name):
    q = [
            {
                "$group": {
                    "_id": f"${column_name}",
                    "max": {"$max": "$salary"},
                    "min": {"$min": "$salary"},
                    "avg": {"$avg": "$salary"},
                    }}
    ]

    results = []
    for stat in collection.aggregate(q):
        results.append(stat)

    save_in_json(results, f'get_salary_stat_by_{column_name}')
    

def get_age_stat_by_column(collection, column_name):
    q = [
            {
                "$group": {
                    "_id": f"${column_name}",
                    "max": {"$max": "$age"},
                    "min": {"$min": "$age"},
                    "avg": {"$avg": "$age"},
                    }}
    ]

    results = []
    for stat in collection.aggregate(q):
        results.append(stat)

    save_in_json(results, f'get_age_stat_by_{column_name}')


def max_salary_by_min_age(collection):
    q = [
        {
            '$sort':{
                'age': 1,
                'salary': -1
            },
        }
    ]

    results = []
    for stat in collection.aggregate(q):
        results.append(stat)

    save_in_json(results, 'max_salary_by_min_age')


def min_salary_by_max_age(collection):
    q = [
        {
            '$sort':{
                'age': -1,
                'salary': 1
            }
        }
    ]

    results = []
    for stat in collection.aggregate(q):
        results.append(stat)

    save_in_json(results, 'min_salary_by_max_age')


def big_query(collection):
    q = [
        {
            "$match": {
                "salary": {"$gt": 50000}
            }
        },
        {
            "$group": {
                "_id": "$city",
                "max": {"$max": "$age"},
                "min": {"$min": "$age"},
                "avg": {"$avg": "$age"},
            }
        },
        {
            "$sort": {
                "min": -1
                    }
                }
        
    ]

    results = []
    for stat in collection.aggregate(q):
        results.append(stat)

    save_in_json(results, 'big_query')


def big_query2(collection):
    q = [
        {
            "$match": {
                "city": {"$in": ["София", "Рига", "Луго"]},
                "job": {"$in": ["Повар","Медсестра", "Врач"]},
                "$or": [
                    {"age": {"$gt": 18, "$lt": 25}},
                    {"age": {"$gt": 50, "$lt": 65}}
                ]
            }
        },
        {
            "$group": {
                "_id": "result",
                "max": {"$max": "$salary"},
                "min": {"$min": "$salary"},
                "avg": {"$avg": "$salary"},
            }
        }
    ]

    results = []
    for stat in collection.aggregate(q):
        results.append(stat)

    save_in_json(results, 'big_query2')


def big_query3(collection):
    q = [
        {
            "$match": {
                "year": {"$lt": 2004}
            }
        },
            {
                "$group": {
                    "_id": "$city",
                    "count": {"$sum": 1},
                    }},
        {
            "$sort": {
                "count": -1
                    }
                }
        
    ]

    results = []
    for stat in collection.aggregate(q):
        results.append(stat)

    save_in_json(results, 'big_query3')



data = load_data_msgpack('files/task_1_item.msgpack')
insert_many(connect(), data)

get_stat_by_salary(connect()) # вывод минимальной, средней, максимальной salary 
get_amount_by_jobs(connect()) # вывод количества данных по представленным профессиям 
get_salary_stat_by_column(connect(), "city") # вывод минимальной, средней, максимальной salary по городу 
get_salary_stat_by_column(connect(), "job") # вывод минимальной, средней, максимальной salary по профессии 
get_age_stat_by_column(connect(), "city") # вывод минимального, среднего, максимального возраста по городу 
get_age_stat_by_column(connect(), "job") # вывод минимального, среднего, максимального возраста по профессии  
 
max_salary_by_min_age(connect()) # вывод максимальной заработной платы при минимальном возрасте 
min_salary_by_max_age(connect()) # вывод минимальной заработной платы при максимальной возрасте 

big_query(connect()) # вывод min, max, average возраста по городу, при условии, что заработная плата > 50 000, сортировка по min возрасту. 
big_query2(connect()) # вывод min, max, average зарплаты по городу, профессии с 18<age<25 & 50<age<65
big_query3(connect()) #
