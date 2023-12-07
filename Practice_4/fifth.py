from connecting import connect_to_db
import json
import csv
import sqlite3

def parse_podcast_info(data):
    items = []
    with open(data, 'r', encoding='utf-8') as file:
        data_js = json.load(file)
        for i in data_js:
            i_upd = {}
            i_upd['guest'] = i['guest']
            i_upd['comments'] = int(i['comments'].replace(',', '')) 
            i_upd['sec_length'] = int(i['length_seconds'])
            i_upd['likes'] = int(i['likes'])
            i_upd['dislikes'] = int(i['dislikes'])
            i_upd['hd_quality'] = i['is_hd']
            items.append(i_upd)
    return items

def parse_influencers(filename):
    items = []
    with open(filename, "r", encoding="utf-8") as file:
        
        reader = csv.reader(file, delimiter=',')
        next(reader)

        for row in reader:
            item = {
            'youtuber_name': row[0],
            'channel_name': row[1],
            'category': row[2],
            'subscribers': int(row[3].replace('M', '').replace('.', '')) * 1000000,
            }
            if 'K' in row[6]: 
                item['avg_likes'] = int(row[6].replace('K', '').replace('.', '')) * 1000
            elif 'M' in row[6]:
                item['avg_likes'] = int(row[6].replace('M', '').replace('.', '')) * 1000000
            else: item['avg_likes'] = 1
            items.append(item)
    return items

def parse_DS_channels(data):

    with open(data, "r", encoding="utf-8") as file:
        items = []
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            item = {
            'channel_name': row[1],
            'subscribers': int(row[3]),
            'below_1k': int(row[5]),
            'between_1k_5k': int(row[6]),
            'between_5k_10k': int(row[7]),
            'between_10k_25k': int(row[8]),
            'between_25k_50k': int(row[9]),
            'between_50k_100k': int(row[10]),
            'between_100k_150k': int(row[11]),
            'between_150k_200k': int(row[12]),
            'between_200k_1m': int(row[13]),
            'above_1m': int(row[14]),
            }
            items.append(item)
            # print(items)
            # input()
    return items

def insert_podcast_info(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO podcast (guest, comments, sec_length, likes, dislikes, hd_quality) 
        VALUES(:guest, :comments, :sec_length, :likes, :dislikes, :hd_quality)""", data)
    db.commit()

def insert_youtube_info(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO youtube_top (youtuber_name, channel_name, category, subscribers, avg_likes) 
        VALUES(:youtuber_name, :channel_name, :category, :subscribers, :avg_likes)""", data)
    db.commit()

def insert_ds_channels(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO ds_channels (channel_name, subscribers, below_1k, between_1k_5k, between_5k_10k, between_10k_25k, 
            between_25k_50k, between_50k_100k, between_100k_150k, between_150k_200k, between_200k_1m, above_1m) 
        VALUES(:channel_name, :subscribers, :below_1k, :between_1k_5k, :between_5k_10k, :between_10k_25k, 
            :between_25k_50k, :between_50k_100k, :between_100k_150k, :between_150k_200k, :between_200k_1m, :above_1m)""", data)
    db.commit()

def best_videos(db, limit = 5): 
    cursor = db.cursor()
    items = []
    res = cursor.execute("""
            SELECT guest, comments, likes, dislikes FROM podcast
            WHERE comments > 1000
            ORDER BY likes / dislikes DESC
            LIMIT ?
            """, [limit])
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items

def counting_50k(db): 
    cursor = db.cursor()
    res = cursor.execute("""
            SELECT COUNT(*) AS num_channels_above_50k 
            FROM ds_channels 
            WHERE subscribers > 50000;
            """)
    result = dict(res.fetchone())
    cursor.close()
    return result

def channel_growth(db):
    cursor = db.cursor()
    cursor.execute("""
            UPDATE ds_channels 
            SET subscribers = subscribers * 1.05;
    """)
    db.commit()
    return []

def channels_in_each_category(db):
    cursor = db.cursor()
    res = cursor.execute("""
            SELECT category, COUNT(*) AS num_channels 
            FROM youtube_top 
            GROUP BY category;
            """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items

def aggregation(db):
    cursor = db.cursor()
    res = cursor.execute("""
            SELECT AVG(avg_likes) AS average_likes, 
                    AVG(subscribers) AS average_subscribers 
                FROM youtube_top;
            """)
    result = dict(res.fetchone())
    cursor.close()
    return result

def last_query(db, limit = 20):
    cursor = db.cursor()
    items = []
    res = cursor.execute("""
            SELECT * FROM podcast
            WHERE comments > 51000 AND hd_quality = 1
            ORDER BY sec_length DESC
            LIMIT ?
            """, [limit])
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


db = connect_to_db('files/test_db4')

# Парсим файлы данных
# podcast_data = parse_podcast_info('files/jre_yt.json')
# youtube_data = parse_influencers('files/youtube_influencers.csv')
# data_DS_channels = parse_DS_channels('files/YT_DS_Channels.csv')

# Заполняем таблицу данными
# insert_podcast_info(db, podcast_data)
# insert_youtube_info(db, youtube_data)
# insert_ds_channels(db, data_DS_channels)

# Запросы
bv = best_videos(db, 10) # Лучшие видео в соотношении +/-
with open("files/results/5/best_videos.json", "w", encoding="utf-8") as r_json:
    r_json.write(json.dumps(bv, ensure_ascii=False))

count50 = counting_50k(db) # Сосчитать количество каналов > 50k
with open("files/results/5/counting_50k.json", "w", encoding="utf-8") as r_json:
    r_json.write(json.dumps(count50, ensure_ascii=False))

channel_growth(db) # Прирастить каждому каналу 5% аудитории

ch_ctgrs = channels_in_each_category(db) # Количество каналов в каждой категории 
with open("files/results/5/channels_in_each_category.json", "w", encoding="utf-8") as r_json:
    r_json.write(json.dumps(ch_ctgrs, ensure_ascii=False))

ag = aggregation(db) # Средние классы и средние подписчики
with open("files/results/5/aggregation.json", "w", encoding="utf-8") as r_json:
    r_json.write(json.dumps(ag, ensure_ascii=False))

tops = last_query(db) # Самые комментируемые, длинные и HD выпуски
with open("files/results/5/good_releases.json", "w", encoding="utf-8") as r_json:
    r_json.write(json.dumps(tops, ensure_ascii=False))


