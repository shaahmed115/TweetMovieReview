from pyspark import SparkContext,SparkConf
#from pyspark.sql import Row
#from pyspark.sql import SQLContext
from pyspark.sql import *
import urllib
from pyspark.mllib.classification import LogisticRegressionWithLBFGS,LogisticRegressionModel
import os
from pyspark.mllib.feature import Word2Vec
from time import time
from pyspark.mllib.regression import LabeledPoint
from numpy import array
from classes.PosNeg import PosNegCount
from classes.WordVector import WordVectorAnalyzer
import nltk
import json
from nltk.tree import Tree
from geopy.geocoders import Nominatim

stop_words = nltk.corpus.stopwords.words('english')
stop_words+=['?','.','!',',']


#geolocator = Nominatim()

sparkConf = SparkConf().setMaster("local").setAppName("Predict").set("spark.app.id", "Predict")
sc = SparkContext(conf=sparkConf)
inp = sc.textFile("testing.txt").map(lambda row: row.split(" "))
word2vec = Word2Vec()
model = word2vec.fit(inp)
WordVectors = {}

for i in model.getVectors().keys():
    WordVectors[i] = model.findSynonyms(i,7)

Positive = open(os.getcwd() + "/positive.txt").read().splitlines()
Negative = open(os.getcwd() + "/negative.txt").read().splitlines()

sameModel = LogisticRegressionModel.load(sc, "model")

from pymongo import MongoClient
client = MongoClient('localhost:27017')
db=client.test
tweetList = []
tweets=db.tweetdb.find()
for tweet in tweets:
	l=[]
	entity_names = ""
	loc = ""
	if tweet.get('place'):
		loc=str(tweet['place']['full_name']).split(',')[-1]
		print loc
	text = tweet['text']	
	
	try:
		words = nltk.word_tokenize(text)
		tags = nltk.pos_tag(words)
		print_chunk = [chunk for chunk in nltk.ne_chunk(tags) if isinstance(chunk, Tree)]
		for chunk in print_chunk:
			if chunk.label() == "PERSON":
				words, tags = zip(*chunk.leaves())
				#print chunk.label() + '\t' +  '-'.join(words)
				#for word in words:
				#	entity_names.append(word.encode('utf-8'))
				entity_names = ','.join(map(str,words))
	except:
		entity_names=""
	posneg=float(PosNegCount(Positive,Negative).Sentiment(tweet['text'].encode('utf-8')))
	WV=float(WordVectorAnalyzer(stop_words,WordVectors,Positive,Negative).FindTweetSentiment(tweet['text'].encode('utf-8')))
	sentiment=sameModel.predict(array([WV,posneg]))
	l = (loc,entity_names,int(sentiment)-1)
	tweetList.append(l)
print tweetList	
sqlContext = SQLContext(sc)
#tweetRDD = sc.parallelize(tweetList).map(lambda x:Row(text=x[0],loc=x[1],sentiment=x[3]))
tweetRDD = sc.parallelize(tweetList).filter(lambda x:x[0] != "").map(lambda x :(x[0],x[2])).reduceByKey(lambda a,b:a+b).collect()
print tweetRDD
#schemaTweet= sqlContext.createDataFrame(tweetRDD,["loc","entity_names","sentiment"])
#schemaTweet.show(n=5)
