from itertools import count
from urllib import request
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from lxml import etree
import re
import pandas as pd
import nltk
import heapq
import feedparser


# Takes a sentence and tokenizes it into words
# input: a string
# output:a list with the words in the sentence, the words are lowered
def sentence_tokenizer(sentence):
    #clean_1 = re.sub(r'\[[0-9]*\]', ' ', sentence)
    clean_2 = re.sub(r'[^a-zA-Z]', ' ', sentence.lower())
    clean_3 = re.sub(r'\s+', ' ', clean_2)
    clean_4 = nltk.word_tokenize(clean_3)
    return clean_4


# Reads a Feed from given url
# input: url as string
# output: Newsfeed as JSON element
def parse_feed(url):
    NewsFeed = feedparser.parse(url)
    return NewsFeed

#get the text from your xpath
def get_xpath_text(url, xpath):
    response = urlopen(url)
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)


    text = tree.xpath(xpath)
    textlist = ''
    if len(text) == 0 : return ''
    for line in text[0]:
        if (line.text == None): continue
        textlist += (line.text + ' ')
    return textlist

# Get Feed
def get_feed(feedurl):
    feed = parse_feed(feedurl)
    alltext =''
    for entry in feed.entries:
        feedtext= get_xpath_text(entry.link,'//*[@id="RegularArticle-ArticleBody-5"]/div[2]')
        alltext += (feedtext + ' ')
    return alltext

url = 'https://www.cnbc.com/id/10000664/device/rss/rss.html'
text = get_feed(url)

sentences = nltk.sent_tokenize(text)

words_tokens = sentence_tokenizer(text)

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
for sentence in sentences:
    tokens = sentence_tokenizer(sentence)
    clean_tokens = [word for word in tokens if word not in stopwords]
    length = len(clean_tokens)
    value = 0
    if length == 0:
        sentence_value = 0
    else:
        for word in clean_tokens:
            value = value + word_frequencies[word]
        sentence_value = value / length
    sentenceAndValue = sentenceAndValue.append({'Sentence': sentence, 'Value': sentence_value}, ignore_index=True)

summary_machineLearning = sentenceAndValue.sort_values('Value', ascending=False)
summary_machineLearning = summary_machineLearning.drop_duplicates()

summary_machineLearning = summary_machineLearning.head(10)
summary_machineLearning['Sentence'] = [re.sub(r'\"', '', clean) for clean in summary_machineLearning['Sentence'].values]
summary = ''
for sentence in summary_machineLearning['Sentence'].values:
    summary += (sentence + '\n')

print(summary)