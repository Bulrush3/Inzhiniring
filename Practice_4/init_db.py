"""
# CREATE TABLE books (
#     id             INTEGER    PRIMARY KEY AUTOINCREMENT,
#     title          TEXT (256),
#     author         TEXT (256),
#     genre          TEXT (256),
#     pages          INTEGER,
#     published_year INTEGER,
#     isbn           TEXT (256),
#     rating         INTEGER,
#     views          INTEGER
# );
"""

"""
CREATE TABLE sec_table (
    id      INTEGER    PRIMARY KEY AUTOINCREMENT,
    book_id            REFERENCES books (id),
    price   INTEGER,
    place   TEXT (256),
    date    TEXT (256) 
);
"""

"""
CREATE TABLE music (
    id           INTEGER    PRIMARY KEY AUTOINCREMENT,
    artist       TEXT (256),
    song         TEXT (256),
    duration_ms  INTEGER,
    year         INTEGER,
    tempo        REAL,
    genre        TEXT (256),
    acousticness REAL
);
"""

"""
CREATE TABLE products (
    id          INTEGER    PRIMARY KEY AUTOINCREMENT,
    name        TEXT (256),
    price       REAL,
    quantity    INTEGER,
    category    TEXT (256),
    fromCity    TEXT (256),
    isAvailable TEXT (256),
    views       INTEGER
);
"""
