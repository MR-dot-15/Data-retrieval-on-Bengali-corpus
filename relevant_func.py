'''
    query -> query vector
    documents -> doc vector
    with-
    bm25 weightage
'''

import numpy as np
import pickle

# calculation of tf-idf factor
def calculate_tf_idf(term, docid, tot_doc, term_database):
    try:
        term_details = term_database[term]
        i = np.where(term_details[:, 0] == docid)[0][0]
        tot_doc_no = tot_doc
        doc_freq = np.size(term_details, 0)
        return\
            (term_details[i][1] * np.log(1.0*tot_doc_no/doc_freq)/np.log(10),\
                term_details[i][1])
    except:
        return (0, 0)

# calculation of b25 score
def calculate_bm_score(term_bag, docid, tot_doc, term_database, len_database):
    docid, tot_doc, term_db = docid, tot_doc, term_database
    k1, b = 1.2, 0.75
    bm_score = 0
    for term in term_bag:
        # tf-idf and tf
        (tf_idf, tf) = calculate_tf_idf(term, docid, tot_doc, term_db)
        # len doc_j/ avg len of docs in the corpus
        l_ratio = len_database[0][docid-1] / len_database[1]
        # the parameter portion in bm25
        par = (1 + k1) / (k1 * (1 - b + b * l_ratio) + tf)
        bm_score += tf_idf * par

    return bm_score