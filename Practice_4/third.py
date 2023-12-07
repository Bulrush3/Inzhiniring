import pickle
import msgpack
from connecting import connect_to_db
import json

def load_data_pickle(file_name):
    items = []
    with open(file_name, 'rb') as f:
        data = pickle.load(f)

        for row in data:
            row.pop("energy")
            row.pop("popularity")
            items.append(row)

    return items

def load_data_msgpack(file_name):
    # items = []
    # Открываем файл в режиме чтения бинарного файла ('rb')
    with open(file_name, 'rb') as data_file:
        data_loaded = msgpack.load(data_file, raw=False)  # Указываем raw=False для чтения данных в человеко-читаемом формате
        for row in data_loaded:
            # items.append(row)
            row.pop('speechiness')
            row.pop('mode')
            row.pop('instrumentalness')
            # print(row)
            # input()
    return data_loaded


def insert_data(db, data):
    cursor = db.cursor()

    cursor.executemany("""
        INSERT INTO music (artist, song, duration_ms, year, tempo, genre, acousticness)
        VALUES(
            :artist, :song, :duration_ms, :year, :tempo, :genre, :acousticness
            )
    """, data)

    db.commit()

def get_stat_by_duration(db):
    cursor = db.cursor()
    res = cursor.execute("""
    SELECT
        SUM(duration_ms) as sum,
        AVG(duration_ms) as avg,                
        MIN(duration_ms) as min,
        MAX(duration_ms) as max
    FROM music
    """)

    print(dict(res.fetchone()))

    cursor.close()
    return []

def get_freq_by_year(db):
    cursor = db.cursor()
    res = cursor.execute("""
    SELECT
        COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() as count,
        year as published_year
    FROM music
    GROUP BY year
    """)
    for row in res.fetchall():
        print(dict(row))
    

def filter_by_tempo(db, min_year, limit = 15): #json
    cursor = db.cursor()
    items = []
    res = cursor.execute("""
            SELECT artist, song, year FROM music
            WHERE year > ? ORDER BY tempo DESC
            LIMIT ?
            """, [min_year, limit])
    for row in res.fetchall():
        item = dict(row)
        items.append(item)

    cursor.close()
    return items

def get_top_by_acoustic(db, limit): #json
    cursor = db.cursor()

    res = cursor.execute("SELECT artist, song, acousticness FROM music ORDER BY acousticness DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
        
    cursor.close()
    return items


items = load_data_pickle('files/task_3_var_60_part_1.pkl') + load_data_msgpack('files/task_3_var_60_part_2.msgpack')

db = connect_to_db("files/test_db2")

items_2 = filter_by_tempo(db, 2017) # новые песни сортированные по темпу
get_stat_by_duration(db) # статистика длительностей
items_1 = get_top_by_acoustic(db, 10) # самые акустичные песни
get_freq_by_year(db) # доля выпущенных треков по годам


# insert_data(db, items)

with open("files/results/top_10_by_acoustic_3.json", "w", encoding="utf-8") as r_json:
    r_json.write(json.dumps(items_1, ensure_ascii=False))

with open("files/results/filter_by_tempo_3.json", "w", encoding="utf-8") as r_json:
    r_json.write(json.dumps(items_2, ensure_ascii=False))  

