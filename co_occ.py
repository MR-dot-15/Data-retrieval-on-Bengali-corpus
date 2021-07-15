'''
    Constructs the co-occurrence database
'''
import pickle
import numpy as np
import re
root = r"C:\Users\rmukh\OneDrive\Desktop\Summer 21\summer_internship_21\Bengali-data"
fn = "bn.topics.76-125.2010.txt"

# marks to split the query
marks = [' ', ',', '-', '\'']

# query terms, clustered
with open("query_terms_based_stem_db_2", 'rb') as f:
    query_db = pickle.load(f)

# posting lists
with open("term_database_dict", 'rb') as f:
    term_db = pickle.load(f)

# query file
with open('\\'.join([root, fn]), 'r', encoding = 'utf8') as infile:
    text = infile.read().split('\n')

# stop-word file
with open('\\'.join([root, "sw.txt"]), 'r', encoding = 'utf8') as f:
    stop_words = f.read().split('\n')

# exracting lines from the query file with <title> specifier
temp = [word_bag[7:-8] for word_bag in text if "<title>" in word_bag][25:]

# co-occurrence matrix holder
coocc_mat = dict()
length = len(temp)
index = 1

for queries in temp:
    print("%.2f perc done"%(index * 100/ length), end = '\r')
    index += 1
    # splitting each query title
    queries = [word for word in re.split('|'.join(marks), queries)\
        if word not in stop_words]

    for word in queries:
        # the cluster
        extended_query_terms = query_db[word]
        # length of the cluster
        leng = len(extended_query_terms)
        # holds the co-occurrence matrix of a term
        co_occurrence_array_for_the_word = np.zeros((leng, leng))

        for i in range(leng):
            one_word = extended_query_terms[i]
            # posting list of "word"
            occurrence = term_db[one_word][:,0]

            for j in range(leng):
                another_word = extended_query_terms[j]
                # finding intersection of the posting lists 
                common_occurrence_no = len(np.intersect1d(occurrence, term_db[another_word][:,0]))
                # storing the common occurrence value
                co_occurrence_array_for_the_word[i,j] = common_occurrence_no

            # normalization   
            _max = np.amax(co_occurrence_array_for_the_word[i])
            co_occurrence_array_for_the_word[i] /= _max

        # entire the collection
        coocc_mat[word] = co_occurrence_array_for_the_word

# pickling
with open('co_occurrence_matrix_2', 'wb') as f:
    pickle.dump(coocc_mat, f)   
