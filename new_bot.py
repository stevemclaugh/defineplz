from twython import Twython
import time
import random
import string
from textblob import TextBlob

APP_KEY = "yYX1PmePymDUOleMXDkO0G6qt"
APP_SECRET = "bciq6fRGWx3Mgto6Hh3082bdSytuApkJ81h2HlAPOmx6uI9iz5"
OAUTH_TOKEN = "894946933449555968-h2hTsuaqlGUigG8n47QOTcK2YsVwhwa"
OAUTH_TOKEN_SECRET = "nn9PPiebrt8aKojohW8D9Oj5TTQHzEu2Xy8gf8GuRfKtK"

import os
os.chdir('/Users/mclaugh/Documents/GitHub/defineplz/')


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

def get_frenchenglish_triggerwords():
    fe_trigger_words = []
    with open("trigger_words.txt", "rU") as trigger_file:
        lines = trigger_file.readlines()
        for line in lines:
            words = line.split()
            for word in words:
                spl_word = strip_punctuation_lowercase(word)
                fe_trigger_words.append(spl_word)
    return fe_trigger_words


def find_keywords_in_tweets(p_tweets, p_trigger_words):
    found_tweets = []
    for t in p_tweets:
        spl_t = strip_punctuation_lowercase(t)
        t_words = spl_t.split()
        for word in t_words:
            if word in p_trigger_words:
                found_tweets.append(t)
    return found_tweets


while True:
	tweet_stems = open('stem_list.txt').read().splitlines()
	trigger_words = get_frenchenglish_triggerwords()
	used_trigger_words = open('used_trigger_words.txt').read().splitlines()

	twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	tweet_dict = twitter.search(q='#dh2017')

	#statuses = [{"text":'This bagel is fabulous.'}]
	statuses = tweet_dict['statuses']


	for status in statuses:
		tweet_text = status['text']
		blob = TextBlob(tweet_text)
		for word in list(blob.words):
			if (word in trigger_words) & (word not in used_trigger_words):
				stem = random.choice(tweet_stems)
				new_status_text = stem.replace('^^^^^', word)
				print(new_status_text)
				tweet_id = status['id']
                try:
                    a = twitter.update_status(status=new_status_text, in_reply_to_status_id=tweet_id)
                    print(a)
                except TwythonError as e:
                    print(e)
                #twitter.update_status(status='See how easy using Twython is!')
				with open('used_trigger_words.txt', 'a') as fo:
					fo.write(word)
					fo.write('\n')
                break
                break
    break
	time.sleep(700+(random.random()*600))








	for status in statuses:
		tweet_text = status['text']
		print(item['text'])

		blob = TextBlob(tweet_text)
		for word in blob.words:
			if (word in trigger_words) & (word not in used_trigger_words):

				stem = random.choice(tweet_stems)
				stem.replace('^^^^^', word)
				print(new_status_text)
				#twitter.update_status(status='See how easy using Twython is!')

				with open('used_trigger_words.txt', 'a') as fo:
					fo.write(trigger_word)
					fo.write('\n')

	time.sleep(700+(random.random()*600))
































#####
