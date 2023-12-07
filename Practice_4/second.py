import pickle
from connecting import connect_to_db
import json

def load_data(file_name):
    items = []
    with open(file_name, 'rb') as f:
        data = pickle.load(f)

        for row in data:
            items.append(row)

    return items

def insert_data(db, data):
    cursor = db.cursor()

    cursor.executemany("""
        INSERT INTO sec_table (book_id, price, place, date)
        VALUES(
            (SELECT id FROM books WHERE title = :title),
            :price, :place, :date
            )
    """, data)

    db.commit()

def first_query(db, title):
    cursor = db.cursor()

    res = cursor.execute("""
            SELECT * 
            FROM sec_table 
            WHERE book_id = (SELECT id FROM books WHERE title = ?)
            """, [title])

    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
        
    cursor.close()
    return items

def second_query(db, title):
    cursor = db.cursor()

    res = cursor.execute("""
            SELECT 
                AVG(price) as avg_price
            FROM sec_table 
            WHERE book_id = (SELECT id FROM books WHERE title = ?)
            """, [title])

    print(dict(res.fetchone()))
        
    cursor.close()
    return []

def third_query(db, price):
    cursor = db.cursor()
    
    res = cursor.execute("""
            SELECT *
            FROM sec_table 
            WHERE book_id = (SELECT id FROM books WHERE place = 'online' AND price > ?)
            """, [price])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
        
    cursor.close()
    return items

# items = load_data('files/task_2_var_60_subitem.pkl')

db = connect_to_db("files/test_db")

book = first_query(db, "Алхимик") # данные о выбранной книге
with open("files/results/book_info_2.json", "w", encoding="utf-8") as r_json:
    r_json.write(json.dumps(book, ensure_ascii=False))

# second_query(db, "Алхимик") # средняя цена выбранной книги

books_2 = third_query(db, 4000) # книги онлайн и больше заданной цены
with open("files/results/books_online_2.json", "w", encoding="utf-8") as r_json:
    r_json.write(json.dumps(books_2, ensure_ascii=False))

# insert_data(db, items)