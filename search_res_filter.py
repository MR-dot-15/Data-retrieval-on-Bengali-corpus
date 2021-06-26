'''
    accesses each search result database from search_res
    calculates precision, recall 
    prints the top (bm score) 20 result
'''
import pickle
import numpy as np
root = r"C:\Users\rmukh\OneDrive\Desktop\Summer 21\summer_internship_21\Bengali-data"

# accessing document id database
with open('docid_db', 'rb') as f:
    doc_id = pickle.load(f)

# accessing the relevance list 
with open("bn.qrels.76-125.2010.txt", 'r') as f:
    relevance_list = f.read().split('\n')

relevance_list = [i.split(' ') for i in relevance_list]

# iterating over already made search results of queries
for index in range(1,6):
    print("Query ", str(index), '\n')
    precision, recall= [], []
    no_retrieved, no_rel = 0, 0

    # finding the relevant files from the relevance list, for a particular query
    rel_list = [i for i in relevance_list if i[0] == str(75 + index) and i[3] == "1"]

    # total relevant documents per query
    tot_rel = len(rel_list)

    # accessing the search result stored in search_res directory
    with open(root + "\\search_res\\" + "query" + str(index), 'rb') as f:
        dic = pickle.load(f)
    
    for i in dic.keys():
        # file name
        file = doc_id[i].split('\\')[-1]
        print(f"{file:<25}", end = '')
        # bm score
        print(f"{round(dic[i], 2):^10}", end = '')

        # precision and recall calculation
        if file in [i[2] for i in rel_list]:
            precision.append(1)
            recall.append(1)
        else:
            precision.append(0)
            recall.append(0)

        no_retrieved += 1

        prec = sum(precision)*1.0/no_retrieved
        rec = sum(recall)*1.0/tot_rel

        print(f"{round(prec,2):^5}", end = '')
        print(f"{round(rec,2):>5}", end = '\n')
    