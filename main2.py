import requests
import csv
from bs4 import BeautifulSoup

# Set up CSV file and write header
column_names = ['Entry Number', 'Name', 'Year', 'Duration', 'Movie Rating', 'Movie Score', 'Total votes']
with open('movie_data.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(column_names)

# Set up headers for the request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Make a request to the website and create a BeautifulSoup object
url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all movies on the page
movies = soup.find_all('li', class_='ipc-metadata-list-summary-item sc-3f724978-0 enKyEL cli-parent')

# Loop through each movie and extract data
for entry_number, movie in enumerate(movies, start=1):
    name = movie.find('h3', class_='ipc-title__text').text.split('. ')[1:]
    
    movie_data = movie.find_all('span', class_='sc-43986a27-8 jHYIIK cli-title-metadata-item')
    year = movie_data[0].text
    duration = movie_data[1].text

    try:
        movie_rated = movie_data[2].text
    except IndexError:
        movie_rated = "Not rated"

    rating = movie.find('span', class_='ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating').text.split()[0]

    vote_count = movie.find('span', class_='ipc-vote__verified-text').text.strip('()')

    # Write data to CSV
    with open('movie_data.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([entry_number, name, year, duration, movie_rated, rating, vote_count])

print(f"Done writing {entry_number} entries to the csv file!")
