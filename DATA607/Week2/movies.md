Movies
================
Bruce Hao
September 3, 2016

Load necessary libraries.

``` r
library(dbConnect)
library(dplyr)
library(ggvis)
```

Establish database connection.

``` r
myDb = dbConnect(MySQL(), user=username, password=password, dbname='movies', host=host)
```

Query movie\_names and movie\_ratings tables.

``` r
rs = dbSendQuery(myDb, 'SELECT DISTINCT names.*, ratings.user_id, ratings.rating 
                 FROM movie_names names INNER JOIN movie_ratings ratings
                 ON names.movie_name = ratings.movie_name')
movies = fetch(rs, n=-1)
```

The following outputs show 1) the frequency of each rating value (1-5) by movie and 2) the average rating for each movie:

``` r
table(movies$movie_name, movies$rating)
```

    ##                               
    ##                                1 2 3 4 5
    ##   Deadpool                     0 2 1 1 1
    ##   Kung Fu Panda 3              0 2 1 0 2
    ##   Ride Along 2                 2 1 1 1 0
    ##   Star Wars: The Force Awakens 1 1 2 1 0
    ##   The Revenant                 1 1 1 1 1
    ##   Zootopia                     2 0 1 0 2

``` r
pvt = movies %>%
        group_by(movie_name) %>%
        summarise(avg_rating = mean(rating)) 
pvt
```

    ## # A tibble: 6 x 2
    ##                     movie_name avg_rating
    ##                          <chr>      <dbl>
    ## 1                     Deadpool        3.2
    ## 2              Kung Fu Panda 3        3.4
    ## 3                 Ride Along 2        2.2
    ## 4 Star Wars: The Force Awakens        2.6
    ## 5                 The Revenant        3.0
    ## 6                     Zootopia        3.0

``` r
#pvt %>% ggvis(~movie_name, ~avg_rating) %>% layer_bars(width = 0.7)
```
