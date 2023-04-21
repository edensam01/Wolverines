import sqlite3

conn = sqlite3.connect('Walmart.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Stock')
cur.execute('DROP TABLE IF EXISTS SEO_data')
cur.execute('CREATE TABLE Stock (date DATE PRIMARY KEY, price REAL)')
cur.execute('CREATE TABLE SEO_data (date DATE PRIMARY KEY, traffic REAL)')
cur.execute('CREATE TABLE Stock_SEO AS SELECT Stock.date, Stock.price, SEO_data.traffic FROM Stock JOIN SEO_data ON Stock.date = SEO_data.date')

for row in data:
    cur.execute("INSERT INTO Stock (date, price) VALUES (?, ?)", row)

for row in data:
    cur.execute("INSERT INTO SEO_data (date, traffic) VALUES (?, ?)", row)

cur.execute('SELECT MIN(date) FROM Stock_SEO')
result = cur.fetchone()
min_value = result[0] 

conn.commit()
conn.close()