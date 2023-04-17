import sqlite3

conn = sqlite3.connect('Walmart.db')
cur = conn.cursor()


cur.execute('DROP TABLE IF EXISTS Stock')
cur.execute('DROP TABLE IF EXISTS SEO_data')
cur.execute('CREATE TABLE Stock (date DATE PRIMARY KEY, price REAL)')
cur.execute('CREATE TABLE SEO_data (date DATE PRIMARY KEY, traffic REAL)')
cur.execute('CREATE TABLE Stock_SEO AS SELECT Stock.date, Stock.price, SEO_data.traffic FROM Stock JOIN SEO_data ON Stock.date = SEO_data.date')

conn.commit()
conn.close()