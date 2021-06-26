'''
    reads from the query file each query
    conducts the search using the on bm25 model
    stores the result in distinct pickle files insdie search_res

    all necessary functions in relevant_func.py
'''

import pickle
import re
import numpy as np
import relevant_func as rf

root = r"C:\Users\rmukh\OneDrive\Desktop\Summer 21\summer_internship_21\Bengali-data"
fn = "bn.topics.76-125.2010.txt"
# marks to split the query
marks = [' ', ',', '-']

'''
    database opening below-------------------------------------------------------------------
'''
# opens the document id db and stores the data
with open("docid_db", 'rb') as f:
    doc_id = pickle.load(f)

# opens the query terms db and stores the data
with open("query_terms_based_stem_db", 'rb') as f:
    q_terms = pickle.load(f)

# opens the inverted list and stores the data
with open("term_database_dict", 'rb') as f:
    term_db = pickle.load(f)
# opens the document length db and stores the data
with open("doc_len", 'rb') as f:
    doc_len = pickle.load(f)
'''
    -----------------------------------------------------------------------------------------
'''

'''
    accessing query file and stop word file, preparing the query bags------------------------
'''
# opening the query file
with open('\\'.join([root, fn]), 'r', encoding = 'utf8') as infile:
    text = infile.read().split('\n')

# opening the stop-word file
with open('\\'.join([root, "sw.txt"]), 'r', encoding = 'utf8') as f:
    stop_words = f.read().split('\n')

# exracting lines from the query file with <title> specifier
temp = [word_bag[7:-8] for word_bag in text if "<title>" in word_bag][0:26]

# preparing queries
index = 6
# already done: 0:4
for query in temp[5:6]:
    # search result holder
    dic = dict()

    print("\n", index, "\n")
    query = re.split('|'.join(marks), query) 
    query = [i for i in query if i not in stop_words]

    #the searching operation------------------------------------------------------------------

    extended_query = []
    for term in query:
        extended_query += q_terms[term]

    corpus_size = len(doc_id.keys())
    bm_score_array = np.empty((0,2))
    for _id in doc_id:
        print(round(_id*100/corpus_size,2), " % done", end = '\r')
        bm_val = rf.calculate_bm_score(extended_query, _id, corpus_size, term_db, doc_len)
        bm_score_array = np.append(bm_score_array, [[_id, bm_val]], 0)
        ranking = bm_score_array[bm_score_array[:,1].argsort()[::-1]]

    #storing results in a database-------------------------------------------------------------

    for i in range(20):
        dic[int(ranking[i][0])] = ranking[i][1]

    with open(root + "\\search_res\\" + "query" + str(index), 'wb') as f:
        pickle.dump(dic, f)

    index += 1
'''
    -----------------------------------------------------------------------------------------
'''
