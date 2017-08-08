from twython import Twython
import time
import random
import string
from textblob import TextBlob

APP_KEY = ""
APP_SECRET = ""
OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""



def strip_punctuation_lowercase(p_word):
    # Clear leading/trailing whitespace and punctuation, and make lowercase
    return p_word.strip().strip(string.punctuation).lower()

def noun_phrase_extract(p_text):
    from textblob import TextBlob
    blob = TextBlob(p_text)
    return blob.noun_phrases

def get_noun_phrases_with_word(p_text, p_word):
    from textblob import TextBlob
    blob = TextBlob(p_text)
    spl_word = strip_punctuation_lowercase(p_word)
    np_list = []
    for np in blob.noun_phrases:
        if spl_word in strip_punctuation_lowercase(np):
            np_list.append(np)
    return np_list


tweet_stems = open('stem_list.txt').read().splitlines()
trigger_words = "X" ##Parser goes here


while True:


	twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

	tweets = twitter.search(q='#dh2017')

	tweet = "Honestly, that they would host a conference banquet at a place with a dress code tells me I wouldn't want to attend #dh2017."

	for tweet in tweets:
		blob = TextBlob(tweet)
		for word in blob.words:
			if word in trigger_words:

				stem = random.choice(tweet_stems)


				twitter.update_status(status='See how easy using Twython is!')






	with open('used_trigger_words.txt', 'a') as fo:
		fo.write(trigger_word)
		fo.write('\n')

	time.sleep(700+(random.random()*600))
































#####
