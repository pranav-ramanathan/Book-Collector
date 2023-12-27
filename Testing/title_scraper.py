import requests
from bs4 import BeautifulSoup

url = 'https://www.patrickbetdavid.com/top-100-books/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract book titles from <a> tags
book_titles = [tag.text for tag in soup.find_all('a', href=True) if 'amazon.com' in tag['href']]

with open('book_titles.txt', 'w') as file:
    for title in book_titles:
        file.write(f"{title}\n")

print('Book titles saved to book_titles.txt')

