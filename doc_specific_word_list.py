import pickle

# opening the inverted list
with open('term_database_dict', 'rb') as f:
    term_db = pickle.load(f)

# list of all words in the inverted list
words = list(term_db.keys())
length = len(words)

# doc specific word holder
doc_word_collection = dict()

for i in range(length):
    print("%.2f"%(i*100/length), "% done", end = '\r')
    word = words[i]

    # say, t: [doc1, doc2,..]
    # scans the posting list of t
    # docᵢ: [index(tᵢ₁), index(tᵢ₂),...]
    for doc_id in term_db[word][:, 0]:
        if doc_id not in doc_word_collection.keys():
            doc_word_collection[doc_id] = [i]
        else:
            doc_word_collection[doc_id].append(i)

# storing the data
with open('word_in_doc', 'wb') as f:
    pickle.dump(doc_word_collection, f)