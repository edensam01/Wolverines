import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Calculate 5-day change in stock price
stock_df['5_day_change'] = Stock_SEO['price'].diff(periods=5)

# Calculate 5-day rolling average of visits
visits_df['5_day_avg_visits'] = Stock_SEO['number_of_visits'].rolling(window=5).mean()

# Merge stock and visits data on date column
merged_df = pd.merge(stock_df, visits_df, on='date')

#BAR CHART 1

# Create stacked bar chart
merged_df.plot(x='date', y=['5_day_change', '5_day_avg_time'], kind='bar', stacked=True)

# Set chart title and labels
plt.title('Average 5-Day Change in Stock Price vs. Average 5-Day Avg Time Spent on Site')
plt.xlabel('Date')
plt.ylabel('Value')

# Show the chart
plt.show()

#BAR CHART 2 

# Create stacked bar chart
merged_df.plot(x='date', y=['5_day_change', '5_day_avg_visits'], kind='bar', stacked=True)

# Set chart title and labels
plt.title('Average 5-Day Change in Stock Price vs. Average 5-Day Number of Visits')
plt.xlabel('Date')
plt.ylabel('Value')

# Show the chart
plt.show()