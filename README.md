This project first streams from Twitter using a keyword list using Python tweepy the file script/Streamer.py and stores them in a mongo databases...
Using the movie name and a SPARQL query, the objects of rdfs_type:people related to the movie subject are identified from DBPedia.The query is specified in sparqlex.py...
Features are extracted on Word Vectors,patterns,positive negative words,PMI and a Logistic Regression using model is created with 77% accuracy for identifying tweet sentiment(pos,neg,neutral) using the spark mlib  library
Tweet sentences are tokenised and pos tagged to look for patterns.Features are defined as positive - negative word count,positive negative sentiment of word vector using scripts/Anayzer.py.
Using the model,features are extracted on testing samples and named entitiesa are identified and compared with the ones obtained from DBPedia.If the edit distance is smaller a threshold they are identified as the same and the predicate relation from DBPedia(Acting/Directing,etc.) is given a +1 or -1,based on the tweet rating identified using the Logistic Regression model.
The locations of the tweet are also identified from the json ['place']['fullname'] attribute
Using map reduce all the ratings are summed up using pyspark map-filter-reduce and visualisations made on the different categories and locations.

Requirements : ApacheSpark(1.6 or higher)
Python 2.7
Pyspark
SparkQL for querying DBPedia
 
