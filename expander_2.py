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

# expanded words
expansion = dict()

# finding how many times a word occurs in an intersection
def find_common_occ(word, intersect_doc_id):
    occ = term_db[word][:,0]
    common_occ = np.intersect1d(occ, intersect_doc_id)
    score = len(common_occ)/len(occ)
    freq = term_db[word][:,1][np.in1d(occ, common_occ, assume_unique = True)].sum()

    return [[score, freq]]


def find_relevant_words(word_cluster1, word_cluster2):
    doc_set1 = rf.set_of_possibly_rel_doc(word_cluster1, term_db)
    doc_set2 = rf.set_of_possibly_rel_doc(word_cluster2, term_db)
    docs_of_interest = np.intersect1d(doc_set1, doc_set2).astype('int32')

    ind_probable_words = []
    for _id in docs_of_interest:
        ind_probable_words += word_in_doc[_id]

    ind_probable_words = list(set(ind_probable_words))
    probable_words = corpus_terms[ind_probable_words]

    return docs_of_interest, probable_words

docs = find_relevant_words(['বাংলাদেশি', 'বাংলাদেশে', 'বাংলাদেশ', 'বাংলাদেশের'], ['রাজনৈতিকভাবে', 'রাজনৈতিকতার', 'রাজনৈতিক'])[0]
terms = find_relevant_words(['বাংলাদেশি', 'বাংলাদেশে', 'বাংলাদেশ', 'বাংলাদেশের'], ['রাজনৈতিকভাবে', 'রাজনৈতিকতার', 'রাজনৈতিক'])[1]

classify_val = np.empty((0, 2))

for term in terms:
    val = find_common_occ(term, docs)
    classify_val = np.append(classify_val, val, axis = 0)