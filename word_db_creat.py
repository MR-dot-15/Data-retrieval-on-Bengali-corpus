'''
    Stems and creates the semmed word database
'''
import os
import pickle
import re
import numpy as np
# import find_intersect as fi
root = r"C:\Users\rmukh\OneDrive\Desktop\Summer 21\summer_internship_21\Bengali-data"
os.chdir(root)

# marks based on which the doc text will be splitted
split_marks = ['\n', chr(2404), ' ', '-']
# these need to be removed
punc_marks = [',', '!', '?', ';', '/', chr(39),'(', ')']

with open('docid_db', 'rb') as inf:
    '''
        reads the doc id vs filename database
    '''
    id_db = pickle.load(inf)


with open('query_terms_based_stem_db', 'rb') as inf:
    '''
        reads the dynamic database containing query words
    '''
    qterms_db = pickle.load(inf)   

with open('\\'.join([root, "sw.txt"]), 'r', encoding = 'utf8') as f:
    '''
        reads the stop word file
    '''
    stop_words = f.read().split('\n')

# the dict data holder
term_database = dict() 

def find_intersect(word1, word2, prefix_length = 0):
    '''
        Given two words, finds the intersection bw them
        for a user defined prefix length
        default value will be used if prefix_length remains 0
    '''
    index = 0
    l1, l2 = len(word1), len(word2)
    if prefix_length == 0:
        prefix_length = 2*max(l1, l2)/3.0
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


def create_word_db():
    '''
        1. creates a database holding the inverted list
        2. edits the previously created q terms db
            and clusters same prefix words together
    '''
    _id = 1
    #for _id in id_db.keys():
    while _id <= 98148:
        filename = root + "\\Bengali-data" + id_db[_id]
        _id += 1

        # reason behind the try-except:
        # files like 1070323_23desh11.pc.utf8 are 'un-processable'
        try:
            with open(filename, 'r', encoding='utf8') as infile:

                # tokenization of the document text
                text = re.split('|'.join(split_marks),infile.read())

            # removing blank elements and section specifiers
            text = [i for i in text if i != '' and '<' not in i]

            # removing punctuation marks
            for index in range(len(text)):
                for mark in punc_marks:
                    if mark in text[index]:
                        text[index] = text[index].replace(mark, '')

            # construction of the inverted matrix
            # without stemming
            for word in text:
                # removing stop-words
                if word not in stop_words:
                    # task 1: creates the inverted list database
                    if word not in term_database.keys():
                        term_database[word] = np.array([[_id, 1]])
                    else:
                        if term_database[word][-1][0] == _id:
                            term_database[word][-1][1] += 1
                        else:
                            term_database[word] =\
                                np.append(term_database[word],[[_id,1]], 0)

                    # task 2: edits the query word db to cluster
                    for term in qterms_db.keys():
                        (intersect, value) = find_intersect(term, word)
                        if value == 1 and word not in qterms_db[term]:
                            qterms_db[term].append(word)
                
                    print(round(_id*100/98147,2), " % done", end = '\r')
                
                else:
                    continue
        except:
            print(_id, end = '\n')
        

        
    # pickled database with term details
    with open('term_database_dict', 'wb') as outfile:
        pickle.dump(term_database, outfile)

    # modifying the query term db with clustered groups
    with open('query_terms_based_stem_db', 'wb') as outfile:
        pickle.dump(qterms_db, outfile)

create_word_db()