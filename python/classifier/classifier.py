#! /usr/bin/env python
import nltk
from itertools import izip
import cPickle as pickle
import math
import string as st
from nltk.classify.maxent import TypedMaxentFeatureEncoding
from nltk.corpus import cmudict
import sys, os
import csv, string
import urllib, urllib2, re
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import plugins
from util import chunks, flatten


d = cmudict.dict()
punctuation = ".,?!\"\':;"
stopwords = nltk.corpus.stopwords.words("english")
os_path = os.getcwd() + '/python/classifier'

def create_common_list():
    common_file = open(os_path + "/common-english-words.txt", "r")
    common_list = common_file.read().split(",")
    common_file.close()
    return common_list
    
commonwords = create_common_list()

#215 wpm
def time_estimation(rating):
    text_len = len(text_time)
    total_sec = text_len*(10-rating)/107
    minutes = total_sec/60
    seconds = total_sec%60
    second_string = str(seconds)
    if seconds < 10:
        second_string = "0" + str(seconds)
    return str(minutes) + ":" + second_string




###CLASSIFIER###
def train():
    try:
        classif = pickle.load(open(os_path + "/classifier.pickle", "r"))    
    except IOError:
        #Could not load file
        processed = process_data()
        
        '''encoding = TypedMaxentFeatureEncoding.train\
            (processed['featuresets'], count_cutoff=3, alwayson_features=True)
        classif = nltk.MaxentClassifier.train\
            (processed['featuresets'], encoding=encoding)'''
        classif = nltk.MaxentClassifier.train(processed['featuresets'])   
        pickle.dump(classif, open(os_path + "/classifier.pickle","wb"))
    return classif


def classify():
    processed = process_data()
    
    test_fs, test_ratings = zip(*processed['featuresets'])
    
    return classifier.batch_classify(test_fs)
    
    
def classify_single(wiki_title, classifier):
    feature_set = paragraph_features(wiki_title)
    if feature_set is None:
        sys.stderr.write("error")
    else:
        rating = classifier.classify(feature_set)
        #error check rating
        print str(rating)
        print time_estimation(rating)
        
def nfold_cross_validate(data, n=4):
    data_chunks = chunks(data, len(data) / n)

    rmse_values = []
    for i in range(n):
        train_set = flatten(data_chunks[:i] + data_chunks[i + 1:])
        test_set = data_chunks[i]
        classif = nltk.MaxentClassifier.train(train_set)   
        
        test_fs, test_ratings = zip(*test_set)
        results = classif.batch_classify(test_fs)
        set_rmse = rmse(test_ratings, results)
        print 'RMSE: ', set_rmse

        rmse_values.append(set_rmse)
    
    print 'Average RMSE:', sum(rmse_values) / float(len(rmse_values))
    
    
###RMSE#
def rmse_class():
    processed = process_data()

    test_fs, test_ratings = zip(*processed['featuresets'])
    results = classifier.batch_classify(test_fs)
    print "Expected: " + str(results)
    print "Actual:   " + str(test_ratings)
    return rmse(test_ratings, results)

def rmse(a, b):
    if len(a) != len(b):
        raise ValueError('a and b must have same length')

    return math.sqrt(float(sum((x - y) ** 2 for x, y in izip(a, b))) / len(a))
 
    
###GET PAGE###

def get_page(url_title):
   url = 'http://en.wikipedia.org/wiki/' + url_title

   try:
      req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
      page = urllib2.urlopen(req).read()
      
      return page
   
   except Exception, e:
      return None

###TRAINING DATA###

