import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json


"""creating a json file containing all article urls for each volume"""

# MAIN_URL = "https://link.springer.com/journal/12065/volumes-and-issues"

# print('working')
# # get volumes
# htmlMain = urlopen(MAIN_URL).read()
# soupMain = BeautifulSoup(htmlMain, 'html.parser')
# volumes = soupMain.find_all('li',class_='app-vol-and-issues-item')
# print('volumes here')
# vol_dict={}
# for volume in volumes:
#     volume_name = volume.find('h2').find('span').text
#     volume_article_urls = []
#     for h in volume.find('ul').find_all('li'):
#         issueUrl  = "https://link.springer.com" + h.find('a')['href']
#         issueMain = urlopen(issueUrl).read()
#         soupIssue = BeautifulSoup(issueMain,'html.parser')
#         for h_2 in soupIssue.find_all('h3', class_='app-card-open__heading'):
#             volume_article_urls.append("https://link.springer.com" + h_2.find('a')['href'])
#     vol_dict[volume_name] = volume_article_urls

# with open("vol_urls.json", "w") as file:
#     json.dump(vol_dict, file, indent=4)


"""scraping titles and abstracts from article urls and saving them in text files"""

os.makedirs("Data", exist_ok=True)
with open("vol_urls.json", "r") as file:
    vol_dict = json.load(file)

for volume_name, urls in vol_dict.items():
    os.makedirs(f"Data/{volume_name}", exist_ok=True)
    for index, url in enumerate(urls):
        html = urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h1', class_='c-article-title').text
        abstract = soup.find('div', class_='c-article-section__content').text
        with open(f"Data/{volume_name}/article_{(index+1):02d}.txt", "w") as file:
            file.write(title + ".\n" + abstract)
