import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
import csv
import yfinance as yf
import pandas as pd
import numpy as np
import sqlite3
from covid19dh import covid19


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
        min_value = '2020-01-20' #first recorded covid case
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
    print(data)

    data_list = [(np.datetime_as_string(date, unit='D'), round(adj_close, 2)) for date, adj_close in data[['Adj Close']].to_records()]

    return data_list

def insertValsStock(data, cur, conn):
    for i in data:
        cur.execute("INSERT INTO Stock (date, price) VALUES (?, ?);", i)
    conn.commit()

def getCovidData(start, end):
    x = covid19("USA", start = start, end = end)[0]
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

    #fortune 500 data link
    url = 'https://www.zyxware.com/articles/4344/list-of-fortune-500-companies-and-their-websites'

    #getting company name and website
    company_name = getCompanyData(url)[0]

    #getting stock ticker
    company_ticker = getTicker(company_name)
    print(company_ticker)

    #getting date to work from
    date_to_work = getDate(cur)
    print([date_to_work])
    year = int(date_to_work[:4])
    month = int(date_to_work[5:7])
    day = int(date_to_work[8:10])

    #getting start and end date
    start, end = startAndEnd(year, month, day)

    #getting stock values to input
    stock_data = getStockData(company_ticker, start, end)
    
    #insert values into the stock table
    insertValsStock(stock_data, cur, conn)

    #getting covid values to input
    covid_data = getCovidData(start, end)

    #insert values into the covid table
    insertValsCovid(covid_data, cur, conn)
    

if __name__ == "__main__":
    main()