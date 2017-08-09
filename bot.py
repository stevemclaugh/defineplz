from twython import Twython
from textblob import TextBlob
import time
import datetime
import random
import string
import os

APP_KEY = "yYX1PmePymDUOleMXDkO0G6qt"
APP_SECRET = "bciq6fRGWx3Mgto6Hh3082bdSytuApkJ81h2HlAPOmx6uI9iz5"
OAUTH_TOKEN = "894946933449555968-h2hTsuaqlGUigG8n47QOTcK2YsVwhwa"
OAUTH_TOKEN_SECRET = "nn9PPiebrt8aKojohW8D9Oj5TTQHzEu2Xy8gf8GuRfKtK"

try: os.chdir(os.path.expanduser('~/Documents/GitHub/defineplz'))
except: pass

try: os.chdir('/home/defineplz/')
except: pass

def get_noun_phrases(p_text):
    blob = TextBlob(p_text)
    return list(blob.noun_phrases)

def get_noun_phrases_with_word(p_text, p_word):
    blob = TextBlob(p_text)
    noun_phrase_list = []
    for noun_phrase in blob.noun_phrases:
        if p_word in noun_phrase:
            noun_phrase_list.append(noun_phrase)
    return noun_phrase_list

def get_all_clichewords():
    fe_cliche_words = []
    with open("cliche_words.txt", "rU") as cliche_file:
        lines = cliche_file.readlines()
        for line in lines:
            words = line.split()
            for word in words:
                fe_cliche_words.append(word)
    return fe_cliche_words

def get_english_french_clichewords_separated():
    fe_cliche_words = {"english":[], "french":[]}
    with open("cliche_words.txt", "rU") as cliche_file:
        lines = cliche_file.readlines()
        for line in lines:
            words = line.split()
            if len(words) >= 2:
                spl_word = words[0].lower()
                fe_cliche_words["english"].append(spl_word)
                spl_word = words[1].lower()
                fe_cliche_words["french"].append(spl_word)
    return fe_cliche_words

def get_sentence_templates_separated():
    sentence_dict = {"english":[], "french":[]}
    lines = open("sentence_templates.txt", "rU").read().splitlines()
    for line in lines:
        if '|' in line:
            eng_sentence, fr_sentence = line.split("|")
            sentence_dict["english"].append(eng_sentence)
            sentence_dict["french"].append(fr_sentence)
    return sentence_dict

def get_matching_status(status_list):
    random.shuffle(status_list)
    for status_dict in status_list:
        tweet_id = status_dict['id']
        tweet_text = status_dict['text']
        blob = TextBlob(tweet_text)
        words = list(blob.words)
        random.shuffle(words)
        for word in words:
            if (word.lower() in eng_cliche_words) & \
                (word.lower() not in used_cliche_words) & \
                (tweet_id not in used_tweet_ids):
                return (tweet_id, word, status_dict)

#while True:
for i in range(1):
    if 7 <= datetime.datetime.now().time().hour <= 23:
        eng_sentence_templates = get_sentence_templates_separated()['english']
        eng_cliche_words = [item.lower() for item in get_english_french_clichewords_separated()['english']]
        used_cliche_words = [item.lower() for item in open('used_cliche_words.txt').read().splitlines()]
        used_tweet_ids = [int(item) for item in open('used_tweet_ids.txt').read().splitlines()]
        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        status_list = twitter.search(q='#dh2017', count=100)['statuses']
        try:
            tweet_id, word, status_dict = get_matching_status(status_list)
        except:
            continue
        status_text = status_dict['text']
        handle = '@' + status_dict['user']['screen_name']
        print('ORIGINAL: ' + status_text)
        new_status_text = ''
        while (len(new_status_text) == 0) | (len(new_status_text) > 140):
            sentence_template = random.choice(eng_sentence_templates)
            new_status_text = handle + ' ' + sentence_template.replace('^^^^^', word.lower()) + ' #dh2017'
        try:
            print('*** BOT POST *** ' + new_status_text)
            #a = twitter.update_status(status=new_status_text, in_reply_to_status_id=tweet_id)
            #pprint(a)
        except:
            print("** Error for this Tweet: **")
            print(new_status_text)
        #with open('used_cliche_words.txt', 'a') as fo:
            #fo.write(word + '\n')
        #with open('used_tweet_ids.txt', 'a') as fo:
            #fo.write(str(tweet_id) + '\n')
    #time.sleep(1200 + (random.random()*600))
