import nltk
from itertools import izip
import cPickle as pickle
import math
import string as st
from nltk.classify.maxent import TypedMaxentFeatureEncoding
from nltk.corpus import cmudict


d = cmudict.dict()
punctuation = ".,?!\"\':;"
stopwords = nltk.corpus.stopwords.words("english")

###CLASSIFIER###
def train():
    try:
        classif = pickle.load(open("./classifier.pickle", "r"))    
    except IOError:
        print "Could not load file."
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
def parse_training_dir():
    return [("5", "f{}f{fe}"), ("3", "w{}w{w}"), ("3", "w{erttttw{w}"), ("2", "w{{w}")]

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
def extract_text(xml):
    return "test"
    
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
    
def is_common(word):
    if word in stopwords:
        return True
    else:
        return False


def paragraph_features(xml):
    features = {}
    text = extract_text(xml)
    word_tokens = nltk.word_tokenize(text)
    sent_tokens = nltk.sent_tokenize(text)
    features["ave syllables per word"] = \
                            num_syllables(word_tokens)/len(word_tokens)
    features["ave sentence length"] = len(word_tokens)/len(sent_tokens)
    features["ave word length"] = len(word_tokens)/sum([len(word) \
                            for word in word_tokens])
    features["\% common words"] = len([1 for word in word_tokens\
                            if is_common(word)])/len(word_tokens)
    
    return features

#para list ("text text text", rating)
def paragraph_featuresets(para_list):
    return [(paragraph_features(w), int(s)) for (w, s) in para_list]



classifier = train()
print classify()
print rmse_class()
classifier.show_most_informative_features(10)