import sqlite3

conn = sqlite3.connect('Walmart.db')
cur = conn.cursor()

for row in data:
    cur.execute("INSERT INTO Stock (date, price) VALUES (?, ?)", row)

for row in data:
    cur.execute("INSERT INTO SEO_data (date, number_of_visits, timeSpent) VALUES (?, ?, ?)", row)

cur.execute('SELECT COUNT(*) as row_count FROM Stock_SEO')
row = cur.fetchone()
row_count = row[0]
if (row_count == 0):
    cur.execute('SELECT date()')
    min = cur.fetchtone()
    min_value = min[0]
else:
    cur.execute('SELECT MIN(date) FROM Stock_SEO')
    result = cur.fetchone()
    min_value = result[0] 

conn.commit()
conn.close()
