library(RCurl)
library(XML)
library(stringr)
library(tm)
library(SnowballC)
library(RWeka)
library(RTextTools)

setwd("~/Google Drive/CUNY/git/DATA607/Week10")
#setwd("C:/Users/bhao/Google Drive/CUNY/git/DATA607/Week10")

# download links to all press releases
all_links = character()
new_results = '/government/announcements?keywords=&announcement_filter_option=press-releases&topics%5B%5D=all&departments%5B%5D=all&world_locations%5B%5D=all&from_date=&to_date=01%2F07%2F2010'
signatures = system.file('CurlSSL', cainfo = 'cacert.pem', package = 'RCurl')

while(length(new_results) > 0) {
  new_results = str_c('https://www.gov.uk/', new_results)
  results = getURL(new_results, cainfo = signatures)
  results_tree = htmlParse(results)
  all_links = c(all_links, xpathSApply(results_tree, '//li[@id]//a', xmlGetAttr, 'href'))
  new_results = xpathSApply(results_tree, "//nav[@id='show-more-documents']//li[@class='next']//a",
                            xmlGetAttr, 'href')
}

# download press releases to local storage
for(i in 1:length(all_links)) {
  url = str_c('https://www.gov.uk/', all_links[i])
  tmp = getURL(url, cainfo = signatures)
  write(tmp, str_c('Press_Releases/', i, '.html'))
}

# create first text corpus
tmp = readLines('Press_Releases/1.html')
tmp = str_c(tmp, collapse = '')
tmp = htmlParse(tmp)
release = xpathSApply(tmp, "//div[@class = 'block-4']", xmlValue)

