import requests
import time

import pandas as pd
from bs4 import BeautifulSoup

def scrape_movie_reviews(df):
    """
    Parses each individual review page and returns list of key attributes.
    :link = URL for review
    """
    scraped_list = list()

    for link in df['URL']:
        full_link = "http://www.rogerebert.com" + link
        webpage = requests.get(full_link).text
        soup = BeautifulSoup(webpage, 'lxml')

        try:
            mpaa = soup.find('p', {'class':'mpaa-rating'}).strong.text[6:]
        except:
            mpaa = ''

        try:
            runtime = int(soup.find('p', {'class':'running-time'}).strong.text[:3].strip())
        except:
            runtime = ''

        try:
            review = ' '.join([paragraph.text for paragraph in soup.find('div', {'itemprop':'reviewBody'}).find_all('p')])
        except:
            review = ''

        scraped_list.append([link, mpaa, runtime, review])

        time.sleep(0.25)

    df = pd.DataFrame(scraped_list, columns = ['URL', 'Rating', 'Runtime', 'Review'])

    return df, scraped_list
