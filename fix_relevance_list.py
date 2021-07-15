import pickle
root = r"C:\Users\rmukh\OneDrive\Desktop\Summer 21\summer_internship_21\Bengali-data"

# accessing document id database
with open('docid_db', 'rb') as f:
    doc_id = pickle.load(f)

# accessing the relevance list 
with open("bn.qrels.76-125.2010.txt", 'r') as f:
    relevance_list = f.read().split('\n')

relevance_list = [i.split(' ') for i in relevance_list]

doc_names = [doc_id[i].split('\\')[-1] for i in doc_id.keys()]

new_rel_list = []

eliminated_items = []

for rel_element in relevance_list:
    if rel_element[2] in doc_names:
        new_rel_list.append(rel_element)
    else:
        eliminated_items.append(rel_element)

rel_lis = '\n'.join([' '.join(i) for i in new_rel_list])

redundant = '\n'.join([' '.join(i) for i in eliminated_items])

with open('rel_list.txt', 'w') as f:
    f.write(rel_lis)

with open('eliminated_items_in_rel_list.txt', 'w') as f:
    f.write(redundant)