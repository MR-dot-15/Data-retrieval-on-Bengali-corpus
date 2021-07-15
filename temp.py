""" import pickle

def find_intersect(word1, word2, prefix_length = 0):
    '''
        Given two words, finds the intersection bw them
        for a user defined prefix length
        default value will be used if prefix_length remains 0
    '''
    index = 0
    l1, l2 = len(word1), len(word2)
    if prefix_length == 0:
        prefix_length = int(2*max(l1, l2)/3.0)
        #prefix_length = 2
    temp = []
    while index < min(l1, l2):
        if word1[index] != word2[index]:
            break
        elif word1[index] == word2[index]:
            temp.append(word1[index])
            index += 1
    if  len(temp) >= prefix_length: return (''.join(temp), 1)
    else: return (''.join(temp), 0)

with open('term_database_dict', 'rb') as inf:
    term_db = pickle.load(inf)

with open('query_terms_based_stem_db_2', 'rb') as f:
    qterms_db = pickle.load(f)

words = list(term_db.keys())

for term in qterms_db.keys():
    for word in words:
        (intersect, value) = find_intersect(term, word)
        if value == 1 and word not in qterms_db[term]:
            qterms_db[term].append(word)

with open('query_terms_based_stem_db_2', 'wb') as inf:
    pickle.dump(qterms_db, inf)  """

# =============================================================================
# import pickle
# import numpy as np
# import re
# 
# # marks based on which the doc text will be splitted
# split_marks = ['\n', chr(2404), ' ', '-']
# # these need to be removed
# punc_marks = [',', '!', '?', ';', '/', chr(39),'(', ')']
# 
# root = r"C:\Users\rmukh\OneDrive\Desktop\Summer 21\summer_internship_21\Bengali-data"
# 
# term = "বার"
# 
# with open('docid_db', 'rb') as f:
#     id_db = pickle.load(f)
# 
# with open('term_database_dict', 'rb') as f:
#     invrt_list = pickle.load(f)
# 
# for _id in id_db.keys():
#     filename = root + "\\Bengali-data" + id_db[_id]
#     try:
#         print(round(_id*100/98147,2), " % done", end = '\r')       
#         with open(filename, 'r', encoding='utf8') as infile:
#             # tokenization of the document text
#             text = re.split('|'.join(split_marks),infile.read())
# 
#         # removing blank elements and section specifiers
#         text = [i for i in text if i != '' and '<' not in i]
# 
#         # removing punctuation marks
#         for index in range(len(text)):
#             for mark in punc_marks:
#                 if mark in text[index]:
#                     text[index] = text[index].replace(mark, '')
# 
#         for word in text:
#             if word == term:
#                 if word not in invrt_list.keys():
#                     invrt_list[word] = np.array([[_id, 1]])
#                 else:
#                     if invrt_list[word][-1][0] == _id:
#                         invrt_list[word][-1][1] += 1
#                     else:
#                         invrt_list[word] =\
#                             np.append(invrt_list[word],[[_id,1]], 0)
# 
#     except:
#         print(_id, end = '\n')
# 
# with open('term_database_dict', 'wb') as outfile:
#         pickle.dump(invrt_list, outfile)
# =============================================================================
import pickle
import numpy as np

# opening the inverted list
with open('term_database_dict', 'rb') as f:
    term_db = pickle.load(f)

punc = ['.', ':']

# stop-word list
with open('sw.txt', 'r', encoding = 'utf8') as f:
    sw = f.read().split('\n')

key_list = list(term_db.keys())

for key in key_list:
    if key in sw or key == '':
        term_db.pop(key)
    for i in punc:
        if i in key:
            new_key = key.strip(i)
            key_val = term_db[key]
            print(key, new_key)
            if new_key not in term_db:
                term_db[new_key] = key_val
                term_db.pop(key)
            else:
                for j in key_val:
                    if j[0] in term_db[new_key][:,0]:
                        x = np.where(term_db[:,0] == j[0])[0]
                        term_db[new_key][x][1] += 1
                    else:
                        term_db[new_key] = np.append(term_db[new_key], j)

with open('term_database_dict', 'wb') as f:
    term_db = pickle.dump(term_db, f)



# ==============================================================================
import numpy as np
import pickle
import relevant_func as rf

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

# "1050129_29bdesh2.pc.utf8", 1050819_19bdesh2.pc.utf8
# the only doc recovered
training_set = ["1060617_17edit1.pc.utf8"]

leng = len(expansion[3])
considered = int(30 * leng / 100)
acquired_words = \
    np.intersect1d(expansion[1][-considered:], expansion[2][-considered:])

ids = []
for i in training_set:
    for _id in doc_id:
        if doc_id[_id].split('\\')[-1] == i:
            ids.append(_id)

training_words_ind = np.array([])

for _id in ids:
    training_words_ind = np.union1d(word_in_doc[_id], training_words_ind)

training_words_ind = training_words_ind.astype('int32')
training_words = corpus_terms[training_words_ind]

predicted_word = np.intersect1d(acquired_words, training_words)
print(predicted_word)
