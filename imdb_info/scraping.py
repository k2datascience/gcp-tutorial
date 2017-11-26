import requests
import re
import time

import pandas as pd
from bs4 import BeautifulSoup

def scrape_imdb_listing(df):
    """
    Searches IMDB, parses results and returns DataFrame.
    :df = DataFrame with movie titles
    """
    movie_list = list()

    for movie in df['Title']:
        base_url = 'http://www.imdb.com/find?q='
        url = base_url + movie +'&s=all'
        webpage = requests.get(url).text
        soup = BeautifulSoup(webpage, 'lxml')

        try:
            results = soup('table', {'class':'findList'})[0]
        except:
            continue

        title = results.find_all('tr')[0]
        link = title.find('a', href=True)['href']

        url = 'http://www.imdb.com' + link
        webpage = requests.get(url).text
        soup = BeautifulSoup(webpage, 'lxml')

        movie_title = soup.find('title')

        try:
            rate = soup.find('span', itemprop='ratingValue').text
        except:
            rate = ''

        try:
            count = soup.find('span', itemprop='ratingCount').text
        except:
            count = ''

        try:
            des = soup.find('meta',{'name':'description'})['content']
        except:
            des = ''

        try:
            metascore = soup.find('div', class_='metacriticScore').text
        except:
            metascore = ''

        try:
            reviews_count = soup.find('div', class_='titleReviewbarItemBorder')
            u_reviews = reviews_count.find_all('a')[0].text.split(' ')[0]
            c_reviews = reviews_count.find_all('a')[1].text.split(' ')[0]
        except:
            u_reviews = ''
            c_review = ''

        try:
            director = soup.find('span', itemprop='name').text
        except:
            director = ''

        try:
            country = soup.find('div', class_='subtext').find_all('a', title=True)[-1].text.split(' ')[-1]
            country = re.sub('[\(\)\{\}<>]', '', country)
        except:
            country = ''

        try:
            rel_date = (', ').join(soup.find('div', class_='subtext').find_all('a',
                                            title=True)[-1].text.split(' ')[:-1])
        except:
            rel_date = ''

        movie_list.append([movie, rate, count, des, metascore, u_reviews, c_reviews,
                       director, country, rel_date])

        time.sleep(0.25)


    df = pd.DataFrame(movie_list, columns = ['Title', 'IMDB_Rating', 'Rating_Count',
        'Description', 'Metascore', 'User_Review_Count', 'Critic_Review_Count',
        'Director', 'Country', 'Release_Date'])

    return df, movie_list
