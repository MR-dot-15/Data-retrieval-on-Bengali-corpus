import pickle
import relevant_func as rf
import numpy as np
root = r"C:\Users\rmukh\OneDrive\Desktop\Summer 21\summer_internship_21\Bengali-data"

with open('query_terms_based_stem_db', 'rb') as f:
    db = pickle.load(f) 

with open('qterms_pref2', 'rb') as f:
    d_b = pickle.load(f)

with open('qterms_pref2_cluster', 'rb') as f:
    d_b_1 = pickle.load(f)

with open('qterms_pref2_2', 'rb') as f:
    d_b_2 = pickle.load(f)
    
with open('term_database_dict', 'rb') as f:
    db1 = pickle.load(f) 

with open('doc_len', 'rb') as f:
    db3 = pickle.load(f) 


with open('docid_db', 'rb') as f:
    db2 = pickle.load(f)  

#print(db2[75939], db2[75938])
""" for i in db2.keys():
    if "1070601_1desh2.pc.utf8" in db2[i]:
        print(i) """

"""with open('co_occurrence_matrix', 'rb') as f:
    db4 = pickle.load(f)"""

with open('co_occ_cluster', 'rb') as f:
    db5 = pickle.load(f)

with open('co_occ_cluster_2', 'rb') as f:
    db6 = pickle.load(f)