organisation = xpathSApply(tmp, "//div[@class = 'inner-heading']//
                           a[@class = 'organisation-link']", xmlValue)
publication = xpathSApply(tmp, "//div[@class = 'inner-heading']//
                           time[@class = 'date']", xmlValue)

release_corpus = Corpus(VectorSource(release))
meta(release_corpus[[1]], 'organisation') = organisation[1]
meta(release_corpus[[1]], 'publication') = publication

# append subsequent articles to text corpus
n = 1
for (i in 2:length(list.files('Press_Releases/'))){
  tmp = readLines(str_c('Press_Releases/', i, '.html'))
  tmp = str_c(tmp, collapse = '')
  tmp = htmlParse(tmp)
  release = xpathSApply(tmp, "//div[@class = 'block-4']", xmlValue)
  
  organisation = xpathSApply(tmp, "//div[@class = 'inner-heading']//
                             a[@class = 'organisation-link']", xmlValue)
  publication = xpathSApply(tmp, "//div[@class = 'inner-heading']//
                            time[@class = 'date']", xmlValue)
  
  if (length(release) != 0) {
    n = n + 1
    tmp_corpus = Corpus(VectorSource(release))
    release_corpus = c(release_corpus, tmp_corpus)
    meta(release_corpus[[n]], 'organisation') = organisation[1]
    meta(release_corpus[[n]], 'publication') = publication
  }
}

# extract meta information into data frame
meta_organisation = meta(release_corpus, type = 'local', tag = 'organisation')
meta_publication = meta(release_corpus, type = 'local', tag = 'publication')
meta_data = data.frame(organisation = unlist(meta_organisation), 
                       publication = unlist(meta_publication))

# filter out umbrella organisations and categories
release_corpus <- release_corpus[
  meta(release_corpus, tag = "organisation") == "Department for Business, Innovation & Skills" |
    meta(release_corpus, tag = "organisation") == "Department for Communities and Local Government" |
    meta(release_corpus, tag = "organisation") == "Department for Environment, Food & Rural Affairs" |
    meta(release_corpus, tag = "organisation") == "Foreign & Commonwealth Office" |
    meta(release_corpus, tag = "organisation") == "Ministry of Defence" |
    meta(release_corpus, tag = "organisation") == "Wales Office"        
  ]
table(meta_data[, 'organisation'])

# create term document matrix
tdm = TermDocumentMatrix(release_corpus)
tdm

# data cleansing
release_corpus = tm_map(release_corpus, removeNumbers)
#release_corpus = tm_map(release_corpus, str_replace_all, pattern = "[[:punct:]]", replacement = " ")
# book errata correction for line above
release_corpus <- tm_map(
  release_corpus, 
  content_transformer(
    function(x, pattern){
      gsub(
        pattern = "[[:punct:]]", 
        replacement = " ",
        x
      )
    }
  )
)

release_corpus = tm_map(release_corpus, removeWords, words = stopwords('en'))
#release_corpus = tm_map(release_corpus, tolower)
# book errata correction for line above
release_corpus <- tm_map(release_corpus, content_transformer(tolower))

# stemming
release_corpus = tm_map(release_corpus, stemDocument)

# remove sparse terms
tdm = removeSparseTerms(tdm, 1 - (10/length(release_corpus)))
tdm

# bigrams two word n-grams
BigramTokenizer <- function(x){
  NGramTokenizer(x, Weka_control(min = 2, max = 2))
}
tdm_bigram <- TermDocumentMatrix(release_corpus)
tdm_bigram

findAssocs(tdm, 'nuclear', 0.7)

# creating a document-term matrix
dtm = DocumentTermMatrix(release_corpus)
dtm = removeSparseTerms(dtm, 1-(10/length(release_corpus)))
dtm

org_labels <- unlist(meta(release_corpus, "organisation"))

N = length(org_labels)
container = create_container(dtm, labels = org_labels, 
                             trainSize = 1:400, testSize = 401:N, virgin = FALSE)
slotNames(container)

# estimation procedure
svm_model = train_model(container, 'SVM')
cross_validate(container, nfold = 10, algorithm = 'SVM')
tree_model = train_model(container, 'TREE')
cross_validate(container, nfold = 10, algorithm = 'TREE')
maxent_model = train_model(container, 'MAXENT')
cross_validate(container, nfold = 10, algorithm = 'MAXENT')

ensemble_model = train_model(container, nfold = 10, algorithm = c("SVM", "SLDA", "BOOSTING",
                                                    "BAGGING", "RF", "GLMNET", "TREE", "NNET", "MAXENT"), seed = NA,
               method = "C-classification", cross = 0, cost = 100, kernel = "radial",
               maxitboost = 100, maxitglm = 10^5, size = 1, maxitnnet = 1000, MaxNWts = 10000,
               rang = 0.1, decay = 5e-04, ntree = 200, l1_regularizer = 0, l2_regularizer = 0,
               use_sgd = FALSE, set_heldout = 0, verbose = FALSE)

cross_validate(container, nfold = 10, algorithm = c("SVM", "SLDA", "BOOSTING",
                                               "BAGGING", "RF", "GLMNET", "TREE", "NNET", "MAXENT"), seed = NA,
               method = "C-classification", cross = 0, cost = 100, kernel = "radial",
               maxitboost = 100, maxitglm = 10^5, size = 1, maxitnnet = 1000, MaxNWts = 10000,
               rang = 0.1, decay = 5e-04, ntree = 200, l1_regularizer = 0, l2_regularizer = 0,
               use_sgd = FALSE, set_heldout = 0, verbose = FALSE)

svm_out = classify_model(container, svm_model)
tree_out = classify_model(container, tree_model)
maxent_out = classify_model(container, maxent_model)
ensemble_out = classify_model(container, ensemble_model)

# evaluation
head(svm_out)
labels_out = data.frame(
  correct_label = org_labels[401:N], 
  svm = as.character(svm_out[,1]),
  tree = as.character(tree_out[,1]),
  maxent = as.character(maxent_out[,1]),
  ensemble = as.character(ensemble_out[,1]),
  stringsAsFactors = FALSE
)

# svm performance
table(labels_out[,1] == labels_out[,2])
prop.table(table(labels_out[,1] == labels_out[,2]))
# random forest performance
table(labels_out[,1] == labels_out[,3])
prop.table(table(labels_out[,1] == labels_out[,3]))
# maximum entropy performance
table(labels_out[,1] == labels_out[,4])
prop.table(table(labels_out[,1] == labels_out[,4]))
# ensemble performance
table(labels_out[,1] == labels_out[,5])
prop.table(table(labels_out[,1] == labels_out[,5]))
