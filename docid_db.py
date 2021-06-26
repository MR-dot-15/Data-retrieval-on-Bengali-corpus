'''
    Creates the doc ID set
'''
import os
import pickle
os.chdir(r"C:\Users\rmukh\OneDrive\Desktop\Summer 21\summer_internship_21\Bengali-data")

docid = dict()
index = 1
for (root, _dir, _file) in os.walk(r"C:\Users\rmukh\OneDrive\Desktop\Summer 21\summer_internship_21\Bengali-data\Bengali-data"):
    for item in _file:
        docid[index] = root[88:] + "\\" + item
        index += 1

with open('docid_db', 'wb') as inf:
    pickle.dump(docid, inf)