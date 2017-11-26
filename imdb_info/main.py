import json
import pickle
import subprocess

import pandas as pd
from sqlalchemy import create_engine

from scraping import scrape_imdb_listing

with open('../config.json') as f:
    mydata = json.load(f)

if __name__ == "__main__":
    print("")
    print("This program scrapes movie data from IMDB.")
    print("")

    # Scraping the third data set and storing it into pickle files and a SQL DB
    print("Beginining to scrape IMDB data. It will scrape 30 reviews per minute.")
    print("")

    # Postgres
    try:
        engine = create_engine('postgresql://' + mydata['username'] + ':' + mydata['password'] + '@' + mydata['URL'] + ':5432/postgres')
        df = pd.read_sql_query("SELECT * FROM ebert_listing;", engine, index_col='index')
    except:
        print("No database available.")
        print("")

    imdb_info, _ = scrape_imdb_listing(df)

    print("IMDB information scraping is complete.")
    print("")
    pickle.dump(imdb_info, open('../data/imdb_info.pkl', 'wb'))
    subprocess.call(["aws", "s3", "cp", "../data/imdb_info.pkl", "s3://k2-aws-tutorial/"])
    print("The raw data is stored in a pickle file.")
    print("")
    imdb_info.to_sql("imdb_info", engine, if_exists="replace")
    print("The data has been added to a inserted to the SQL database.")
    print("")
    print("Program complete.")
    print("")
