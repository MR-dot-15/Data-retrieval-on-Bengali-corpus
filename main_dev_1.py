'''
    # description to be provided
'''
# total time taken = 4883.781 s
# query items = 50
# on avg 97.68 s

import pickle
import numpy as np
import relevant_func as rf
import time as t

root = r"C:\Users\rmukh\OneDrive\Desktop\Summer 21\summer_internship_21\Bengali-data"

# opens the co-occurrence based cluster and stores the data
with open('qterms_pref2_cluster', 'rb') as f:
    qt_cluster = pickle.load(f)

# opens the document id db and stores the data
with open("docid_db", 'rb') as f:
    doc_id = pickle.load(f)

# opens the inverted list and stores the data
with open("term_database_dict", 'rb') as f:
    term_db = pickle.load(f)
    
# opens the document length db and stores the data
with open("doc_len", 'rb') as f:
    doc_len = pickle.load(f)

'''
    qt_cluster has bags of query terms (pref match + co-occurrence)
    each bag has its query id as the key
'''
# init time
t_1 = t.time()

for query_id in qt_cluster:
    print("Query %i"%(query_id), end = '\n')

    # holds search results for iᵗʰ query
    dic = dict()

    # bag containing terms of iᵗʰ query 
    query_specific_bag = qt_cluster[query_id]

    # extracting all the terms in the query
    # to find probably relevant docs
    all_words_flattened = []
    for i in query_specific_bag:
        all_words_flattened += query_specific_bag[i][1:]

    # set of doc id-s where at least one term occurs
    possibly_rel_doc_id_holder = \
        rf.set_of_possibly_rel_doc(all_words_flattened, term_db).astype('int32')

    # # of docs
    corpus_size = len(doc_id.keys())
    # bm score holder
    bm_score_array = np.empty((0,2))

    '''
        bm score calculation
    '''

    for _id in possibly_rel_doc_id_holder:
        print(round(_id*100/corpus_size,2), " % done", end = '\r')
        # ref: relevant_func
        bm_val = rf.custom_bm_score_2(query_specific_bag, _id, corpus_size, term_db, doc_len, inst_weight = 0)
        bm_score_array = np.append(bm_score_array, [[_id, bm_val]], 0)
        ranking = bm_score_array[bm_score_array[:,1].argsort()[::-1]]

    '''
        storing results in a database
    '''
    # top 50 results to be stored
    for i in range(50):
        dic[int(ranking[i][0])] = ranking[i][1]

    with open(root + "\\search_res_ultimate_3\\" + "query" + str(query_id), 'wb') as f: 
    # ^^^^ change the directory name accordingly
        pickle.dump(dic, f)


t_2 = t.time()
print("Time taken %.3f"%(t_2 - t_1))