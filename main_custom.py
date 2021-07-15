'''
    # development 1
    in stead of searching on the entire corpus 
    only those docs are selected (based on inverted list)
    where at least two of the tᵢ's occur (st tᵢ \in q)
    expectation: 
        - it will reduce the net run time 
        - more accuracy, cuz P(having a relevant doc would increase)

    # development 2
    say two clusters: c₁(t₁) and c₂(t₂)
    while using the BM model a weight factor will be used
    weight(cᵢ) = 1/cᵢ
    hence, if len(c₁) > len(c₂), words from c₂ will be considered
    to be more 'valuable'
'''

import pickle
import re
import numpy as np
import relevant_func as rf
import time as t

root = r"C:\Users\rmukh\OneDrive\Desktop\Summer 21\summer_internship_21\Bengali-data"
fn = "bn.topics.76-125.2010.txt"
# marks to split the query
marks = [' ', ',', '-', '\'']

# opens the document id db and stores the data
with open("docid_db", 'rb') as f:
    doc_id = pickle.load(f)

# opens the query terms db and stores the data
with open("query_terms_based_stem_db_2", 'rb') as f:
    q_terms = pickle.load(f) 

# opens the co-occurrence based cluster and stores the data
with open('co_occ_cluster_2', 'rb') as f:
    co_occ_cluster = pickle.load(f)

# opens the inverted list and stores the data
with open("term_database_dict", 'rb') as f:
    term_db = pickle.load(f)
    
# opens the document length db and stores the data
with open("doc_len", 'rb') as f:
    doc_len = pickle.load(f)

'''
    accessing query file and stop word file, preparing the query bags
'''
# opening the query file
with open('\\'.join([root, fn]), 'r', encoding = 'utf8') as infile:
    text = infile.read().split('\n')

# opening the stop-word file
with open('\\'.join([root, "sw.txt"]), 'r', encoding = 'utf8') as f:
    stop_words = f.read().split('\n')

# exracting lines from the query file with <title> specifier
temp = [word_bag[7:-8] for word_bag in text if "<title>" in word_bag][25:]

# init time
t_1 = t.time()

# preparing queries
index = 26
# already done: 0:5
for query in temp:
    # search result holder
    dic = dict()

    print("\n", index, "\n")
    query = re.split('|'.join(marks), query) 
    query = [i for i in query if i not in stop_words]

    '''     
        the searching operation 
    '''
    # case 1: raw query term search
    # extended_query = query

    # case 2: query term clusters, without co-occurrence estimation
    """ extended_query = []
    for term in query:
        extended_query += q_terms[term] """
    
    # case 3: query term clusters, re-done using co-occurrence estimation
    """ extended_query = []
    for term in query:
        extended_query += co_occ_cluster[term] """

    # case 4: using a customized bm model with different weights 
    # (ref: relevant func)
    extended_query = dict()
    bag_of_query_words = []

    # finding the co-occurrence intersection of the words in a query
    for term in query:
        try:
            # query term clusters, re-done using co-occurrence estimation
            extended_query[term] = co_occ_cluster[term]
            bag_of_query_words += co_occ_cluster[term]
        except:
            continue

    possibly_rel_doc_id_holder = rf.set_of_possibly_rel_doc(bag_of_query_words, term_db).astype('int32')
    corpus_size = len(doc_id.keys())
    bm_score_array = np.empty((0,2))
    for _id in possibly_rel_doc_id_holder:
        print(round(_id*100/corpus_size,2), " % done", end = '\r')
        bm_val = rf.custom_bm_score_2(extended_query, _id, corpus_size, term_db, doc_len)
        bm_score_array = np.append(bm_score_array, [[_id, bm_val]], 0)
        ranking = bm_score_array[bm_score_array[:,1].argsort()[::-1]]

    '''
        storing results in a database
    '''

    for i in range(50):
        dic[int(ranking[i][0])] = ranking[i][1]

    with open(root + "\\search_res_custom_bm_2\\" + "query" + str(index), 'wb') as f: #<--- change the directory name accordingly
        pickle.dump(dic, f)

    index += 1

t_2 = t.time()
print("Time taken %.3f"%(t_2 - t_1))