# Data-retrieval-on-Bengali-corpus
A data retrieval system on a Bengali news article corpus, summer project-'21. </br>
**Note:**</br>
To run the system properly, the ```root``` path needs to be changed accordingly in all the .py files. 

## Bengali-data (folder)
  - Contains entire the corpus
  - (Not here in this repo)
## search_res
  - Stores the pickled search results, query ID-wise
---
## txt files
### *bn.topics*
  - Some pre-set query topics to carry out the search operation on
  - (Not here in this repo)
### *bn.qrels*
  - Relevance score of documents wrt the query items
  - (Not here in this repo)
### *sw*
  - A bengali stop-word list (provided by sir)
---
## py files
  Need to be run following this particular chronology
### *docid_db.py*
  - os.walk() to find the file names of all the corpus documents
  - pickling them inside ```docid_db```
### *extract_query.py*
  - reads the bn.query... file and extracts the <title> block (as of now)
  - tokenizes, un-punctuates and removes stop words
  - pickles them in ```query_terms_based_stem_db``` in the following way: {t<sub>1</sub>:[], t<sub>2</sub>:[],...}
### *word_db_creat.py*
  - reads the query words and all the files in the corpus
  - performs the clustering operation based on prefix intersection (2/3<sup>rd</sup> of min(w<sub>1</sub>, w<sub>2</sub>)
  - stores the clustered database by overwriting ```query_terms_based_stem_db```: 
  {t<sub>1</sub>:[w<sub>11</sub>, w<sub>12</sub>,...], t<sub>2</sub>:[w<sub>21</sub>, w<sub>22</sub>,...],...}
  - creates the inverted matrix and pickles into ```term_database_dict```
### *relevant_func.py*
  - BM25 model algorithm
### *doc_len.py*
  - measures the length of each document in terms of total # of words 
  - calculates the average
  - pickles into ```doc_len```
### *main.py*
  - conducts the actual searching operation by picking up queries from ```bn.topics```
  - stores the search results (top 20 BM ranks) in the ```search_res``` directory
### *search_res_filter*
  - retrieves the pickled search result
  - measures precision, accuracy scores
  - prints the result in a formatted table
### *co_occ.py*
  - constructs the co-occurrence matrix and finds k-nearest neighbours from the cluster for each query term
  - stores the result into ```co_occurrence_matrix```
---
## pickle files
  Roles already explained
### *docid_db*
### *query_terms_based_stem_db*
### *term_database_dict*
### *doc_len*
### *co_occurrence_matrix*
