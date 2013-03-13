import pprint
import nltk
import string

#funtions for isolaing features
#need to be altered to work with classifier(return values or alter dictionary?)

def avg_Length(text):

   sentences=nltk.sent_tokenize(text)
   
   #p=re.compile('[a-z][A-Z]')
   total=0
   for item in sentences:
      total+=len(item)
   return float(total)/len(sentences)

def hapax_find(text):

   fdist= nltk.probability.FreqDist(word.lower().strip(string.punctuation) for word in text.split())
   return fdist.hapaxes()

def acronym_count(text):
   count=0
   sentences=nltk.sent_tokenize(text)
   for sentence in sentences:
      for word in nltk.word_tokenize(sentence):
         if word.isupper() and len(word)>=3:
            count+=1
   return count

#makes arrays of various distributions
#sort out returns later
#probably shouldn't include this one doesn't return anything
def char_Dist(text):
   ignore=[' ','.']
   validchars=0
   chars=[0.0]*27
   charmap={
         'a':1,
         'b':2,
         'c':3,
         'd':4,
         'e':5,
         'f':6,
         'g':7,
         'h':8,
         'i':9,
         'j':10,
         'k':11,
         'l':12,
         'm':13,
         'n':14,
         'o':15,
         'p':16,
         'q':17,
         'r':18,
         's':19,
         't':20,
         'u':21,
         'v':22,
         'w':23,
         'x':24,
         'y':25,
         'z':26}
   nums=[0.0]*10
   punctuation=[0.0]*31
   punctmap={
         '!':0,
         '\'':1,
         '#':2,
         '$':3,
         '%':4,
         '&':5,
         '"':6,
         '(':7,
         ')':8,
         '*':9,
         '+':10,
         ',':11,
         '-':12,
         '/':13,
         ':':14,
         ';':15,
         '<':16,
         '=':17,
         '>':18,
         '?':19,
         '@':20,
         '[':21,
         ']':22,
         '\\':23,
         '^':24,
         '_':25,
         '`':26,
         '{':27,
         '|':28,
         '}':29,
         '~':30
         }
   total=0
   for letter in text:
      if(letter in ignore):
         continue
      total+=1
      if(letter.lower() in charmap):
         chars[charmap[letter.lower()]]+=1
      elif(letter.isdigit()):
         nums[int(letter)]+=1
      elif(letter in punctmap):
         punctuation[punctmap[letter]]+=1
      else:
         chars[0]+=1

   print(total)
   for i in range(len(chars)):
      chars[i]=chars[i]/float(total)
   for i in range(len(nums)):
      nums[i]=nums[i]/float(total)
   for i in range(len(punctuation)):
      punctuation[i]=punctuation[i]/float(total)

def unkown_char_freq(text):
   ignore=[' ','.']
   total=0
   count=0
   charmap={
         'a':1,
         'b':2,
         'c':3,
         'd':4,
         'e':5,
         'f':6,
         'g':7,
         'h':8,
         'i':9,
         'j':10,
         'k':11,
         'l':12,
         'm':13,
         'n':14,
         'o':15,
         'p':16,
         'q':17,
         'r':18,
         's':19,
         't':20,
         'u':21,
         'v':22,
         'w':23,
         'x':24,
         'y':25,
         'z':26}
   punctmap={
         '!':0,
         '\'':1,
         '#':2,
         '$':3,
         '%':4,
         '&':5,
         '"':6,
         '(':7,
         ')':8,
         '*':9,
         '+':10,
         ',':11,
         '-':12,
         '/':13,
         ':':14,
         ';':15,
         '<':16,
         '=':17,
         '>':18,
         '?':19,
         '@':20,
         '[':21,
         ']':22,
         '\\':23,
         '^':24,
         '_':25,
         '`':26,
         '{':27,
         '|':28,
         '}':29,
         '~':30
         }
   for letter in text:
      if(letter in ignore):
         continue
      total+=1
      if(letter.lower() not in charmap and not letter.isdigit() and letter not in punctmap):
         count+=1
   return float(count)/total

#percent of text is special chars
def special_char_freq(text):
   ignore=[' ','.']
   total=0
   count=0
   punctmap={
         '!':0,
         '\'':1,
         '#':2,
         '$':3,
         '%':4,
         '&':5,
         '"':6,
         '(':7,
         ')':8,
         '*':9,
         '+':10,
         ',':11,
         '-':12,
         '/':13,
         ':':14,
         ';':15,
         '<':16,
         '=':17,
         '>':18,
         '?':19,
         '@':20,
         '[':21,
         ']':22,
         '\\':23,
         '^':24,
         '_':25,
         '`':26,
         '{':27,
         '|':28,
         '}':29,
         '~':30
         }
   for letter in text:
      if(letter in ignore):
         continue

      total+=1
      if(letter in punctmap):
         count+=1
   
   return float(count)/total
