'''
    Constructs the co-occurrence database
'''
import pickle
import numpy as np

with open("query_terms_based_stem_db", 'rb') as f:
    query_db = pickle.load(f)

with open("term_database_dict", 'rb') as f:
    term_db = pickle.load(f)

extended_query_terms = []
for word in query_db.keys():
    extended_query_terms += query_db[word]

coocc_mat = dict()
counter, leng = 0, len(extended_query_terms)
for word in extended_query_terms:
    print(counter*100.0/leng, "% done", end = '\r')
    occurrence = term_db[word]
    common_occurrence = []
    for another_word in extended_query_terms:
        common_occurrence_no = len(np.intersect1d(occurrence, term_db[another_word]))
        common_occurrence.append(common_occurrence_no)
    coocc_mat[word] = common_occurrence
    counter += 1

with open('co_occurrence_matrix', 'wb') as f:
    pickle.dump(coocc_mat, f) 