import pickle
root = r"C:\Users\rmukh\OneDrive\Desktop\Summer 21\summer_internship_21\Bengali-data"

""" with open('query_terms_based_stem_db', 'rb') as f:
    db = pickle.load(f) """

"""
with open('term_database_dict', 'rb') as f:
    db1 = pickle.load(f)"""

"""
with open('doc_len', 'rb') as f:
    db3 = pickle.load(f) """


with open('docid_db', 'rb') as f:
    db2 = pickle.load(f) 

#print(db2[75939], db2[75938])
""" for i in db2.keys():
    if "1070601_1desh2.pc.utf8" in db2[i]:
        print(i) """

""" with open(root + "\\search_res\\query2", 'rb') as f:
    db3 = pickle.load(f) """

with open('co_occurrence_matrix', 'rb') as f:
    db4 = pickle.load(f)
