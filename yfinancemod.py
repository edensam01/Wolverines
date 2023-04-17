import csv

company_name = "Walmart"

f = open('stock_tickers.csv', 'r')
k = csv.reader(f)
l = []
for i in k:
    if company_name in i[1]:
        ticker = i[0]
        break

print(ticker)
