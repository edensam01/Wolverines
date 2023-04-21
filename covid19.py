from covid19dh import covid19

x= covid19("USA", start = "2022-06-01", end = "2022-06-10")[0]

print(x)
l = list(zip(x['date'].dt.strftime('%Y-%m-%d'), x['confirmed']))

print(l)