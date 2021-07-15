'''
    collection of all the functions used at different times
    a list is given below:
    - set_of_possibly_rel_doc(wordbag, inverted_list)
    - find_intersect(word1, word2, prefix_length = 0)
    - calculate_tf_idf(term, docid, tot_doc, term_database)
    - calculate_bm_score(term_bag, docid, tot_doc, term_database, len_database)
    - custom_bm_score(term_bag_dict, docid, tot_doc, term_database, len_database)
    - custom_bm_score_2(term_bag_dict, docid, tot_doc, term_database, len_database)
    - occurrence(word, term_db)
    - coocc_val(word1, word2, term_db)
    - coocc_val_2(word1, word2, term_db)
    - coocc_np(word1,list_of_words, term_db)
    - co_occurrence_classifier(term, term_db)
    - match_score(str1, str2)
    - find_best_match(word, corpus_terms)
'''
import numpy as np

# given a bag of words
# it finds the intersection of the document lists 
# where at least one of the words occur
def set_of_possibly_rel_doc(wordbag, inverted_list):
    possibly_rel_doc = np.array([])
    for word in wordbag:
        occurrence_of_word = inverted_list[word][:, 0]
        possibly_rel_doc = np.union1d\
            (occurrence_of_word, possibly_rel_doc)
    return possibly_rel_doc

# prefix match finder
# default = 50% of the longer word's length 
def find_intersect(word1, word2, prefix_length = 0):
    '''
        Given two words, finds the intersection bw them
        for a user defined prefix length
        default value will be used if prefix_length remains 0
    '''
    index = 0
    l1, l2 = len(word1), len(word2)
    if prefix_length == 0:
        prefix_length = int(2 * max(l1, l2)/3)
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

# calculation of tf-idf factor
def calculate_tf_idf(term, docid, tot_doc, term_database):
    try:
        # posting list of a term with freq
        term_details = term_database[term]

        # finding the particular doc id instance
        i = np.where(term_details[:, 0] == docid)[0][0]

        # # of total docs
        tot_doc_no = tot_doc

        # # of docs containing that term
        doc_freq = np.size(term_details, 0)

        # tf-idf formula
        return\
            (term_details[i][1] * np.log(1.0*tot_doc_no/doc_freq)/np.log(10),\
                term_details[i][1])
    except:
        return (0, 0)

# calculation of b25 score
def calculate_bm_score(term_bag, docid, tot_doc, term_database, len_database):
    # redundant renaming
    docid, tot_doc, term_db = docid, tot_doc, term_database

    # parameter values
    k1, b = 1.2, 0.75

    # bm score holder
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

# customized bm score with parameters as explained below
# thought behind: in normal clustering, some terms got high # of variants
# eg "লালু", "লাল" etc
# higher the # of variants, lesser is its uniqueness -> lesser stress 
def custom_bm_score(term_bag_dict, docid, tot_doc, term_database, len_database):
    bm_score = 0
    for key in term_bag_dict:
        #weight = 1 / len(term_bag_dict[key])
        weight = np.exp(-len(term_bag_dict[key]) * 0.1)
        bm_score += weight * calculate_bm_score\
            (term_bag_dict[key], docid, tot_doc, term_database, len_database)

    return bm_score

# specially made for the last development
# say, qᵢ = {t₁, t₂,...}
# boost score = #_of_tᵢ in that doc
def custom_bm_score_2(term_bag_dict, docid, tot_doc, term_database, len_database, inst_weight = 1):
    bm_score = 0
    instance_weight = 0
    for key in term_bag_dict:
        if len(term_bag_dict[key]) > 1:
            if inst_weight == 0:
                # the first element of term_bag_dict[key] is 0 or 1, hence [1:]
                occurrence_of_cluster = \
                    set_of_possibly_rel_doc(term_bag_dict[key][1:], term_database).astype('int32')
                if docid in occurrence_of_cluster:
                    instance_weight += 1
        # an alternative definition of the instance_weight:
        # weight = 2 - exp(-instance_weight) \in [1, 2]

            bm_score += calculate_bm_score\
                (term_bag_dict[key][1:], docid, tot_doc, term_database, len_database)

    weight = 2 - np.exp(-instance_weight)
    return weight * bm_score

# # of occurrence of a term in the corpus
# redundant
def occurrence(word, term_db):
    return len(term_db[word][:,0])

# redefined using numpy ufunc
# input <- ([list of words], inverted list)
occ_np = np.frompyfunc(occurrence, 2, 1)

# co-occurrence value b/w word1 and word2
def coocc_val(word1, word2, term_db):
    occurrence_array, base = term_db[word2][:,0], term_db[word1][:,0]
    occurrence, tot = len(occurrence_array), len(base)
    co_occurrence = len(np.intersect1d(occurrence_array, base))

    return (co_occurrence, occurrence, tot)

