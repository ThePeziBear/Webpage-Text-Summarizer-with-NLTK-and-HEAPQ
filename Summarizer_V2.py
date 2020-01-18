# import necessary libraries

from urllib import request
from bs4 import BeautifulSoup as bs
import re
import nltk
from nltk.corpus import stopwords

import heapq


# Collect Data trough web scraping

url = 'https://en.wikipedia.org/wiki/Graz'

allContent = ""

htmlDoc = request.urlopen(url)

soupObject = bs(htmlDoc, 'html.parser')

Contents = soupObject.findAll('p')


for Content in Contents:
    allContent += Content.text

# Cleaning Data


allContent_CleanedData_1 = re.sub(r'\[[0-9]*\]', ' ', allContent)
allContent_CleanedData_2 = re.sub(r'\s+', ' ', allContent_CleanedData_1)
sentences_tokens = nltk.sent_tokenize(allContent_CleanedData_2)


sentences_tokens = nltk.sent_tokenize(allContent_CleanedData_2)

#Creating Sentence Token
    #tokenize_sents(strings)[source]_ Apply self.tokenize() to each element of strings. I.e.:
    # return [self.tokenize(s) for s in strings]
    #Return type list(list(str))

def sent_tokensize(self, strings):
    return [self.tokensize(allContent_CleanedData_2) for all_content in strings]
    nltk.sent_tokensize(allContent_CleanedData_2)


words_tokens = nltk.word_tokenize(allContent_CleanedData_2)


# Calculate the Frequency

stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}

for word in words_tokens:
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1


#calculate weightest frequency

maximum_frequency_word = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word]=(word_frequencies[word]/maximum_frequency_word)

#print(maximum_frequency_word)

print(word_frequencies)


# calculate Sentence score with each word weighted frequency

sentences_scores= {}

for sentence in sentences_tokens:
    for word in nltk.word_tokenize(sentence.lower()):
        if word in word_frequencies.keys():
            if len(sentence.split(' ')) < 30:
                if sentence not in sentences_scores.keys():
                    sentences_scores[sentence] = word_frequencies[word]
                else:
                    sentences_scores[sentence] += word_frequencies[word]

print(sentences_scores)

summary_machineLearning = heapq.nlargest(20,sentences_scores, key=sentences_scores.get)

print(summary_machineLearning)
