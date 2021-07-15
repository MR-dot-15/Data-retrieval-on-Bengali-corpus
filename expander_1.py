import pickle
import numpy as np
import relevant_func as rf

# opens the word in doc data
with open('word_in_doc', 'rb') as f:
    word_in_doc = pickle.load(f)

# opening the inverted list
with open('term_database_dict', 'rb') as f:
    term_db = pickle.load(f)

terms = ["বাংলাদেশ", "রাজনৈতিক"]
words = np.array(list(term_db.keys()))
words_for_term = np.array([])

# in the doc id vs terms in that doc database
# it finds all the terms that occurs with a certain term tᵢ
# in a certain document
for term in terms:
    _ids = term_db[term][:,0]
    for _id in _ids:
        words_for_term = np.union1d\
            (words_for_term, word_in_doc[_id])

print("step 1 done")
words_for_term = np.asarray(words_for_term, dtype = 'int32')

co_occ_matrix = np.empty((len(words_for_term), len(terms)))

# finding the co-occurrence vector 
# associated with a certain term 
# wrt all the terms found in the last step
words_to_operate = words[words_for_term]
for term_index in range(len(terms)):
    co_occ_matrix[:,term_index] = \
        rf.coocc_np(terms[term_index], words_to_operate, term_db)
    co_occ_matrix[:,term_index] = \
        co_occ_matrix[:,term_index] / rf.occ_np(words_to_operate, term_db)

print("step 2 done")

prod_of_co_occ_vec = np.ones_like(co_occ_matrix[:,0])
for i in range(len(terms)):
    prod_of_co_occ_vec *= co_occ_matrix[:, i]

x = prod_of_co_occ_vec.argsort()[::-1]
res = words[words_for_term[x]]
