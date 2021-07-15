import numpy as np
import pickle
import relevant_func as rf

root = r"C:\Users\rmukh\OneDrive\Desktop\Summer 21\summer_internship_21\Bengali-data"

# opens the co-occurrence based cluster and stores the data
with open('qterms_pref2_cluster', 'rb') as f:
    qt_cluster = pickle.load(f)

# opens the inverted list and stores the data
with open("term_database_dict", 'rb') as f:
    term_db = pickle.load(f)

# all the terms in the corpus
corpus_terms = np.array(list(term_db.keys()))

# opens the term index vs doc id dataset
with open("word_in_doc", 'rb') as f:
    word_in_doc = pickle.load(f)

with open('expansion', 'rb') as f:
    expansion = pickle.load(f)

# opens the document id db and stores the data
with open("docid_db", 'rb') as f:
    doc_id = pickle.load(f)
    
# opens the document length db and stores the data
with open("doc_len", 'rb') as f:
    doc_len = pickle.load(f)
    
# accessing the relevance list 
with open("rel_list.txt", 'r') as f:
    relevance_list = f.read().split('\n')

relevance_list = [i.split(' ') for i in relevance_list]

# "1050129_29bdesh2.pc.utf8", 1050819_19bdesh2.pc.utf8, 
# "1060617_17edit1.pc.utf8"
# ^ the only doc recovered
training_set = []
training_words_ind = np.array([])

leng = len(expansion[3])
considered = int(30 * leng / 100)
acquired_words = \
    np.intersect1d(expansion[1][-considered:], expansion[2][-considered:])


query_id = 38

rel_list = \
    ["1050129_29bdesh2.pc.utf8", "1050819_19bdesh2.pc.utf8", "1060617_17edit1.pc.utf8"]

# # of docs
corpus_size = len(doc_id.keys())
# bm score holder
bm_score_array = np.empty((0,2))

bag_of_terms = qt_cluster[query_id]
bag_of_terms['pred'] = [0]
bag_flattened = []
for i in bag_of_terms:
    bag_flattened += bag_of_terms[i][1:]
    
docs = rf.set_of_possibly_rel_doc(bag_flattened, term_db).astype('int32')

for _id in docs:
    if doc_id[_id].split('\\')[-1] in rel_list:
        training_set.append(_id)
    
    
    for index in training_set:
        training_words_ind = np.union1d(word_in_doc[index], training_words_ind)
    
    training_words_ind = training_words_ind.astype('int32')
    training_words = corpus_terms[training_words_ind]
    
    predicted_word = np.intersect1d(acquired_words, training_words)
    bag_of_terms['pred'] += list(predicted_word)
    
    bm_val = rf.custom_bm_score_2(bag_of_terms, _id, corpus_size, term_db, doc_len)
    bm_score_array = np.append(bm_score_array, [[_id, bm_val]], 0)
    ranking = bm_score_array[bm_score_array[:,1].argsort()[::-1]]

dic = []
for i in range(100):
    dic[int(ranking[i][0])] = ranking[i][1]

with open(root + "query" + str(query_id), 'wb') as f: 
# ^^^^ change the directory name accordingly
    pickle.dump(dic, f)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    