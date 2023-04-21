import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
import csv
import yfinance as yf
import pandas as pd
import numpy as np
import sqlite3
from covid19dh import covid19

'''

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
|                                           |
|   run `pip3 install -r requirements.txt`  |
|           to install the APIs             |
|                                           |
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

'''
def clean_databases(cur, conn):
    cur.execute('DROP TABLE IF EXISTS Stock')
    cur.execute('CREATE TABLE Stock (id INTEGER PRIMARY KEY, date DATE, price REAL)')
    cur.execute('DROP TABLE IF EXISTS Covid')
    cur.execute('CREATE TABLE Covid (id INTEGER PRIMARY KEY, date DATE, cases REAL)')
    cur.execute('DROP TABLE IF EXISTS Stock_Covid')
    conn.commit()

def getCompanyData(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', {'class': 'table'})
    rows = table.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 3:
            company_name = cols[1].get_text()
            website = cols[2].get_text()
            break
    
    return (company_name, website)

def getTicker(company_name):
    f = open('stock_tickers.csv', 'r')
    k = csv.reader(f)

    for i in k:
        if company_name in i[1]:
            ticker = i[0]
            break

    return ticker

def getDate(cur):
    cur.execute('SELECT MAX(date) FROM Stock')
    result = cur.fetchone()
    min_value = result[0]
    if min_value == None:
        min_value = '2020-03-15' #from 15th March (when US went into lockdown)
    return min_value

def startAndEnd(year, month, day):
    given_date = datetime(year, month, day)

    start = given_date + timedelta(days=1)
    end = given_date + timedelta(days=25)

    start_str = start.strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")

    return (start_str, end_str)

def getStockData(company_ticker, start, end):
    data = yf.download(company_ticker, start=start, end=end)
    date_range = pd.date_range(start=start, end=end)
    data = data.reindex(date_range)
    data.fillna(method="ffill", inplace=True)

    data_list = [(np.datetime_as_string(date, unit='D'), round(adj_close, 2)) for date, adj_close in data[['Adj Close']].to_records()]

    return data_list

def insertValsStock(data, cur, conn):
    for i in data:
        cur.execute("INSERT INTO Stock (date, price) VALUES (?, ?);", i)
    conn.commit()

def getCovidData(start, end):
    x = covid19("USA", start = start, end = end, verbose = False)[0]
    l = list(zip(x['date'].dt.strftime('%Y-%m-%d'), x['confirmed']))
    return l

def insertValsCovid(data, cur, conn):
    for i in data:
        cur.execute("INSERT INTO Covid (date, cases) VALUES (?, ?);", i)
    conn.commit()

def main():
    #connect to database
    conn = sqlite3.connect('Walmart.db')
    cur = conn.cursor()

    #check to erase the databases
    answer = input("Type 'execute' to clean/create the database, otherwise click enter: ")
    print()
    if answer == 'execute':
        clean_databases(cur, conn)
        return

    #fortune 500 data link
    url = 'https://www.zyxware.com/articles/4344/list-of-fortune-500-companies-and-their-websites'

    #getting company name and website
    company_name = getCompanyData(url)[0]
    print(f"The top fortune 500 company is {company_name}\n")

    #getting stock ticker
    company_ticker = getTicker(company_name)
    print(f"The stock tickers for {company_name} is {company_ticker}\n")

    #getting date to work from
    date_to_work = getDate(cur)
    year = int(date_to_work[:4])
    month = int(date_to_work[5:7])
    day = int(date_to_work[8:10])
    
    #getting start and end date
    start, end = startAndEnd(year, month, day)
    print(f"Getting data from {start} to {end}\n")

    #getting stock values to input
    print("Getting Stock Data...")
    stock_data = getStockData(company_ticker, start, end)
    print("Received Stock Data!\n")

    #insert values into the stock table
    print("Inserting Stock Data...")
    insertValsStock(stock_data, cur, conn)
    print("Inserted Stock Data!\n")

    #getting covid values to input
    print("Getting Covid Data...")
    covid_data = getCovidData(start, end)
    print("Received Covid Data!\n")

    #insert values into the covid table
    print("Inserting Covid Data...")
    insertValsCovid(covid_data, cur, conn)
    print("Inserted Covid Data!\n")

    cur.execute('DROP TABLE IF EXISTS Stock_Covid')
    cur.execute('CREATE TABLE Stock_Covid AS SELECT Stock.id, Stock.date, Stock.price, Covid.cases FROM Stock JOIN Covid ON Stock.id = Covid.id')
    print("Joined Tables Succesfully!\n")

if __name__ == "__main__":
    main()