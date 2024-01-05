from bs4 import BeautifulSoup
import requests
import csv
import os
import lxml

column_name = ['Entry Number', 'Name', 'Year', 'Duration', 'Movie Rating', 'Movie Score', 'Total votes']
csvfile = open('movie_data.csv', 'w', newline='', encoding='utf-8') 
csvwriter = csv.writer(csvfile)
csvwriter.writerow(column_name)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

website = requests.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250", headers=headers).text
soup = BeautifulSoup(website, 'lxml')
movies = soup.find_all('li', class_='ipc-metadata-list-summary-item sc-3f724978-0 enKyEL cli-parent')
c = 0

for movie in movies:
    name = movie.find('h3', class_='ipc-title__text').text.split('. ')[1:]
    name = "{}".format(*name)

    movie_data = movie.find_all('span', class_='sc-43986a27-8 jHYIIK cli-title-metadata-item')
    year = movie_data[0].text
    duration = movie_data[1].text

    try:
        movie_rated = movie_data[2].text
    except IndexError:
        movie_rated = "N/A"  

    rating_container = movie.find('div', class_='sc-9ab53865-0 bIaPYM sc-43986a27-2 bvCMEK cli-ratings-container')
    rating = rating_container.text.split()[0]
    count = rating_container.text.split()[1].strip("()")  

    c += 1

    csvwriter.writerow([c, name, year, duration, movie_rated, rating, count])

print(f"Done writing {c} entries to the csv file!")
csvfile.close()
