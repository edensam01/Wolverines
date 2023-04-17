import sqlite3

conn = sqlite3.connect('Walmart.db')
cur = conn.cursor()


cur.execute('DROP TABLE IF EXISTS Stock')
cur.execute('DROP TABLE IF EXISTS SEO_data')
cur.execute('CREATE TABLE Stock (date DATE PRIMARY KEY, price REAL)')
cur.execute('CREATE TABLE SEO_data (date DATE PRIMARY KEY, traffic REAL)')

conn.commit()
conn.close()