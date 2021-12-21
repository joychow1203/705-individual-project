# MA705 Final Project

The final dashboard is deployed on Heroku (https://joychow.herokuapp.com/).

## Dashboard Description

This dashboard allows users to explore 182 top-rated mystery and horror movies based on the following search criteria: 
1) Select a rating value to see all movies with this IMDB score and above. 
2) As a second criterion, select a year to see all movies released in this year and later.

The scatterplot and table present the matched results for rating and year. Users can hover over a dot to see movie details including its title, primary genre, the year in which the movie was released, its IMDB rating, and the number of votes on IMDB. The table shows more information such as the movie's synopsis and remarks from critics; users can also sort the results based on a certain column such as year. 

Additional feature: select a country to find directors who belong and have more than one movie on this list as well as the average score of a specific director's movies.

### Data Sources

Data were compiled from RottenTomatoes and IMDB database. Based on two movie lists published by RottenTomatoes, the specifics of these movies were collected from their respective pages through web scraping and converted into a cleaned data frame. Duplicates were removed since several movies were on both lists, resulting in 182 movies in total. IMDB basics and ratings were matched according to movies' unique IDs. The rating information was then matched to each of the 182 movies according to movie title and released year. Excel was used slightly in this process.

- Top 100 Mystery & Suspense Movies: https://www.rottentomatoes.com/top/bestofrt/top_100_mystery__suspense_movies/
- Top 100 Horror Movies: https://www.rottentomatoes.com/top/bestofrt/top_100_horror_movies/
- Movie basics and ratings on IMDB: https://www.imdb.com/interfaces/

### Areas of Improvement

- Was not successful at extracting critics/audience ratings from RottenTomatoes' flexbox elements. Would be better if this information can be integrated as well.
