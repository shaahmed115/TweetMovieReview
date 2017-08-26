import nltk
import os

class WordVectorAnalyzer:
		def __init__(self,stop_words,WordVectors,Positive,Negative):
			self.WordVectors = WordVectors
			self.stop_words = stop_words
			self.Negative = Positive
			self.Positive = Negative
		def stopwords_remove(self,sentence):
			for word in sentence:
				if word in self.stop_words:
					sentence.remove(word)
				else:
					continue
			return sentence		


		def FindWordSentiment(self,word):
			pos_count=0
			neg_count=0
			try:
				synonyms=self.WordVectors[word]
			except KeyError:
				#print "Word not here"
				return 0
			for w in synonyms:
				if w[0] in self.Positive:
					pos_count+=1
				if w[0] in self.Negative:
					neg_count+=1
					
			#print pos_count
			#print neg_count
			if pos_count==neg_count:
				return 0.0
			return pos_count if (pos_count > ((-1) * neg_count)) else neg_count 	
			
		def FindTweetSentiment(self,sentence):
			TweetSentiment = 0
			text=nltk.word_tokenize(sentence.decode('utf-8'))
			tags=nltk.pos_tag(text)
			for i in tags:
				if i[1]== 'NN':
					#synonyms=model.findSynonyms(i[0],3)
					word_sentiment = self.FindWordSentiment(i[0])	
					TweetSentiment = TweetSentiment + word_sentiment
			if float(TweetSentiment) > float(0.0):
				return 2.0
			if float(TweetSentiment) < float(0.0):
				return 0.0
			else:
				return 1.0






			
