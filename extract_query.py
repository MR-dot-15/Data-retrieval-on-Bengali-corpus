'''
    accesses the query file, picks out terms in the <title> specifier
    creates a database where future 'stemming' would happen
'''
import os
import pickle
import re
import relevant_func as rf
import numpy as np

root = r"C:\Users\rmukh\OneDrive\Desktop\Summer 21\summer_internship_21\Bengali-data"
fn = "bn.topics.76-125.2010.txt"
# marks to split the query
marks = [' ', ',', '-', '\'']
redundants = ['', ' ']

# opening the query file
with open('\\'.join([root, fn]), 'r', encoding = 'utf8') as infile:
    text = infile.read().split('\n')

# opening the stop-word file
with open('\\'.join([root, "sw.txt"]), 'r', encoding = 'utf8') as f:
    stop_words = f.read().split('\n')

# opening inverted list
with open('term_database_dict', 'rb') as inf:
    term_db = pickle.load(inf)
corpus_terms = list(term_db.keys())

# query terms to be saved here
terms = dict()

# exracting lines from the query file with <title> specifier
# already done up to 26th query (starting from 1)
temp = [word_bag[7:-8] for word_bag in text if "<title>" in word_bag]

query_id = 1
for element in temp:
    print(query_id, "%.2f"%(query_id*100/len(temp)), " % done", end = '\n')
    # query holder {query id: {bag of words in dict format}}
    query_specific_terms = dict()
    # splitting each query title
    words = re.split('|'.join(marks), element)
    index = 0
    # starts from 0 and slides ove entire the query term list
    # if it reaches the second last, the algo stops
    while index <= len(words) - 2:
        word, neighbor = words[index], words[index + 1]
        # at each steps checks if query is in the inverted list
        # if not replaces by the 'best-match' (basically prefix + suffix matching)
        # confidence score is always 1
        if word not in list(query_specific_terms) + stop_words + redundants:
            if word not in term_db:
                try:
                    best_match = rf.find_best_match(word, term_db)
                    query_specific_terms[best_match] = [1]
                except:
                    pass
            else:
                query_specific_terms[word] = [1]
                try:
                    best_match = rf.find_best_match(word, term_db)
                    if best_match not in words:
                        query_specific_terms[best_match] = [0]
                except:
                    pass
                
        # if ith word is not a sw or a blank space
        # checks the combination of i + (i+1)
        # if it's there in the inverted list, assigns a confidence score 1
        # otherwise finds the best match with confidence score 0
        if neighbor not in stop_words + redundants:
            bunch_word_neighbor = ''.join([word, neighbor])
            if bunch_word_neighbor in term_db:
                query_specific_terms[bunch_word_neighbor] = [1]
            else:
                try:
                    best_match = rf.find_best_match(bunch_word_neighbor, term_db)
                    if best_match in words:
                        pass
                    else:
                        query_specific_terms[best_match] = [0]
                except:
                    pass
        
        if neighbor not in stop_words + redundants:
            bunch_word_neighbor = '-'.join([word, neighbor])
            if bunch_word_neighbor in term_db:
                query_specific_terms[bunch_word_neighbor] = [1]
            try:
                best_match = rf.find_best_match(bunch_word_neighbor, term_db)
                if best_match in words:
                    pass
                else:
                    query_specific_terms[best_match] = [0]
            except:
                pass

        # handles the last step iteration
        if index == len(words) - 2:
            if neighbor not in list(query_specific_terms) + stop_words + redundants:
                if neighbor not in term_db:
                    try:
                        best_match = rf.find_best_match(neighbor, term_db)
                        query_specific_terms[best_match] = [1]
                    except:
                        pass
                else:
                    query_specific_terms[neighbor] = [1]
                    try:
                        best_match = rf.find_best_match(neighbor, term_db)
                        if best_match not in words:
                            query_specific_terms[best_match] = [0]
                    except:
                        pass
        index += 1
    print(query_specific_terms)
    terms[query_id] = query_specific_terms
    query_id += 1

# pickling the query terms db
with open('qterms_pref2_2', 'wb') as outfile:
    pickle.dump(terms, outfile)
