# MA 705 Individual Project

## Dashboard Description

This dashboard allows users to explore 182 top-rated mystery and horror movies based on the following search criteria: 
1) Select a rating value to see all movies with this score and above. The scatterplot presents the matched results on the timeline; users can hover over a dot to see movie details including its title, primary genre, the year in which the movie was released, IMDB rating, and the number of votes on IMDB. The table shows additional information such as the movie's synopsis and review from critics. 
2) Select a country to find out top directors who belong to that country and have more than one movie on the list as well as the average scores of their movies. 

### Data Cleaning
Data were compiled from RottenTomatoes and IMDB database. Based on two movie lists published by RottenTomatoes, the specifics of the movies included were collected from their respective pages and converted into a cleaned data frame. Duplicates were removed since several movies were included in both lists, resulting in 182 movies in total. IMDB ratings and votes were then matched with each movie. Excel was used slightly in this process.

### Data Sources and References
- Top 100 Mystery & Suspense Movies: https://www.rottentomatoes.com/top/bestofrt/top_100_mystery__suspense_movies/
- Top 100 Horror Movies: https://www.rottentomatoes.com/top/bestofrt/top_100_horror_movies/
- Movie basics and ratings on IMDB: https://www.imdb.com/interfaces/

### Dashboard Inspiration
I am passionate about thriller movies and have watched some of the movies on these lists.

### Potential Areas of Improvement
- Was not successful at extracting critics/audience ratings from RottenTomatoes' flexbox elements. Would be better if this information can be integrated as well. 
- Intended to use year range as a second criterion for filtering movies but encountered a non-type error. Would be better to have additional user input.
- A movie can belong to more than one genre, while only the primary genre was used in the plot. Would be well-rounded if this can be improved.
