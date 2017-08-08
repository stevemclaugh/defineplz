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


def get_englishfrench_triggerwords_separated():
    fe_trigger_words = {"english":[], "french":[]}
    with open("trigger_words.txt", "rU") as trigger_file:
        lines = trigger_file.readlines()
        for line in lines:
            words = line.split()
            if len(words) >= 2:
                spl_word = strip_punctuation_lowercase(words[0])
                fe_trigger_words["english"].append(spl_word)
                spl_word = strip_punctuation_lowercase(words[1])
                fe_trigger_words["french"].append(spl_word)
    return fe_trigger_words

def get_englishfrench_sentences_separated():
    fe_sentences = {"english":[], "french":[]}
    with open("english_french_sentences.txt", "rU") as sentence_file:
        lines = sentence_file.readlines()
        for line in lines:
            if len(line.strip()) == 0:
                continue
            sentences = line.split("\t")
            if len(sentences) >= 2:
                spl_sentence = strip_punctuation_lowercase(sentences[0])
                fe_sentences["english"].append(spl_sentence)
                spl_sentence = strip_punctuation_lowercase(sentences[1])
                fe_sentences["french"].append(spl_sentence)
    return fe_sentences


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
for i in range(30):
    tweet_stems = open('stem_list.txt').read().splitlines() #get_englishfrench_sentences_separated()
    trigger_words = get_englishfrench_triggerwords_separated()['english']
    used_trigger_words = open('used_trigger_words.txt').read().splitlines()
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    tweet_dict = twitter.search(q='#dh2017')
    #statuses = [{"text":'This bagel is fabulous.'}]
    statuses = tweet_dict['statuses']
    random.shuffle(statuses)
    #status = random.choice(statuses)
    for status in statuses:
        tweet_text = status['text'].strip()
        blob = TextBlob(tweet_text)
        for word in list(blob.words):
            if (word in trigger_words) & (word not in used_trigger_words):
                #print(word)
                stem = random.choice(tweet_stems)
                #print(stem)
                new_status_text = stem.replace('^^^^^', word)
                #print(new_status_text)
                tweet_id = status['id']
                try:
                    print(new_status_text + ' #DH2017')
                    break
                    break
                    break
                    #a = twitter.update_status(status=new_status_text, in_reply_to_status_id=tweet_id)
                    #print(a)
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
