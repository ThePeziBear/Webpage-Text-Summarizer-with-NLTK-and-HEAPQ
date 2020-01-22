from itertools import count
from urllib import request
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import nltk
import heapq
import feedparser


# Takes a sentence and tokenizes it into words
# input: a string
# output:a list with the words in the sentence, the words are lowered
def sentence_tokenizer(sentence):
    clean_1 = re.sub(r'\[[0-9]*\]', ' ', sentence.lower())
    clean_2 = re.sub(r'[^a-zA-Z]', ' ', clean_1)
    clean_3 = re.sub(r'\s+', ' ', clean_2)
    clean_4 = nltk.word_tokenize(clean_3)
    return clean_4


# Reads a Feed from given url
# input: url as string
# output: Newsfeed as JSON element
def parse_feed(url):
    NewsFeed = feedparser.parse(url)
    #entry = NewsFeed.entries
    return NewsFeed

def clean_paragraphs(paragraphs):
    allParagaphContent_CleanerData = re.sub(r'\[[0-9]*\]', ' ', paragraphs)
    allParagaphContent_CleanedData = re.sub(r'\s+', ' ', allParagaphContent_CleanerData)
    #Hier sind richtige Sätze mit Satzzeichen
    return allParagaphContent_CleanedData

def get_url_text(url):
    htmlDoc = request.urlopen(url)
    soupObject = bs(htmlDoc, 'html.parser')
    # Get all Paragraphs
    paragraphs = soupObject.findAll('p')

    allParagaphContents = ''
    for paragaphContent in paragraphs:
        allParagaphContents += (paragaphContent.text + ' ')
    richtigeSaetze = clean_paragraphs(allParagaphContents)
    
    return richtigeSaetze


# Get Feed
def get_feed(feedurl):
    feed = parse_feed(feedurl)

    alltext =''
    for entry in feed.entries:
        feedtext= get_url_text(str(entry.link))
        alltext += (feedtext + ' ')
    return alltext

url = 'https://www.cnbc.com/id/10000664/device/rss/rss.html'
text = get_feed(url)



allParagaphContent_CleanedData = re.sub(r'[^a-zA-Z]', ' ', text)
allParagaphContent_CleanedData = re.sub(r'\s+', ' ', allParagaphContent_CleanedData)
#Hier ist reiner Nudltext
nltk.download()
sentences = nltk.sent_tokenize(text)

tokens_word = nltk.sent_tokenize(text)


# Creating Sentence Token
def sent_tokensize(self, strings):
    return [self.tokensize(allParagaphContent_CleanedData) for allParagaphContent in strings]
    nltk.sent_tokensize(allParagaphContent_CleanedData)


words_tokens = nltk.word_tokenize(text.lower())

# Get useless words in english
stopwords = nltk.corpus.stopwords.words('english')

# Calculate the Frequency
word_frequencies = {}

for word in words_tokens:
    if word not in stopwords:
        if word in word_frequencies.keys():
            word_frequencies[word] += 1
        else:
            word_frequencies[word] = 1

sentences_scores = {}

sentenceAndValue = pd.DataFrame(columns={'Sentence', 'Value'})
for sentence in tokens_sentences:
    tokens = sentence_tokenizer(sentence.lower())
    clean_tokens = [word for word in tokens if word not in stopwords]
    length = len(clean_tokens)
    value = 0
    if length == 0:
        sentence_value = 0
    else:
        for word in clean_tokens:
            value = value + word_frequencies[word]
        sentence_value = value / length
    # sentenceAndValue.append((sentence_value,sentence))
    sentenceAndValue = sentenceAndValue.append({'Sentence': sentence, 'Value': sentence_value}, ignore_index=True)

summary_machineLearning = sentenceAndValue.sort_values('Value', ascending=False)
# summary_machineLearning = heapq.nlargest(10, sentenceAndValue, key=sentenceAndValue.get)
#print(summary_machineLearning.head(10))
print('Test')
