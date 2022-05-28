from collections import Counter
import os
import re

def words(text): return re.findall(r'\w+', text.lower())

corpus = 'corpus_sederhana.txt'
WORDS = Counter(words(open(corpus).read()))

def P(word):
    "Probability of `word`."
    N=sum(WORDS.values())
    return WORDS[word] / N

def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def strip_non_ascii(string,symbols):
    ''' Returns the string without non ASCII characters''' #isascii = lambda s: len(s) == len(s.encode())
    stripped = (c for c in string if 0 < ord(c) < 127 and c not in symbols)
    return ''.join(stripped)

def adaAngka(s):
    return any(i.isdigit() for i in s)

def fixTags(t):
    getHashtags = re.compile(r"#(\w+)")
    pisahtags = re.compile(r'[A-Z][^A-Z]*')
    tagS = re.findall(getHashtags, t)
    for tag in tagS:
        if len(tag)>0:
            tg = tag[0].upper()+tag[1:]
            proper_words = []
            if adaAngka(tg):
                tag2 = re.split('(\d+)',tg)
                tag2 = [w for w in tag2 if len(w)>0]
                for w in tag2:
                    try:
                        _ = int(w) # error if w not a number
                        proper_words.append(w)
                    except:
                        w = w[0].upper()+w[1:]
                        proper_words = proper_words+re.findall(pisahtags, w)
            else:
                proper_words = re.findall(pisahtags, tg)
            proper_words = ' '.join(proper_words)
            t = t.replace('#'+tag, proper_words)
    return t


# def cleanTweets(Tweets):
#     factory = StopWordRemoverFactory(); stopwords = set(factory.get_stop_words()+['twitter','rt','pic','com','yg','ga','https'])
#     factory = StemmerFactory(); stemmer = factory.create_stemmer()
#     for i,tweet in enumerate(tqdm(Tweets)):
#         txt = tweet['fullTxt'] # if you want to ignore retweets  ==> if not re.match(r'^RT.*', txt):
#         txt = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',' ',txt)# clean urls
#         txt = txt.lower() # Lowercase
#         txt = Tokenizer.tokenize(txt)
#         symbols = set(['@']) # Add more if you want
#         txt = [strip_non_ascii(t,symbols) for t in txt] #remove all non ASCII characters
#         txt = ' '.join([t for t in txt if len(t)>1])
#         Tweets[i]['cleanTxt'] = txt # this is not a good Python practice, only for learning.
#         txt = stemmer.stem(txt).split()
#         Tweets[i]['nlp'] = ' '.join([t for t in txt if t not in stopwords])
#     return Tweets

# def translate(txt,language='en'): # txt is a TextBlob object
#     try:
#         return txt.translate(to=language)
#     except:
#         return txt

# def get_nMax(arr, n):
#     indices = arr.ravel().argsort()[-n:]
#     indices = (np.unravel_index(i, arr.shape) for i in indices)
#     return [(arr[i], i) for i in indices]

# def filter_for_tags(tagged, tags=['NN', 'JJ', 'NNP']):
#     return [item for item in tagged if item[1] in tags]

# def normalize(tagged):
#     return [(item[0].replace('.', ''), item[1]) for item in tagged]

# def unique_everseen(iterable, key=None):
#     "List unique elements, preserving order. Remember all elements ever seen."
#     # unique_everseen('AAAABBBCCDAABBB') --> A B C D
#     # unique_everseen('ABBCcAD', str.lower) --> A B C D
#     seen = set()
#     seen_add = seen.add
#     if key is None:
#         for element in itertools.ifilterfalse(seen.__contains__, iterable):
#             seen_add(element)
#             yield element
#     else:
#         for element in iterable:
#             k = key(element)
#             if k not in seen:
#                 seen_add(k)
#                 yield element

# def lDistance(firstString, secondString):
#     "Function to find the Levenshtein distance between two words/sentences - gotten from http://rosettacode.org/wiki/Levenshtein_distance#Python"
#     if len(firstString) > len(secondString):
#         firstString, secondString = secondString, firstString
#     distances = range(len(firstString) + 1)
#     for index2, char2 in enumerate(secondString):
#         newDistances = [index2 + 1]
#         for index1, char1 in enumerate(firstString):
#             if char1 == char2:
#                 newDistances.append(distances[index1])
#             else:
#                 newDistances.append(1 + min((distances[index1], distances[index1+1], newDistances[-1])))
#         distances = newDistances
#     return distances[-1]

# def kataKunci(text):
#     #tokenize the text using nltk
#     wordTokens = nltk.word_tokenize(text)
#     #assign POS tags to the words in the text
#     tagged = nltk.pos_tag(wordTokens)
#     textlist = [x[0] for x in tagged]

#     tagged = filter_for_tags(tagged)
#     tagged = normalize(tagged)

#     unique_word_set = unique_everseen([x[0] for x in tagged])
#     word_set_list = list(unique_word_set)

#    #this will be used to determine adjacent words in order to construct keyphrases with two words

#     graph = buildGraph(word_set_list)
#     #pageRank - initial value of 1.0, error tolerance of 0,0001,
#     calculated_page_rank = nx.pagerank(graph, weight='weight')
#     #most important words in ascending order of importance
#     keyphrases = sorted(calculated_page_rank, key=calculated_page_rank.get, reverse=True)
#     #the number of keyphrases returned will be relative to the size of the text (a third of the number of vertices)
#     aThird = len(word_set_list) / 3
#     keyphrases = keyphrases[0:aThird+1]

#     #take keyphrases with multiple words into consideration as done in the paper - if two words are adjacent in the text and are selected as keywords, join them
#     #together
#     modifiedKeyphrases = set([])
#     dealtWith = set([]) #keeps track of individual keywords that have been joined to form a keyphrase
#     i = 0
#     j = 1
#     while j < len(textlist):
#         firstWord = textlist[i]
#         secondWord = textlist[j]
#         if firstWord in keyphrases and secondWord in keyphrases:
#             keyphrase = firstWord + ' ' + secondWord
#             modifiedKeyphrases.add(keyphrase)
#             dealtWith.add(firstWord)
#             dealtWith.add(secondWord)
#         else:
#             if firstWord in keyphrases and firstWord not in dealtWith:
#                 modifiedKeyphrases.add(firstWord)

#             #if this is the last word in the text, and it is a keyword,
#             #it definitely has no chance of being a keyphrase at this point
#             if j == len(textlist)-1 and secondWord in keyphrases and secondWord not in dealtWith:
#                 modifiedKeyphrases.add(secondWord)

#         i = i + 1
#         j = j + 1

#     return modifiedKeyphrases

# def Rangkum(text,M):
#     sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
#     sentenceTokens = sent_detector.tokenize(text.strip())
#     graph = buildGraph(sentenceTokens)
#     calculated_page_rank = nx.pagerank(graph, weight='weight')
#     #most important sentences in ascending order of importance
#     sentences = sorted(calculated_page_rank, key=calculated_page_rank.get, reverse=True)
#     #return a 100 word summary
#     summary = ' '.join(sentences[:M])
#     summaryWords = summary.split()
#     summaryWords = summaryWords[0:101]
#     summary = ' '.join(summaryWords)
#     return summary