# same as before, returns only the co-occurrence value
# used below, to create a np-ufunc
def coocc_val_2(word1, word2, term_db):
    occurrence_array, base = term_db[word2][:,0], term_db[word1][:,0]
    occurrence, tot = len(occurrence_array), len(base)
    co_occurrence = len(np.intersect1d(occurrence_array, base))

    return co_occurrence

# redefined using np ufunc
# input <- (term_of_interest, [list of terms], inverted list)
coocc_np = np.frompyfunc(coocc_val_2, 3, 1)

# intention: finding meaningful, important variants of a term
# to avoid the issue of co-occurrence value clustering
# tanh function is used: kind of as a classifier
def co_occurrence_classifier(term, term_db):
    words = list(term_db.keys())
    lis = np.array([])
    co_occ = np.array([])

    for word in words:
        (intersect, value) = find_intersect(term, word, prefix_length = 0)
        if len(term) <= 3 and len(intersect) != len(term):
            continue
        if value == 1:
            lis = np.append(lis, word)
            co_occ_val, occ_val, tot = coocc_val(term, word, term_db)

            try:
                relative = len(term_db[intersect][:,0])/tot
                booster = np.tanh(relative-1) + 1
            except:
                booster = 0.01

            #val = 1000*(co_occ_val**2/(occ_val * tot)) * booster * len(intersect)
            val = 1000*(co_occ_val/occ_val) * 100*(co_occ_val/tot) * booster * len(intersect)
            co_occ = np.append(co_occ, val)

    # index of words in lis
    index_array = np.arange(len(co_occ))
    # co occurrence values > 0
    co_occ_g0 = co_occ[co_occ>0]
    # index of words having >0 coocc
    index_g0 = index_array[co_occ>0]

    if len(index_g0) <= 5:
        return lis[index_g0]

    # sort_index of co_occ_g0
    ind = np.argsort(co_occ_g0)
    co_occ_g0_sorted = co_occ_g0[ind][:-1]
    index_g0_sorted = index_g0[ind][:-1]

    lim = co_occ_g0_sorted[-1]
    x = np.linspace(0, lim)

    y_mean = np.mean(co_occ_g0_sorted)
    y_var = np.std(co_occ_g0_sorted)

    y_mod = np.tanh((co_occ_g0_sorted - y_mean)/y_var)

    classified_ind = index_g0_sorted[abs(y_mod-1)<0.3]
    ref_lis = lis[classified_ind]

    return ref_lis[-5:]


# not sure what to do with this
# intention: given two strings s1, s2 returns a match value
""" def match_score(str1, str2):
    str1, str2 = \
        np.array(list(str1)), np.array(list(str2))
    len1, len2 = len(str1), len(str2)
    _min = min(len(str1), len(str2))
    if _min <= 6:
        return 0 
    
    match = str1[:_min] == str2[:_min]
    return 2 * match.sum()/(len(str1) + len(str2)) """

def match_score(str1, str2):
    str1, str2 = list(str1), list(str2)
    len1, len2 = len(str1), len(str2)
    _min = min(len(str1), len(str2))
    # the first entry of the tuple is to make the loop word
    # iteration stops when it becomes 0
    front, end = 1, 1
    front_match, back_match = [], []
    for i in range(_min):
        if front == 0:
            bk = str1[-i - 1] == str2[-i - 1]
            if bk == 1:
                back_match.append(str1[-i - 1])
            else:
                end = 0
                break
        elif end == 0:
            fr = str1[i] == str2[i]
            if fr == 1:
                front_match.append(str1[i])
            else:
                front = 0
                break
        else:
            fr = str1[i] == str2[i]
            bk = str1[-i - 1] == str2[-i - 1]
            if fr == 1 and bk == 1:
                front_match.append(str1[i])
                back_match.append(str1[-i - 1])
                if abs(2*i + 1 - _min) <= 1:
                    break
            elif fr == 1 and bk == 0:
                front_match.append(str1[i])
                end = 0
            elif fr == 0 and bk == 1:
                back_match.append(str1[-i - 1])
                front = 0
            else:
                front, end= 0, 0
                break
    booster = np.exp(- 0.1 * abs(len1 - len2))
    score = 2 * booster * (len(front_match) + len(back_match)) / (len1 + len2)
    if score >= 1: return 1
    else: return score


def find_best_match(word, corpus_terms):
    match_words = np.empty((0,2))
    for probable_match in corpus_terms:
        score = match_score(word, probable_match)
        if score > 0.7:
            match_words = \
                np.append(match_words, [[probable_match, score]], axis = 0)
    
    res = match_words[match_words[:,1].argmax()][0]
    return res



#================================================================
# some statistics regarding the data set
# average word length = 8.28
# minimum = 1
# maimum = 29
# 25th percentile = 6
# 75th percentile = 10
#================================================================