import datetime
import sqlite3
conn = sqlite3.connect('Walmart.db')
cur = conn.cursor()
def run():
    

    cur.execute('DROP TABLE IF EXISTS Stock')
    cur.execute('CREATE TABLE Stock (date DATE PRIMARY KEY, price REAL)')
    cur.execute('DROP TABLE IF EXISTS SEO_data')
    cur.execute('CREATE TABLE Covid (date DATE PRIMARY KEY, cases REAL)')
    conn.commit()
run()

# cur.execute('SELECT MAX(date) FROM Stock')
# result = cur.fetchone()
# min_value = result[0]
# if min_value == None:
#     min_value = datetime.date.today().strftime('%Y-%m-%d')
# print(min_value) 
