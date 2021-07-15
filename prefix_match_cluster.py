import relevant_func as rf
import pickle
import numpy as np

with open('term_database_dict', 'rb') as inf:
    term_db = pickle.load(inf)

with open('qterms_pref2', 'rb') as f:
    qterms_db = pickle.load(f)

words = list(term_db.keys())

occurrence_np = np.frompyfunc(rf.occurrence, 2, 1)

for i in qterms_db:
    print("query %d"%(i), end = '\n')
    query_bag = qterms_db[i]
    base_words = [i for i in query_bag.keys() if query_bag[i][0] == 1]
    bag = list(query_bag.keys())
    for term in bag:
        """ if query_bag[term][0] == 1:
            variants = rf.co_occurrence_classifier(term, term_db)
            query_bag[term] += list(variants)
            if term not in query_bag[term]:
                    query_bag[term].append(term)
        else:
            co_occ_vector = rf.coocc_np(term, base_words, term_db)
            occ_vector = occurrence_np(base_words, term_db)
            probability = (co_occ_vector/occ_vector).sum()
            if probability > 0.5:
                variants = rf.co_occurrence_classifier(term, term_db)
                query_bag[term] += list(variants)
                if term not in query_bag[term]:
                    query_bag[term].append(term)
            else:
                query_bag.pop(term) """
        if query_bag[term][0] == 0:
            co_occ_vector = rf.coocc_np(term, base_words, term_db)
            occ = rf.occurrence(term, term_db)
            probability = (co_occ_vector/occ).sum()
            if probability < 1:
                query_bag.pop(term)

    
with open('qterms_pref2_2', 'wb') as inf:
    term_db = pickle.dump(qterms_db, inf)
