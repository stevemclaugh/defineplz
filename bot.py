from twython import Twython
from textblob import TextBlob
import urllib.request
import time
import datetime
import random
import string
import os
from pprint import pprint

APP_KEY = "yYX1PmePymDUOleMXDkO0G6qt"
APP_SECRET = ""
OAUTH_TOKEN = "894946933449555968-h2hTsuaqlGUigG8n47QOTcK2YsVwhwa"
OAUTH_TOKEN_SECRET = ""

try: os.chdir(os.path.expanduser('~/Documents/GitHub/defineplz'))
except: pass

try: os.chdir('/home/defineplz/')
except: pass

commmon_words_url = 'https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt'

response = urllib.request.urlopen(commmon_words_url)
data = response.read()
common_words = [item.lower() for item in data.decode('utf-8').splitlines()]


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
            eng_sentence = line.split("|")[0]
            sentence_dict["english"].append(eng_sentence)
            try:
                fr_sentence = line.split("|")[1]
                sentence_dict["french"].append(fr_sentence)
            except:
                pass
    return sentence_dict

def get_matching_status(status_list):
    random.shuffle(status_list)
    sentence_dict = get_sentence_templates_separated()
    for status_dict in status_list:
        tweet_id = status_dict['id']
        tweet_text = status_dict['text']
        blob = TextBlob(tweet_text)
        words = list(blob.words)
        random.shuffle(words)
        for word in words:
            if (word.lower() in eng_cliche_words) & \
                                (word.lower() not in used_cliche_words) & \
                                (tweet_id not in used_tweet_ids) & \
                                ("retweeted_status" not in status_dict):
                return (tweet_id, word, sentence_dict["english"], status_dict)
            elif (word.lower() in fr_cliche_words) & \
                                (word.lower() not in used_cliche_words) & \
                                (tweet_id not in used_tweet_ids) & \
                                ("retweeted_status" not in status_dict):
                return (tweet_id, word, sentence_dict["french"], status_dict)

def get_candidate_noun_phrase(status_dict):
    phrases = [status_dict['text']]
    blacklist = "http https #dh2017 dh2017 ’ s l… https rt re-"
    lol = [get_noun_phrases(item) for item in phrases]
    lol = [[item for item in phrase_list if (item.lower() not in blacklist)&(item.lower() not in common_words)] for phrase_list in lol]
    candidate_phrases = []
    for phrases in lol:
        for phrase in phrases:
            if ('#' not in phrase) & ('@' not in phrase) & \
                      ("’ " not in phrase) & ("http" not in phrase) & \
                      (". " not in phrase) & ("2017" not in phrase) & \
                      ("..." not in phrase) & ("/" not in phrase) & \
                      ("re-" not in phrase) & ('…' not in phrase):
                candidate_phrases.append(phrase.replace(" 's","'s").strip("'").strip('"'))
    return candidate_phrases







while True:
    #print('~~ Starting the while loop. ~~')
    #print(datetime.datetime.now().time())
    #print('\n')
    #try:
        time.sleep(0)
        print('******')
        if 7 <= datetime.datetime.now().time().hour <= 23:
            print('*****')
            eng_sentence_templates = get_sentence_templates_separated()['english']
            eng_cliche_words = [item.lower() for item in get_english_french_clichewords_separated()['english']]
            fr_cliche_words = [item.lower() for item in get_english_french_clichewords_separated()['french']]
            used_cliche_words = [item.lower() for item in open('used_cliche_words.txt').read().splitlines()]
            used_tweet_ids = [int(item) for item in open('used_tweet_ids.txt').read().splitlines()]
            twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
            status_list = twitter.search(q='#dh2017', count=100)['statuses']
            try:
                print('****')
                tweet_id, word, sentence_templates, status_dict = get_matching_status(status_list)
            except:
                print('***')
                continue
            status_text = status_dict['text']
            handle = '@' + status_dict['user']['screen_name']
            print('ORIGINAL: ' + status_text)
            noun_phrase = random.choice(get_candidate_noun_phrase(status_dict))
            new_status_text = ''
            i = 0
            while (len(new_status_text) == 0) | (len(new_status_text) > 140):  ## Risk of infinite loop here
                sentence_template = random.choice(sentence_templates)
                new_status_text = handle + ' ' + sentence_template.replace('^^^^^', noun_phrase) + ' #dh2017'
                i += 1
                if i > 1000: continue
            try:
                print('*** BOT POST *** ' + new_status_text)
                #a = twitter.update_status(status=new_status_text, in_reply_to_status_id=tweet_id)
                #pprint(a)
            except:
                print("** Error for this Tweet: **")
                print(new_status_text)
            with open('used_cliche_words.txt', 'a') as fo:
                #fo.write(word + '\n')
                fo.write(noun_phrase + '\n')
            with open('used_tweet_ids.txt', 'a') as fo:
                fo.write(str(tweet_id) + '\n')
        time.sleep(3100 + (random.random()*200))
    #except Exception as e:
    #    except Exception as e: print(e)
    #    time.sleep(3100 + (random.random()*200))

## Manual post
#a = twitter.update_status(status=new_status_text, in_reply_to_status_id=tweet_id)
