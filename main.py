import requests
from bs4 import BeautifulSoup
import csv

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

def main():
    #fortune 500 data link
    url = 'https://www.zyxware.com/articles/4344/list-of-fortune-500-companies-and-their-websites'

    #getting company name and website
    company_name, company_website = getCompanyData(url)

    #getting stock ticker
    company_ticker = getTicker(company_name)



if __name__ == "__main__":
    main()