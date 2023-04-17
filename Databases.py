import sqlite3

conn = sqlite3.connect('Walmart.db')
cur = conn.cursor()

for row in data:
    cur.execute("INSERT INTO Stock (date, price) VALUES (?, ?)", row)

for row in data:
    cur.execute("INSERT INTO SEO_data (date, traffic) VALUES (?, ?)", row)

cur.execute('SELECT MIN(date) FROM Stock_SEO')
result = cur.fetchone()
min_value = result[0] 

conn.commit()
conn.close()