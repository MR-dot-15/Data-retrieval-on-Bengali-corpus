'''
    reads the co-occurrence matrix and prefix match cluster
    finds the best 'matches' from the cluster ...
    ... based on the co-occurrence value
    reforms the clustering and stores in a pickle (co_occ_cluster)
'''
import numpy as np
import pickle
import relevant_func as rf
        
    

# opens the query terms db 
with open("query_terms_based_stem_db_2", 'rb') as f:
    q_terms = pickle.load(f) 

# opens the co-occurrence matrix
with open('co_occurrence_matrix_2', 'rb') as f:
    co_occ_mat = pickle.load(f) 
    
with open('term_database_dict', 'rb') as f:
    invrt_list = pickle.load(f)
    

co_occ_based_cluster = dict()
terms = q_terms.keys()
for word in terms:
    #print(round(index*100./length, 2), " % done", end = '\r')
    new_cluster = []
    cluster = q_terms[word]
    if len(cluster) != 0:
        co_occurrence = co_occ_mat[word]
        try:
            pos_of_word = cluster.index(word)
        except:
            match_val = np.array([])
            for element in cluster:
                occ = np.sum(invrt_list[element][:,1])
                match_val = np.append(match_val, rf.match_value(word, element, occ))
            temp = np.where(match_val == np.amax(match_val))
            pos_of_word = temp[0]
        finally:
            for j in range(len(cluster)):
                if max(co_occurrence[pos_of_word, j], \
                    co_occurrence[j, pos_of_word]) > 0.8:
                    new_cluster.append(cluster[j])
        
            co_occ_based_cluster[word] = new_cluster

with open('co_occ_cluster_3', 'wb') as inf:
    pickle.dump(co_occ_based_cluster, inf) 