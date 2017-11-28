import numpy as np
import pandas as pd



# Ebert Listings
def convert_year(row):
    try:
        year = int(row['Year'])
        return year
    except:
        return np.nan

def clean_ebert_listings(df):
    df['Year'] = df.apply(lambda x: convert_year(x), 1)

    return df

# Ebert Reviews
def convert_runtime(row):
    try:
        runtime = int(row['Runtime'])
        return runtime
    except:
        return np.nan

def clean_ebert_reviews(df):
    df['Runtime'] = df.apply(lambda x: convert_runtime(x), 1)

    return df

# IMDB Information
def convert_imdb_rating(row):
    try:
        rating = float(row['IMDB_Rating'])
        return rating
    except:
        return np.nan

def convert_rating_count(row):
    try:
        count = float(row['Rating_Count'].replace(',', ''))
        return count
    except:
        return np.nan

def user_review_count(row):
    try:
        count = float(row['User_Review_Count'].replace(',', ''))
        return count
    except:
        return np.nan

def critic_review_count(row):
    try:
        count = float(row['Critic_Review_Count'].replace(',', ''))
        return count
    except:
        return np.nan

def convert_metascore(row):
    try:
        score = float(row['Metascore'].strip())
        return score
    except:
        return np.nan

def convert_country(row):
    try:
        country = row['Country'].strip()
        return country
    except:
        return np.nan

def convert_release_date(row):
    try:
        rel_date = row['Release_Date'].strip()

        if 'TV' in rel_date:
            return np.nan
        else:
            try:
                rel_date = datetime.datetime.strptime(rel_date, "%d, %B, %Y")
                return rel_date
            except:
                return np.nan

    except:
        return np.nan

def convert_genre(row):
    try:
        genres = ', '.join(row['Genre_List'])
        return genres
    except:
        return np.nan

def convert_actors(row):
    try:
        actors = ', '.join(row['Stars_List'])
        return actors
    except:
        return np.nan

def clean_imdb(df):
    df['IMDB_Rating'] = df.apply(lambda x: convert_imdb_rating(x), 1)
    df['Rating_Count'] = df.apply(lambda x: convert_rating_count(x), 1)
    df['User_Review_Count'] = df.apply(lambda x: user_review_count(x), 1)
    df['Critic_Review_Count'] = df.apply(lambda x: critic_review_count(x), 1)
    df['Metascore'] = df.apply(lambda x: convert_metascore(x), 1)
    df['Country'] = df.apply(lambda x: convert_country(x), 1)
    df['Release_Date'] = df.apply(lambda x: convert_release_date(x), 1)
    df['Genre_List'] = df.apply(lambda x: convert_genre(x), 1)
    df['Stars_List'] = df.apply(lambda x: convert_actors(x), 1)

    return df
