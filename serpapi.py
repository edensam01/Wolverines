import pytrends.request
import pandas as pd
# company_name = "Walmart"
# start = "2023-04-17"
# end = "2023-03-23"

# pytrends = pytrends.request.TrendReq(hl='en-US', tz=360)

# kw_list = [company_name]
# pytrends.get_historical_interest(kw_list, year_start=2018, month_start=1, day_start=1, hour_start=0, year_end=2018, month_end=2, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=0) 

start = "2023-04-17"
end = "2023-03-23"

# Create a pytrends object
pytrends = pytrends.request.TrendReq()

# Set the search term and time frame
kw_list = ["Walmart"]
timeframe = "today 5-y"

# Build the payload
pytrends.build_payload(kw_list, timeframe=timeframe)

date_range = pd.date_range(start=start, end=end)

# Get the interest over time
data = pytrends.interest_over_time()
data = data.reindex(date_range)
data.fillna(method="ffill", inplace=True)


# Print the results
print(data)