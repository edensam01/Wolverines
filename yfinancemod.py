import yfinance as yf

# Replace "AAPL" with the stock symbol of your choice
ticker = yf.Ticker("AAPL")

# Retrieve historical data with non-trading days included
hist_data = ticker.history(period="max", interval="1d", auto_adjust=False)

print(hist_data)