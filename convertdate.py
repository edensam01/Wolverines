from datetime import datetime, timedelta

year = 2023

month = 4

day = 16

given_date = datetime(year, month, day)

start = given_date - timedelta(days=26)
end = given_date - timedelta(days=1)

start_str = start.strftime("%Y-%m-%d")
end_str = end.strftime("%Y-%m-%d")

print(start_str, end_str)