from bs4 import BeautifulSoup
import requests
import csv
import os

column_name = ['Entry Number', 'Name', 'Year', 'Duration', 'Movie Rating', 'Movie Score', 'Total votes']
csvfile = open('movie_data.csv', 'w', newline='') 
csvwriter = csv.writer(csvfile)
csvwriter.writerow(column_name)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

website = requests.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250", headers=headers).text
soup = BeautifulSoup(website, 'lxml')
movies = soup.find_all('li', class_= 'ipc-metadata-list-summary-item sc-3f724978-0 enKyEL cli-parent')
c = 0
for movie in movies:
    name = movie.find('h3', class_= 'ipc-title__text').text.split('. ')[1:]
    name = "{}".format(*name) 

    movieData = movie.find_all('span', class_= 'sc-43986a27-8 jHYIIK cli-title-metadata-item') 

    year = movieData[0].text
    duration = movieData[1].text

    try:
        movieRated = movieData[2].text
    except IndexError:
        print("value does not exist")

    rating = movie.find('span', class_= 'ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating').text
    rating, count = rating.split()
    count = count.strip("()") # removing the parentheses
    
    c+=1 # to check whether we are able to properly scrape the data for all 250 movies

    
    csvwriter.writerow([c, name, year, duration, movieRated, rating, count]) 
    """ print(name)
    print(year)
    print(duration)
    print(movieRated)
    print(rating)
    print(count) """
   
print(f"Done writing {c} entries to the csv file!")
csvfile.close()