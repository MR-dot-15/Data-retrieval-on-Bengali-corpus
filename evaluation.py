"""
    calculates the 
    - precision @ 5
    - precision @ 10 
    - MAP
"""
import pickle

root = r"C:\Users\rmukh\OneDrive\Desktop\Summer 21\summer_internship_21\Bengali-data"
# four different folders blah blah
# names to be inserted here
result_base = "\\search_res\\"

# accessing document id database
with open('docid_db', 'rb') as f:
    doc_id = pickle.load(f)

# accessing the relevance list 
with open("rel_list.txt", 'r') as f:
    relevance_list = f.read().split('\n')
relevance_list = [i.split(' ') for i in relevance_list]

# evaluation value database
eval_data = dict()

print("Doing for: ", result_base.strip('\\'))

# iterating over already made search results of queries
for i in range(1, 51):
    # apparently there is no relevant doc in the corpus
    # like wth!
    if i == 48:
        continue
    index = i - 75
    precision, recall= [0], [0]
    no_retrieved, no_rel = 0, 0

    # finding the relevant files from the relevance list, for a particular query
    rel_list = [i for i in relevance_list if i[0] == str(75 + index) and i[3] == "1"]

    # total relevant documents per query
    tot_rel = len(rel_list)

    # accessing the search result stored in search result directories
    with open(root + result_base + "query" + str(index), 'rb') as f:
        dic = pickle.load(f)
    
    for i in dic.keys():
        # number of retrieved docs
        no_retrieved += 1

        # to keep track whether the precision val is relevant for mean calculation
        condition = False

        # file name
        _file = doc_id[i].split('\\')[-1]

        # precision and recall calculation
        if _file in [i[2] for i in rel_list]:
            # number of relevant docs
            no_rel += 1
            # changing the condition val
            condition = True

        # precision and recall value whenever one relevant doc is found
        precision_val = no_rel/ no_retrieved
        recall_val = no_rel/tot_rel
        if no_retrieved > 10 and recall_val == 1:
            break

        if condition:
            precision.append(precision_val)
        
        if no_retrieved == 5:
            fifth_precision_values = precision_val

        if no_retrieved == 10:
            tenth_precision_values = precision_val
        
        
    avg_precision_values = sum(precision)/tot_rel
    eval_data[index] = [fifth_precision_values, tenth_precision_values, avg_precision_values]

path = root + "\\eval_result\\""eval_" + result_base.strip('\\')
with open(path, 'wb') as f:
    pickle.dump(eval_data, f)