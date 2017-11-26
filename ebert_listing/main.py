import json
import pickle

import pandas as pd
from sqlalchemy import create_engine

from scraping import scrape_eberts_listing

with open('../config.json') as f:
    mydata = json.load(f)

if __name__ == "__main__":
    print("")
    print("This program scrapes movie listing data from Roger Ebert's website.")
    print("")

    # Scraping first data set and storing it into pickle files and a SQL DB
    pages = int(input("How many pages would you like to scrape (24 movies per page)? "))
    print("Beginining to scrape movies.")
    print("")
    ebert_listing = scrape_eberts_listing()
    print("Movie scraping is complete.")
    print("")
    pickle.dump(ebert_listing, open('../data/ebert_listing.pkl', 'wb'))
    print("The raw data is stored in a pickle file.")
    print("")

    # Postgres
    try:
        engine = create_engine('postgresql://' + mydata['username'] + ':' + mydata['password'] + '@' + mydata['URL'] + ':5432/postgres')
        ebert_listing.to_sql('ebert_listing', engine, if_exists="replace")
    except:
        print("No database available.")
        print("")

    print("The data has been inserted to the SQL database.")
    print("")
    print("Program complete.")
    print("")
