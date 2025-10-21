import os
from bs4 import BeautifulSoup
from urllib.request import urlopen


print("working")
#get urls
mainUrl = "https://link.springer.com/journal/12065/volumes-and-issues/18-5"
htmlMain = urlopen(mainUrl).read()
soupMain = BeautifulSoup(htmlMain, 'html.parser')

print("phase one done")
urls = []
for h in soupMain.find_all('h3', class_='app-card-open__heading'):
    urls.append("https://link.springer.com" + h.find('a')['href'])

print(urls)

# for url in urls:
os.makedirs("Data", exist_ok=True)
for index, url in enumerate(urls):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h1', class_='c-article-title').text
    abstract = soup.find('div', class_='c-article-section__content').text
    with open(f"Data/D{index}.txt", "w") as f:
        f.write(title + "\n" + abstract)
