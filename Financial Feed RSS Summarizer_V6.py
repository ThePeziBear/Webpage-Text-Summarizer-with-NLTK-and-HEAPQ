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
    entry = NewsFeed.entries
    return NewsFeed


# Get Feed
def get_feed(url):
    feed = parse_feed('https://www.cnbc.com/id/10000664/device/rss/rss.html')
    for entry in feed.entries:
        url = entry.link
        htmlDoc = request.urlopen(url)
        soupObject = bs(htmlDoc, 'html.parser')

        # Get all Paragraphs
        allParagaphContent = ''
        paragraphsContents = soupObject.findAll('p')

    print(paragraphsContents)



def feed_to_string():
    for paragaphContent in paragraphsContents:
        allParagaphContent += (paragaphContent.text + ' ')

    allParagaphContent_CleanerData = re.sub(r'\[[0-9]*\]', ' ', allParagaphContent)
    allParagaphContent_CleanedData = re.sub(r'\s+', ' ', allParagaphContent_CleanerData)

    # Get Sentences from paragraphs
    tokens_sentences = nltk.sent_tokenize(allParagaphContent_CleanedData)

    # Get all Words
    allParagaphContent_CleanedData = re.sub(r'[^a-zA-Z]', ' ', allParagaphContent_CleanedData)
    allParagaphContent_CleanedData = re.sub(r'\s+', ' ', allParagaphContent_CleanedData)

    tokens_word = nltk.sent_tokenize(allParagaphContent_CleanedData)


    # Creating Sentence Token
    def sent_tokensize(self, strings):
        return [self.tokensize(allParagaphContent_CleanedData) for allParagaphContent in strings]
        nltk.sent_tokensize(allParagaphContent_CleanedData)


    words_tokens = nltk.word_tokenize(allParagaphContent_CleanedData.lower())

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
