import json
import pickle
import subprocess

import pandas as pd
from sqlalchemy import create_engine

from scraping import scrape_movie_reviews

with open('../config.json') as f:
    mydata = json.load(f)

if __name__ == "__main__":
    print("")
    print("This program scrapes movie review data from Roger Ebert's website.")
    print("")

    # Scraping the second data set and storing it into pickle files and a SQL DB
    print("Beginining to scrape movie review data. It will scrape 70 reviews per minute.")
    print("")

    # Postgres
    try:
        engine = create_engine('postgresql://' + mydata['username'] + ':' + mydata['password'] + '@' + mydata['URL'] + ':5432/postgres')
        df = pd.read_sql_query("SELECT * FROM ebert_listing;", engine, index_col='index')
    except:
        print("No database available.")
        print("")

    ebert_reviews, _ = scrape_movie_reviews(df)

    print("")
    print("Movie review scraping is complete.")
    print("")
    pickle.dump(ebert_reviews, open('../data/ebert_reviews.pkl', 'wb'))
    subprocess.call(["aws", "s3", "cp", "../data/ebert_reviews.pkl", "s3://k2-aws-tutorial/"])
    print("The raw data is stored in a pickle file.")
    print("")
    ebert_reviews.to_sql('ebert_reviews', engine, if_exists="replace")
    print("The data has been added to a inserted to the SQL database.")
    print("")
    print("Program complete.")
    print("")
