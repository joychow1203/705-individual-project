# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 20:06:43 2021

@author: joych
"""

import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from collections import Counter

# extract list of 100 mystery movies
headers = {'User-Agent': 'Safari'}
url_mystery = "https://www.rottentomatoes.com/top/bestofrt/top_100_mystery__suspense_movies/"

mystery_req = requests.get(url_mystery, headers=headers)
mystery_req.raise_for_status()

mystery = BeautifulSoup(mystery_req.text, 'html.parser')

mystery_info = mystery.select("a.unstyled.articleLink")

mystery_info_title = [mmovie.text.strip() for mmovie in mystery_info]
mystery_info_link = [mmovie.attrs['href'] for mmovie in mystery_info]

#print(mystery_info_title.index('Citizen Kane (1941)'))
#print(mystery_info_title.index('The Friends of Eddie Coyle (1973)'))

mystery_titles = mystery_info_title[53:153]
mystery_links = mystery_info_link[53:153]
mystery_links = ["https://www.rottentomatoes.com/" + link for link in mystery_links]


# extract list of 100 horror movies
url_horror = "https://www.rottentomatoes.com/top/bestofrt/top_100_horror_movies/"

horror_req = requests.get(url_horror, headers=headers)
horror_req.raise_for_status()

horror = BeautifulSoup(horror_req.text, 'html.parser')

horror_info = horror.select("a.unstyled.articleLink")

horror_info_title = [hmovie.text.strip() for hmovie in horror_info]
horror_info_link = [hmovie.attrs['href'] for hmovie in horror_info]

#print(horror_info_title.index('Us (2019)'))
#print(horror_info_title.index('28 Days Later (2003)'))

horror_titles = horror_info_title[53:153]
horror_links = horror_info_link[53:153]
horror_links = ["https://www.rottentomatoes.com/" + link for link in horror_links]


# finalize list

top_movies_titles = mystery_titles + horror_titles
top_movies_links = mystery_links + horror_links

#remove duplicates
#top_movies_titles = list(set(top_movies_titles))

movie_df = pd.DataFrame(list(zip(top_movies_titles, top_movies_links)), columns =['Title', 'Link'])

movie_df['Year'] = movie_df["Title"].apply(lambda x : x[-5:])
#movie_df.to_csv('movie_df.csv')


################################
# collect info from each movie
headers = {'User-Agent': 'Safari'}

"""
year_info=[]
genre_info=[]
runtime_info=[]
language_info=[]
director_info=[]
description_info=[]

for link in top_movies_links:
    movie_req = requests.get(link, headers=headers)
    movie_req.raise_for_status()
    movie_page = BeautifulSoup(movie_req.text, 'html.parser')
    basics_info = movie_page.select("li.meta-row.clearfix")
    for info in basics_info:
        details = [info.text.strip() for info in basics_info]
    for element in details:
        if "Genre" in element:
            genre_info.append(element)
        if "Original Language" in element:
            language_info.append(element)
        if "Director" in element:
            director_info.append(element)
        if "Runtime" in element:
            runtime_info.append(element)

info_df = pd.DataFrame({'Genre':genre_info, 'Original Language':language_info, "Duration":runtime_info, "Director":director_info}) 
info_df.to_csv('info_df.csv')
"""

# extract movie description
"""
description_info=[]

for link in top_movies_links:
    movie_req = requests.get(link, headers=headers)
    movie_req.raise_for_status()
    movie_page = BeautifulSoup(movie_req.text, 'html.parser')
    de_info = movie_page.select("div#movieSynopsis.movie_synopsis.clamp.clamp-6.js-clamp")
    for de1 in de_info:
        descriptions = [de1.text.strip() for de1 in de_info]
    description_info.append(descriptions)

description_df = pd.DataFrame({'Description':description_info})
description_df.to_csv('description_df.csv')
"""

# extract critics reviews
"""
critic_info=[]

for link in top_movies_links:
    movie_req = requests.get(link, headers=headers)
    movie_req.raise_for_status()
    movie_page = BeautifulSoup(movie_req.text, 'html.parser')
    critics = movie_page.select("p.what-to-know__section-body")
    for review in critics:
        reviews = [review.text.strip() for review in critics]
    critic_info.append(reviews)

