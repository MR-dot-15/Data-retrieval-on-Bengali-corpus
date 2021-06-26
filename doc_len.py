'''
    doc len for bm25
    creates a separate doc len database
'''
import pickle
import numpy as np
import re

root = r"C:\Users\rmukh\OneDrive\Desktop\Summer 21\summer_internship_21\Bengali-data"
# marks based on which the doc text will be splitted
split_marks = ['\n', chr(2404), ' ', '-']

# accessing the docid database
with open('docid_db', 'rb') as f:
    docid = pickle.load(f)

# reads the stop word file
with open('\\'.join([root, "sw.txt"]), 'r', encoding = 'utf8') as f:
    stop_words = f.read().split('\n')

# iterates through docid.keys()
# appends word count to doc_len
def calculate_length():
    doc_len = np.zeros((len(docid.keys(),)))
    for _id in docid.keys():
        print(_id, end = ',')
        filename = root + "\\Bengali-data" + docid[_id]
        try:
            with open(filename, 'r', encoding='utf8') as infile:

                # tokenization of the document text
                text = re.split('|'.join(split_marks),infile.read())

            # removing blank elements, stop words, section specifiers
            text = [i for i in text if i != '' and '<' not in i\
                and i not in stop_words]
            
            doc_len[_id] = len(text)

        except:
            continue    
    return doc_len

doc_len = calculate_length()
avg_len = np.mean(doc_len)

with open('doc_len', 'wb') as f:
    pickle.dump({0:doc_len, 1:avg_len}, f)