#should return a list of tuples containing ("label", "query result")
def parse_training_dir():
    
    results = []

    with open(os_path + '/trainingset_short.tsv', 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        for row in csvreader:
            print "Processing {0}".format(row[0])
            results.append((str(int(row[1])), (get_page(re.search('wiki/(\S+)', row[0]).group(1)))))
    return results

def load_training_data():
    l = []
    data = parse_training_dir()
    for rating, text in data:
        l.append((text, rating))
    return l

#Loads series of query results to train on and associated feature sets
def process_data():
    para_list = load_training_data()
    featuresets = paragraph_featuresets(para_list)

    return {
        'para_list': para_list,
        'featuresets': featuresets
    }

###FEATURES###
def extract_text(page):
   if not page:
      return None
   
   try:
      ps = BeautifulSoup(page).findAll('p')
      ret = ''

      for p in ps:
         temp = str(p)

         #remove html tags
         temp = re.sub('\<.*?\>', '', temp)

         #remove citations
         temp = re.sub('\<.*?\>', '', temp)

         ret += temp
         ret += '\n'

      return BeautifulStoneSoup(ret, convertEntities="html", smartQuotesTo="html").contents[0]
   
   except Exception, e:
      print e
      return None
    
    
def num_syllables(tokens):
    syll = 0
    for word in tokens:
        strip_word = word.lower().strip(punctuation)
        if strip_word.isalpha():
            try:
                syll += [len(list(y for y in x if (y[-1] in st.digits))) \
                                for x in d[word.lower()]][0]
            except KeyError:
                syll += 1
        else:
            syll += 0
    return syll
    
def is_stopword(word):
    if word in stopwords:
        return True
    else:
        return False
        
def is_common(word):
    if word in commonwords:
        return True
    else:
        return False
        
def stopword_count(tokens):
    return float(len([1 for word in tokens if is_stopword(word)]))

def common_count(tokens):
    return float(len([word for word in tokens if is_common(word)]))
    
def character_count(word_tokens):
    return sum([len(word) for word in word_tokens])

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def paragraph_features(wiki_title):
    features = {}
    
    page = get_page(wiki_title)
    if not page:
       return None
    text = extract_text(page)
    
    global text_time
    text_time = text#used for time_estimation()

    word_tokens = nltk.word_tokenize(text)
    sent_tokens = nltk.sent_tokenize(text)

    
    features["ave syllables/word"] = num_syllables(word_tokens)/len(word_tokens)
    features["ave sentence length"] = len(word_tokens)/len(sent_tokens)
    features["ave word length"] = character_count(word_tokens)/len(word_tokens)
    features["percent common words"] = \
                        common_count(word_tokens)/len(word_tokens)
    features["percent stop words"] = \
                        stopword_count(word_tokens)/len(word_tokens)
    features["hapax legomenon"] = \
                        plugins.hapax_find(word_tokens)/len(word_tokens)
    features["acronym count"] = \
                        plugins.avg_acronym_count(word_tokens)/len(word_tokens)
    features["percent numbers"]= \
                        plugins.number_freq(word_tokens)/len(word_tokens)
                        
    return features

def paragraph_features_page(page):
    features = {}

    text = extract_text(page)
    word_tokens = nltk.word_tokenize(text)
    sent_tokens = nltk.sent_tokenize(text)
    
    features["ave syllables/word"] = num_syllables(word_tokens)/len(word_tokens)
    features["ave sentence length"] = len(word_tokens)/len(sent_tokens)
    features["ave word length"] = character_count(word_tokens)/len(word_tokens)
    features["percent common words"] = \
                        common_count(word_tokens)/len(word_tokens)
    features["percent stop words"] = \
                        stopword_count(word_tokens)/len(word_tokens)
    features["hapax legomenon"] = \
                        plugins.hapax_find(word_tokens)/len(word_tokens)
    features["acronym count"] = \
                        plugins.avg_acronym_count(word_tokens)/len(word_tokens)
    features["percent numbers"]= \
                        plugins.number_freq(word_tokens)/len(word_tokens)
    
    return features

#para list ("text text text", rating)
def paragraph_featuresets(para_list):
    return [(paragraph_features_page(w), int(s)) for (w, s) in para_list]



create_common_list()
classifier = train()

#if   - classify call for wikipedia article
#else - validation call
if len(sys.argv) > 1:
    if sys.argv[1] == "-v":
        nfold_cross_validate(process_data()['featuresets'], n=4)
    else:
        classify_single(sys.argv[1], classifier)
else:
    print rmse_class()
    classifier.show_most_informative_features(10)
