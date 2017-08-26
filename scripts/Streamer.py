import time
import numpy as np
import tweepy
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer

api_key="RoF9Qhnz3Y39sw05k4m7nja7x"
api_secret="hViTwMJdSBODyVQRAjtMd3eYrkCS0X3fvoHMtwCi2bOl2SXAxi"
access_token="734468284452622336-oAekH2StbBLZHSGsPbgFkdO1FuBkhPB"
access_token_secret="YpI4YTfJuCRaTiZQpyldaYqoRaoYYvIQDX0uSg3lcrZrC"
auth=tweepy.OAuthHandler(api_key,api_secret)
auth.set_access_token(access_token,access_token_secret)

#stop_words = stopwords.words('english')
#stop_words+=['?','.','!',',']

#def stopword_remove(tokens):
#	for token in tokens:
#		if token in stop_words:
#			print token
#			tokens.remove(token)
#	return tokens

from pymongo import MongoClient
client = MongoClient('localhost',27017)
db=client.test
api=tweepy.API(auth)
class listener(tweepy.StreamListener):
	def on_data(self, data):
		try:
			tweet=json.loads(data)
			tweet_lower = tweet['text'].lower()
			jsondata=json.loads(data)
			#print jsondata['text'].encode('utf-8')
			#print ('\n')
			db.tweetdb.insert(jsondata)
			return True
		except BaseException,e:
			print 'failed:',str(e)
			time.sleep(5)
			pass

	def on_error(self, status):

		print status
keyword_list = ["Dunkirk"] #track list
#keyword_list = ["Trump","Hillary","Clinton","Democrat","Republic","Donald"] #track list
auth = tweepy.OAuthHandler(api_key, api_secret) #OAuth object
auth.set_access_token(access_token, access_token_secret)
twitterStream = tweepy.Stream(auth, listener()) 
twitterStream.filter(track=keyword_list, languages=['en'])  #call the filter method to run the Stream Object
