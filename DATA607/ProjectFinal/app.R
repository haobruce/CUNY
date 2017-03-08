####################################################################################################
# background
####################################################################################################

library(shiny)
library(recommenderlab)
library(dplyr)
library(stringr)

#setwd("~/Google Drive/CUNY/git/DATA607/ProjectFinal")
#setwd("C:/Users/bhao/Google Drive/CUNY/git/DATA607/ProjectFinal")
ratings_path = file.path('ml-latest-small', 'ratings.csv')
movies_path = file.path('ml-latest-small', 'movies.csv')
ratings = read.csv(ratings_path, stringsAsFactors = FALSE)
movies = read.csv(movies_path, stringsAsFactors = FALSE)

# create year column
movies = movies %>% mutate(year = as.integer(str_extract(title, "([[:digit:]]{4})")))

# limit to more recent movies
ratings = ratings %>% 
  left_join(movies, by = 'movieId') %>%
  filter(year >= 2010) %>%
  select(userId, movieId, rating, timestamp)

movies = movies %>%
  filter(year >= 2010) %>%
  arrange(title)

genres = movies$genres
genres = str_split(genres, "\\|", simplify = TRUE)
genres = as.character(genres)
genres = sort(unique(genres))

# recommenderLab
i = paste0('u', ratings$userId)
j = paste0('m', ratings$movieId)
x = ratings$rating

df = data.frame(i, j, x, stringsAsFactors = T)

# interesting that as.integer works on character vector
sparse_matrix = sparseMatrix(as.integer(df$i), as.integer(df$j), x = df$x)
colnames(sparse_matrix) = levels(df$j)
rownames(sparse_matrix) = levels(df$i)

# create recommenderLab real rating object
real_ratings = new('realRatingMatrix', data = sparse_matrix)

# create recommender model
model_ubcf = Recommender(real_ratings, method = 'UBCF', param = list(normalize = 'center'))



####################################################################################################
# ui
####################################################################################################

ui = fluidPage(
  
  # Custom css               
  tags$head(
    tags$style(HTML('.selectize-input {
                        white-space: nowrap;
                    }
                    .selectize-dropdown {
                        width: 660px !important;
                    }'
    ))
  ),
  
  titlePanel('Movie Recommendations'),
  
  sidebarLayout(
    sidebarPanel(
     h4('Instructions:'),
     tags$p('1. Use filters to narrow movie selection'),
     tags$p('2. Select movie name and rating using dropdown menus'),
     tags$p('3. Click add rating to add movie and rating to user movie ratings'),
     tags$p('4. Click see recommendations after completing movie selection and ratings'),
     tags$p('5. Refresh the page to reset app'),
     tags$hr(),
      
     sliderInput('yearInput', 'Filter movie year', 2010, 2016, c(2010, 2016), sep = ''),
     selectInput('genreInput', 'Filter movie by genre', genres),
     htmlOutput('selectUI'),
     selectInput('ratingInput', 'Select rating (5 = best; 1 = worst)', seq(1.0, 5.0, 0.5)),
     actionButton('addRating', 'Add rating'),
     tags$p(),
     actionButton('seeRecommendation', 'See recommendations')
    ),
    
    mainPanel(
      tags$em(textOutput('error'), style = "color: red"),
      h4('Custom movie recommendations'),
      dataTableOutput('recommendations'),
      tags$hr(),
      h4('User movie ratings'),
      dataTableOutput('customSelections')
    )
  )
)



####################################################################################################
# ui
####################################################################################################

server = function(input, output) {
  
  searchResults = reactive({
    movies[movies$year %in% input$yearInput & 
           str_detect(movies$genres, input$genreInput) &
           !(movies$title %in% customDf$title)
           ,]
  })
  
  # create dynamic input options based on filters selected
  output$selectUI = renderUI({
    #selectInput('movieInput', 'Select movie name', searchResults()[,'title'])
    selectizeInput('movieInput', 'Select movie name', searchResults()[,'title'])
  })
 
  # action for addRating button
  customDf = data.frame()
  observeEvent(input$addRating, {

    # add selected movie and rating to custom data frame
    tmpDf = data.frame(title = input$movieInput, rating = input$ratingInput)
    # note the <<- which allows search to be made through parent environments
    customDf <<- rbind(tmpDf, customDf)
    output$customSelections = renderDataTable({ customDf },
                                              options = list(lengthMenu = c(10, 25, 50), 
                                                             pageLength = 10,
                                                             autoWidth = TRUE,
                                                             columnDefs = list(list(width = '15px', targets = c(1)))))
                
    # remove selected movie from available search results
    searchResults = reactive({
      movies[movies$year %in% input$yearInput & 
               str_detect(movies$genres, input$genreInput) &
               !(movies$title %in% customDf$title)
             ,]
    })
    output$selectUI = renderUI({
      #selectInput('movieInput', 'Select movie name', searchResults()[,'title'])
      selectizeInput('movieInput', 'Select movie name', searchResults()[,'title'])
    })
    
  }) 
  
  
  # action for seeRecommendation button
  observeEvent(input$seeRecommendation, {
    # check of ratings are varied
    if (length(unique(customDf$rating)) == 1) {

            output$error = renderText('Error: Please vary ratings to avoid errors.')

    } else {
      
      output$error = renderText('')
      custom_ratings_df = data.frame(title = customDf$title, rating = customDf$rating)
      custom_ratings_df$rating = as.numeric(custom_ratings_df$rating)
      
      # add movieId
      custom_ratings = custom_ratings_df %>% left_join(movies, by = 'title') %>%
        mutate(i = 'uCustom', j = paste0('m', movieId), x = rating) %>% select(i, j, x)
  
      custom_df = rbind(df, custom_ratings)
      custom_sparse_matrix = sparseMatrix(as.integer(custom_df$i), as.integer(custom_df$j), x = custom_df$x)
      colnames(custom_sparse_matrix) = levels(custom_df$j)
      rownames(custom_sparse_matrix) = levels(custom_df$i)
      
      # create real rating object
      custom_real_ratings = new('realRatingMatrix', data = custom_sparse_matrix)
      
      # make prediction using ubcf model
      custom_ubcf = predict(model_ubcf, n = 10, custom_real_ratings)
      custom_ubcf = as(custom_ubcf, 'list')$uCustom
      
      # check for valid prediction
      if (length(custom_ubcf) == 0) {
        
        output$error = renderText('Error: No recommendations found. Please make additional selections and rerun.')
        
      } else {
        
        output$error = renderText('')
        custom_ubcf = data.frame(rank = 1:10, movieId = as.integer(str_replace(custom_ubcf, 'm', '')))
        custom_ubcf = custom_ubcf %>% 
          left_join(movies, by = 'movieId') %>%
          select(rank, title)
        output$recommendations = renderDataTable({ custom_ubcf },
                                                 options = list(lengthMenu = c(10, 25, 50), 
                                                                pageLength = 10,
                                                                autoWidth = TRUE,
                                                                columnDefs = list(list(width = '15px', targets = c(0)))))
      }
    }
  })
}



####################################################################################################
# shinyApp
####################################################################################################

shinyApp(ui = ui, server = server)


