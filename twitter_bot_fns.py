import string
from textblob import TextBlob

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