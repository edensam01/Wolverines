import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def write_to_file(f, s):
    f.write(s)
    return

def main():
    conn = sqlite3.connect('Walmart.db')
    cur = conn.cursor()
    f = open('calculations.txt', 'w')

    #reading in the joined table to a pandas dataframe
    df = pd.read_sql_query('SELECT * FROM Stock_Covid', conn)

    #cleaning the table to remove all NA values
    df = df.fillna(method='ffill', limit=100)

    #Getting daily case count instead of cumulative
    df['cases_per_day'] = df['cases'].diff()
    df.loc[0, 'cases_per_day'] = 907.0
    
    #dropping total cases as we have no use of it
    df = df.drop('cases', axis = 1)
    
    #renaming the column to cases for simplicity
    df = df.rename(columns={'cases_per_day': 'cases'})

    Information = 'When the mean is significantly different from the median, it usually indicates that there are some extreme values (outliers) in the data that are pulling the mean in one direction or the other.\n\n'

    write_to_file(f, Information)

    #calculating average stock price
    cur.execute('SELECT AVG(price) FROM Stock_Covid')
    average_price = round(cur.fetchone()[0], 2)
    #calculating median stock price
    median_stock_price = round(df['price'].median(), 2)

    #writing calculations to file
    temp = f'Average Price: {average_price} | Median Price: {median_stock_price} \n'
    write_to_file(f, temp)

    #calculating average cases per day
    average_cases = round(df['cases'].mean(), 2)
    #calculating median cases per day
    median_cases = round(df['cases'].median(), 2)

    #writing calculations to file
    temp = f'Average Cases: {average_cases} | Median Cases: {median_cases} \n\n'
    write_to_file(f, temp)

    Information = "From the data, we can conclude that there aren't many outliers in the price, but there are a lot of outliers in the number of cases per day. This would mean that to find correlations, it woul be better to look at larger datasets\n"

    write_to_file(f, Information)

    #calculation 1: Rolling 5 day average for price
    df['price_5day'] = df['price'].rolling(window=5).mean()

    #calculation 2: Rolling 5 day average for cases
    df['cases_5day'] = df['cases'].rolling(window=5).mean()

    #calculation 3: Normalizing and Scaling the Data for Price
    df['price_normalized'] = df['price'] / df['price'].max()

    #calculation 4: Normalizing and Scaling the Data for Cases (we are taking a 6 day window because of testing times and reporting delays, amongst other factors)
    df['cases_normalized'] = df['cases_5day'] / df['cases'].rolling(window = 6, center=True).max()

    #calculation 5: Rolling 5 day average for normalized price
    df['price_n_5day'] = df['price_normalized'].rolling(window=5).mean()

    #calculation 6: Rolling 5 day average for normalized cases
    df['cases_n_5day'] = df['cases_normalized'].rolling(window=5).mean()


    fig, (price_5day, cases_5day, normalized) = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))
    fig.subplots_adjust(wspace=0.5, hspace=0.5, left=0.1, right=0.9, bottom=0.1, top=0.9)

    # plot the 5 day rolling average of price column on the first subplot
    df['price_5day'].plot(ax = price_5day)
    price_5day.set_xlabel('Days Since Lockdown')
    price_5day.set_ylabel('Price')
    price_5day.set_title('5-day Rolling Average of Stock Price v Days Since Lockdown')
    price_5day.legend()

    # plot the 5 day rolling average of cases column on the second subplot
    df['cases_5day'].plot(ax = cases_5day)
    cases_5day.set_xlabel('Days Since Lockdown')
    cases_5day.set_ylabel('Cases')
    cases_5day.set_title('5-day Rolling Average of Cases v Days Since Lockdown')
    cases_5day.legend()

    # plot the normalized stock and cases columns on the third subplot to identify correlations
    df['price_n_5day'].plot(ax = normalized)
    df['cases_n_5day'].plot(ax = normalized)
    normalized.set_xlabel('Days Since Lockdown')
    normalized.set_ylabel('Scaled Value')
    normalized.set_title('5-day Rolling Average of Normalized Stock and Cases v Days Since Lockdown')
    normalized.legend()

    plt.savefig("Graphs.png", bbox_inches="tight")
    plt.show()
    f.close()
    return
    
main()