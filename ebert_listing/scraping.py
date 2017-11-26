import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_eberts_listing(num_pages=10):
    """
    Parses through webpage with list of movies and returns DataFrame.
    :num_pages = Number of pages to go through
    """
    url = "http://www.rogerebert.com/reviews?great_movies=0&no_stars=0&title=Cabin+in+the+Woods&filtersgreat_movies%5D%5B%5D=&filters%5Bno_stars%5D%5B%5D=&filters%5Bno_stars%5D%5B%5D=1&filters%5Btitle%5D=&filters%5Breviewers%5D=&filters%5Bgenres%5D=&page={}&sort%5Border%5D=newest"
    pages = list(range(1, num_pages))
    links = [url.format(i) for i in pages]

    review_list = list()
    count = 0

    for link in links:
        webpage = requests.get(link).text
        soup = BeautifulSoup(webpage, 'lxml')
        all_movies = soup('figure', {'class':'movie review'})

        for movie in all_movies:
            url = movie.a.get('href')
            title = movie.find_all('a')[1].text
            stars = len(movie.find_all('i', {'class':'icon-star-full'})) + 0.5 * len(movie.find_all('i', {'class':'icon-star-half'}))

            try:
                year = movie.find('span', {'class':'release-year'}).text[1:-1]
            except:
                year = ''

            count += 1
            review_list.append([count, title, stars, year, url])


    df = pd.DataFrame(review_list, columns = ['ID', 'Title', 'EbertStars', 'Year', 'URL'])
    return df
