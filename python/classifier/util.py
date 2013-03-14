import itertools

def flatten(l):
    return list(itertools.chain.from_iterable(l))

def chunks(l, n):
    """Return a list of successive n-sized chunks from l."""
    return [l[i:i + n] for i in range(0, len(l), n)]

def bag_of_words(words):
    return dict((word, True) for word in words)
