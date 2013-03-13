import nltk
from itertools import izip
import cPickle as pickle
import math
import string as st
from nltk.classify.maxent import TypedMaxentFeatureEncoding
from nltk.corpus import cmudict
import sys


d = cmudict.dict()
punctuation = ".,?!\"\':;"
stopwords = nltk.corpus.stopwords.words("english")

def create_common_list():
    common_file = open("./common-english-words.txt", "r")
    common_list = common_file.read().split(",")
    common_file.close()
    return common_list
    
commonwords = create_common_list()

def time_estimation(wiki_title, rating):
    return "4:33"




###CLASSIFIER###
def train():
    try:
        classif = pickle.load(open("./classifier.pickle", "r"))    
    except IOError:
        #Could not load file
        processed = process_data()
        
        encoding = TypedMaxentFeatureEncoding.train\
            (processed['featuresets'], count_cutoff=3, alwayson_features=True)
        classif = nltk.MaxentClassifier.train\
            (processed['featuresets'], encoding=encoding)
            
        pickle.dump(classif, open("./classifier.pickle","wb"))
    return classif


def classify():
    processed = process_data()
    
    test_fs, test_ratings = zip(*processed['featuresets'])
    
    return classifier.batch_classify(test_fs)
    
    
def classify_single(wiki_title, classifier):
    feature_set = paragraph_features(wiki_title)
    if feature_set is None:
        print "error"
    else:
        rating = classifier.classify(feature_set)
        #error check rating
        print "Rating: " + str(rating)
        print "Estimated Time to Read: " + time_estimation(wiki_title, rating)
    
    
###RMSE#
def rmse(a, b):
    if len(a) != len(b):
        raise ValueError('a and b must have same length')

    return math.sqrt(float(sum((x - y) ** 2 for x, y in izip(a, b))) / len(a))

def rmse_equal(a, b):
    if len(a) != len(b):
        raise ValueError('a and b must have same length')

    return math.sqrt(float(sum(0 if x == y else 1 for x, y in izip(a, b))) / len(a))
    
def rmse_class():
    processed = process_data()

    test_fs, test_ratings = zip(*processed['featuresets'])
    results = classifier.batch_classify(test_fs)

    print 'Actual:', test_ratings
    print 'Predicted:', results

    return rmse(test_ratings, results)



###TRAINING DATA###

#should return a list of tuples containing ("label", "query result")
def parse_training_dir():#STUB
    return [("5", "I live in a bank."), ("3", "This is a test string to show how to do things."), ("4", "This strong is also somewhat difficult to read."), ("2", "Why, writing this way, would one consider formal linguistics as a guide?")]

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
def extract_text(xml):#STUB
    return xml
    
    
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
    return len([1 for word in tokens if is_stopword(word)])

def common_count(tokens):
    return len([1 for word in tokens if is_common(word)])
    
def character_count(word_tokens):
    return sum([len(word) for word in word_tokens])


def paragraph_features(wiki_title):
    features = {}
    
    text = extract_text(wiki_title)
    
    word_tokens = nltk.word_tokenize(text)
    sent_tokens = nltk.sent_tokenize(text)
    
    features["ave syllables/word"] = num_syllables(word_tokens)/len(word_tokens)
    features["ave sentence length"] = len(word_tokens)/len(sent_tokens)
    features["ave word length"] = character_count(word_tokens)/len(word_tokens)
    features["\% common words"] = common_count(word_tokens)
    features["\% stop words"] = stopword_count(word_tokens) 
    return features

def paragraph_features_text(text):
    features = {}
    
    word_tokens = nltk.word_tokenize(text)
    sent_tokens = nltk.sent_tokenize(text)
    
    features["ave syllables/word"] = num_syllables(word_tokens)/len(word_tokens)
    features["ave sentence length"] = len(word_tokens)/len(sent_tokens)
    features["ave word length"] = character_count(word_tokens)/len(word_tokens)
    features["\% common words"] = common_count(word_tokens)
    features["\% stop words"] = stopword_count(word_tokens) 
    return features

#para list ("text text text", rating)
def paragraph_featuresets(para_list):
    return [(paragraph_features_text(w), int(s)) for (w, s) in para_list]



create_common_list()
classifier = train()

#if   - classify call for wikipedia article
#else - validation call
if len(sys.argv) > 1:
    classify_single(sys.argv[1], classifier)
else:
    
    print classify()
    print rmse_class()
    classifier.show_most_informative_features(10)
