import nltk
from itertools import izip
import math
#from nltk.classify.maxent import TypedMaxentFeatureEncoding

###CLASSIFIER###
def train():
    processed = process_data()
    #encoding = TypedMaxentFeatureEncoding.train(processed['featuresets'], count_cutoff=3, alwayson_features=True)
    return nltk.MaxentClassifier.train(processed['featuresets'])

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
def load_training_data():
    l = []
    data = ["3 f{}f{f}", "4 w{}w{w}"]#process training data here
    for entry in data:
        rating, text = int(entry.split()[0]), entry.split()[1]
        l.append((text, rating))
    return l

def process_data():
    para_list = load_training_data()
    featuresets = paragraph_featuresets(para_list)

    return {
        'para_list': para_list,
        'featuresets': featuresets
    }
    
    

###FEATURES###
def paragraph_features(xml):
    features = {}
    '''
    words = nltk.word_tokenize(para)
    pos_list = nltk.pos_tag(words)

    sent_sum, char_len, neg_verb, pos_count = 0, 0, 0, 0
    for (word, tag) in pos_list:
        char_len += len(word)
        if 'VBD' in tag or 'VBN' in tag:
            neg_verb += 1
        if 'POS' in tag:
            pos_count += 1
        if '!' in word:
            features['contains(!)'] = 1
        if 'JJ' in tag or 'VB' in tag:
            features['contains(%s)' % word] = 1

    #features['avg word length'] = char_len/len(pos_list)
    features['neg verb'] = neg_verb
    features['pos_count'] = pos_count'''
    features['test'] = 1
    return features

#para list ("text text text", rating)
def paragraph_featuresets(para_list):
    return [(paragraph_features(w), s) for (w, s) in para_list]



classifier = train()
print classify()
print rmse_class()