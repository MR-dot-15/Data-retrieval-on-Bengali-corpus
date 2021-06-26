'''
    accesses the query file, picks out terms in the <title> specifier
    creates a database where future 'stemming' would happen
'''
import os
import pickle
import re

root = r"C:\Users\rmukh\OneDrive\Desktop\Summer 21\summer_internship_21\Bengali-data"
fn = "bn.topics.76-125.2010.txt"
# marks to split the query
marks = [' ', ',', '-']

# opening the query file
with open('\\'.join([root, fn]), 'r', encoding = 'utf8') as infile:
    text = infile.read().split('\n')

# opening the stop-word file
with open('\\'.join([root, "sw.txt"]), 'r', encoding = 'utf8') as f:
    stop_words = f.read().split('\n')

# query terms to be saved here
terms = dict()

# exracting lines from the query file with <title> specifier
temp = [word_bag[7:-8] for word_bag in text if "<title>" in word_bag][0:26]


for element in temp:
    # splitting each query title
    words = re.split('|'.join(marks), element)
    for word in words:
        if word not in terms.keys() and word not in stop_words:
            # storing the terms 
            terms[word] = []

# pickling the query terms db
with open('query_terms_based_stem_db', 'wb') as outfile:
    pickle.dump(terms, outfile)