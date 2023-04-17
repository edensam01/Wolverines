import requests
from bs4 import BeautifulSoup

url = 'https://www.zyxware.com/articles/4344/list-of-fortune-500-companies-and-their-websites'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find('table', {'class': 'table'})
rows = table.find_all('tr')

for row in rows:
    cols = row.find_all('td')
    if len(cols) == 3:
        company_name = cols[1].get_text()
        website = cols[2].get_text()
        print(f"Company name: {company_name}")
        print(f"Website: {website}")
        break