critics_df = pd.DataFrame({'Critics Review':critic_info})
critics_df.to_csv('critics_df.csv')
"""

################################
# compile and clean movie dataframe

movie_df = pd.read_csv("/Users/joych/Desktop/movie_df.csv", index_col=0)
info_df = pd.read_csv("/Users/joych/Desktop/info_df.csv", index_col=0)
description_df = pd.read_csv("/Users/joych/description_df.csv", index_col=0)
critics_df = pd.read_csv("/Users/joych/Desktop/critics_df.csv", index_col=0)

allmovies = pd.concat([movie_df, info_df, description_df, critics_df], axis=1)

# clean titles
allmovies["Title"] = [title.split("(", 1)[0].strip() for title in allmovies["Title"]]
# clean years
allmovies["Year"] = [year[0:4] for year in allmovies["Year"]]

# clean genres
allmovies["Genre"] = [genre[6:].strip().replace("\n","").replace("  ","") for genre in allmovies["Genre"]]

# clean languages
allmovies["Original Language"] = [language.strip().replace("\n","")[18:] for language in allmovies["Original Language"]]

# clean durations
allmovies["Duration"] = [duration.replace("\n","")[9:].strip() for duration in allmovies["Duration"]]

# clean directors
allmovies["Director"] = [director.replace("\n","")[9:].strip().replace("  ","") for director in allmovies["Director"]]

# clean descriptions
allmovies["Description"] = [description[2:-2] for description in allmovies["Description"]]

# clean critics reviews
allmovies["Critics Review"] = [review[2:-23] for review in allmovies["Critics Review"]]


allmovies["Primary Genre"] = allmovies["Genre"]
allmovies["Primary Genre"] = [genre.split(",")[0] for genre in allmovies["Primary Genre"]]

allmovies["Year"] = pd.to_numeric(allmovies["Year"])

# identify the year range that a movie belongs to
conditions = [
    (allmovies["Year"] < 1951),
    (allmovies["Year"] >= 1951) & (allmovies["Year"] <1961),
    (allmovies["Year"] >= 1961) & (allmovies["Year"] <1971),
    (allmovies["Year"] >= 1971) & (allmovies["Year"] <1981),
    (allmovies["Year"] >= 1981) & (allmovies["Year"] <1991),
    (allmovies["Year"] >= 1991) & (allmovies["Year"] <2001),
    (allmovies["Year"] >= 2001) & (allmovies["Year"] <2011),
    (allmovies["Year"] >= 2011) & (allmovies["Year"] <2021),
    ]

values = ["Before 1950s","1951-1960","1961-1970","1971-1980","1981-1990","1991-2000","2001-2010","2011-2020",]
allmovies["Year Range"] = np.select(conditions, values)
allmovies.astype({'Year Range': 'string'}).dtypes

allmovies = allmovies.drop_duplicates(subset=['Link'])
#allmovies.to_csv('allmovies_final.csv')


################################
# use IMDB data to find ratings and votes
IMDBtitles = pd.read_csv("/Users/joych/Desktop/dashboard/basicsdata.tsv", sep='\t')
IMDBratings = pd.read_csv("/Users/joych/Desktop/dashboard/ratingsdata.tsv", sep='\t')

IMDBtitles = IMDBtitles[IMDBtitles.titleType == "movie"]
IMDBtitles.tconst = IMDBtitles.tconst.str.strip()
IMDBratings.tconst = IMDBratings.tconst.str.strip()

# join basics and ratings
movie_reference = pd.merge(IMDBtitles, IMDBratings, on="tconst", how="left")
movie_reference.to_csv('movie_reference.csv')

# used Excel to match movies to IMDB ratings and votes according to title and year


################################
# 2nd dataframe for top directors' ratings
# used Excel to assign country to each top director

movies = pd.read_csv("/Users/joych/Desktop/allmovies_final.csv", index_col=0)

director_list = movies['Director'].tolist()
director_count = Counter(director_list)

directors_df = pd.DataFrame.from_dict(director_count, orient='index').reset_index()
drating_df = movies.groupby("Director").mean("IMDB Rating").reset_index()

directors_rating = directors_df.merge(drating_df, left_on = 'index', right_on = 'Director')
directors_rating = directors_rating[["index", 0, "IMDB Rating"]]
directors_rating.columns = ["Director", "Count", "Average Rating"]

directors_rating = directors_rating.sort_values(["Count"], ascending=False)
directors_rating = directors_rating[directors_rating["Count"]>1]
directors_rating["Average Rating"] = directors_rating["Average Rating"].round(1)
