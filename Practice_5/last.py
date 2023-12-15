from pymongo import MongoClient
import json
import csv


def connect(): # Подключение к БД
    client = MongoClient()
    db = client["influencers"]
    return db.person

def parse_csv(filename):
    items = []
    with open(filename, "r", encoding="utf-8") as file:
        
        reader = csv.reader(file, delimiter=',')
        next(reader)

        for row in reader:
            item = {
            'youtuber_name': row[0],
            'channel_name': row[1],
            'category': row[2],
            'subscribers': int(row[3].replace('M', '').replace('.', '')) * 100000,
            'country': row[4]
            }
            if 'K' in row[6]: 
                item['avg_likes'] = int(row[6].replace('K', '').replace('.', '')) * 1000
            elif 'M' in row[6]:
                item['avg_likes'] = int(row[6].replace('M', '').replace('.', '')) * 1000000
            else: item['avg_likes'] = None
            items.append(item)
    return items

def parse_json(filename):
    items = []
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        
        for row in data: 
            item = {
                'youtuber_name': row[0],
                'channel_name': row[1],
                'category': row[2],
                'subscribers': int(row[3].replace('M', '').replace('.', '')) * 100000,
                'country': row[4]
            }
             
            if 'K' in row[6]: 
                item['avg_likes'] = int(row[6].replace('K', '').replace('.', '')) * 1000
            elif 'M' in row[6]:
                item['avg_likes'] = int(row[6].replace('M', '').replace('.', '')) * 1000000
            else:
                item['avg_likes'] = None
    
            items.append(item)
    return items


def insert_many(collection, data): # Заполнить базу имеющимися данными
    collection.insert_many(data)

def save_in_json(data, filename): # Функция сохранения результата запроса в json
    with open(f"files/results/4/{filename}.json", "w", encoding='utf-8') as r_json:
        r_json.write(json.dumps(data, ensure_ascii=False))


def filter_by_likes(collection): # 7 самых нравящихся каналов по убыванию с ограничением по подписчикам
    persons = []
    for person in collection.find({"subscribers": {"$lt": 13500000}},
                                limit=5).sort({'avg_likes': -1}):
        person['_id'] = str(person['_id'])
        persons.append(person)

    save_in_json(persons, f'filter_by_likes')

def music_category(collection): # Лучшие в категории Music & Dance
    persons = []
    for person in collection.find({"category": "Music & Dance"}, limit=10).sort({'subscribers': -1}):
        person['_id'] = str(person['_id'])
        persons.append(person)

    save_in_json(persons, f'music_category')

def subs_likes(collection): # случайные каналы с (subscribers < 20M, likes > 200K)
    persons = []
    for person in collection.find({"subscribers": {"$lt": 20000000}, "avg_likes": {"$gt": 200000}},
                                limit=5):
        person['_id'] = str(person['_id'])
        persons.append(person)

    save_in_json(persons, f'subs_likes')

def three_categories(collection): #  10 каналов в определённых категориях с лайками > 10М
    persons = []
    for person in collection.find({"avg_likes": {"$gt": 1000000},
                                   "category": {"$in": ['Humor', 'DIY & Life Hacks', 'Video games']}},
                                    limit = 10).sort({'subscribers': -1}):
        person['_id'] = str(person['_id'])
        persons.append(person)

    save_in_json(persons, f'three_categories')


def without_seven_categories(collection): # каналы вне указанных категорий
    persons = []
    for person in collection.find({"category": {"$nin": ['Music & Dance', 'Animation', 'Humor', 
                                                         'DIY & Life Hacks', 'Video games',
                                                         'News & Politics', 'Movies', 'Education', '']}}
                                                         ):
        person['_id'] = str(person['_id'])
        persons.append(person)

    save_in_json(persons, f'without_seven_categories')
#=========================================================================================================
def get_stat_by_subscribers(collection):
    q = [
            {
                "$group": {
                    "_id": "result",
                    "max": {"$max": "$subscribers"},
                    "min": {"$min": "$subscribers"},
                    "avg": {"$avg": "$subscribers"},
                    }}
    ]

    results = []
    for stat in collection.aggregate(q):
        results.append(stat)

    save_in_json(results, 'get_stat_by_subscribers')

def get_amount_by_categories(collection):
    q = [
            {
                "$group": {
                    "_id": "$category",
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

    save_in_json(results, 'get_amount_by_categories')

def get_likes_stat_by_condition(collection):
    q = [
        {
            "$match": {
                "category": {"$in": ["Science & Technology", "DIY & Life Hacks"]},
                "country": {"$in": ["India", "Brazil"]},
            }
        },
        {
            "$group": {
                "_id": "result",
                "max": {"$max": "$avg_likes"},
                "min": {"$min": "$avg_likes"},
                "avg": {"$avg": "$avg_likes"},
            }
        }
    ]

    results = []
    for stat in collection.aggregate(q):
        results.append(stat)

    save_in_json(results, f'get_salary_stat_by_condition')

def amount_by_countries(collection): # < 20M subs
    q = [
        {
            "$match": {
                "subscribers": {"$lt": 20000000}
            }
        },
            {
                "$group": {
                    "_id": "$country",
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

    save_in_json(results, 'amount_by_countries')

def get_likes_stat_by_condition2(collection):
    q = [
        {
            "$match": {
                "category": {"$in": ["Music & Dance"]},
                "country": {"$nin": ["India", "United States"]},
                "$or": [
                    {"subscribers": {"$gt": 20000000, "$lt": 30000000}},
                    {"subscribers": {"$gt": 40000000, "$lt": 50000000}}
                ]
            }
        },
        {
            "$group": {
                "_id": "result",
                "max": {"$max": "$avg_likes"},
                "min": {"$min": "$avg_likes"},
                "avg": {"$avg": "$avg_likes"},
            }
        }
    ]

    results = []
    for stat in collection.aggregate(q):
        results.append(stat)

    save_in_json(results, 'get_salary_stat_by_condition')
#===========================================================
def delete1(collection):
    result = collection.delete_many({
        "$or": [
            {"subscribers": {"$lt": 20000000}},
            {"subscribers": {"$gt": 15000000}}
        ]
    })

def update_subscribers(collection):
    result = collection.update_many({
        "$mul": {
            "subscribers": 1.05
        }
    })

def update_likes(collection):
    result = collection.update_many({}, {
        "$inc": {"avg_likes": 5000}
    })
    
def increase_subscribers_by_CountryCategory(collection):
    filter = {
        "country": {"$in": ["Russia","China"]},
        "category": {"$in": ["Video games"]}
    }
    update = {
        "$mul": {
            "subscribers": 1.1
        }
    }

    result = collection.update_many(filter, update)

def delete2(collection):
    result = collection.delete_many({
        "category": {"$in": ["","Toys"]}
    })




# Парсим файлы данных
data1 = parse_csv('files/data_part1.csv')
data2 = parse_json('files/data_part2.json')

# # Заполняем таблицу данными
# insert_many(connect(), data1)
# insert_many(connect(), data2)

filter_by_likes(connect())
music_category(connect())
subs_likes(connect())
three_categories(connect())
without_seven_categories(connect())

get_stat_by_subscribers(connect())
get_amount_by_categories(connect())
get_likes_stat_by_condition(connect())
amount_by_countries(connect())
get_likes_stat_by_condition2(connect())

delete1(connect())
update_subscribers(connect())
update_likes(connect())
increase_subscribers_by_CountryCategory(connect())
delete2(connect())






    
