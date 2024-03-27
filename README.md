# Project1: Information retrieval system based on user-provided relevance feedback
## Purpose
   
   This project serves as an information retrieval system designed to enhance search results provided by Google through user-provided feedback.
   The project takes a user query, typically a word related to the target information, as input.In each iteration, the system expands the query based on user feedback regarding the relevance of the search results to the target. The iteration continues until the accuracy reaches a predefined threshold. 
   The objective is to minimize the number of iterations required to achieve the desired precision threshold, thus optimizing the search process.

   This is a project is developed in Spring 2024 for the course COMS 6111 Advanced Database Systems taught by Professor Luis Gravano at Columbia University.

   Reference: https://www.cs.columbia.edu/~gravano/cs6111/proj1.html

   
## Detail
1. Group members: Dawei Yin, dy2482 & Yenchu Chen, yc4360
2. List of files:
    * `main.py`: This is the main Python file responsible for collecting search results using Google's Custom Search JSON API and collecting the user feedback.
    * `rocchio.py`: This Python file takes the original queryn and search result as input and utilizes the Rocchio algorithm along with n-gram techniques to generate an expanded query.
    * `README.md`: This file contains a description of the project, providing an overview of its purpose and functionality.
    * `requirements.txt`: This file lists all the packages used in the project, ensuring compatibility and ease of setup for other users.
    * `logs_for_testcase.txt`: This file contains the results of our project, including outputs from various test cases conducted during evaluation.
3. Instruction to run the project:

    Enter into the directory where main.py file is located. Run: python main.py [threshold_rate] [original_query]
    * Take threshold as 0.9 and original query "per se" as example.
   ```
   python main.py 0.9 "per se"
   ```
4. Description of the internal design of this project:

   * High-level Concept:
     1. Parse command-line arguments (precision and query).
     2. Build the Google Custom Search service. [build_service]
     2. Use the Engine ID with the server we set and the original query to get the search result. [search_by_query]
     3. Retrieve the 'Title', 'URL', 'Summary'(snippet) from the response(contains exactly top 10 search result). [parse_response]
     4. Search result will be displayed to the user one by one and user will type Y or N judging from whether the result is relative to the target. [get_ok]
     5. If the user's feedback to the search result reaches the desired threshold or none of the returned document is relevant, the program will stop.[query_by_precision]
     6. If not, based on the user's feedback, the program will utilize Rocchio's algorithm by analyzing 'Title' and 'Summary' to obtain the top two relevant words and reorderd all the words by ngram technique to generate the new query. The detailed implementation of Rocchio's algorithm is introduced in the section 5. [query_by_precision]

   * External libraries used:
     1. googleapiclient: Used for accessing the Google Custom Search API. 
     2. requests: Used for making HTTP requests to fetch web page content. 
     3. BeautifulSoup: Used for parsing HTML content and extracting text data from web pages. 
     4. nltk: Used for natural language processing tasks such as tokenization, stopwords removal, and stemming. 
     5. numpy: Used for numerical computing tasks and operations on vectors and matrices.

5. Description of your query-modification method:

   1. Initialize the Rocchio class with relevant and irrelevant documents(based on user feedback) and the query.
   2. Generate a vocabulary list by extracting all words from the documents and the query. This process involves tokenizing the strings, converting all words to lowercase, removing punctuation and non-alphabetic characters, and filtering out stopwords defined by the nltk.corpus library. [get_vocab]
   3. Compute TF-IDF vectors for the relevant and irrelevant documents. This involves:
      * Computing the IDF for each word in the vocabulary across all documents.[get_idf]
        
        `idf(wi) = math.log10(len(all_docs) / (doc_with(wi))`
      * Computing two TF-IDF vector(in respect of relevant and irrelevant document) for each documents by multiplying the term frequency (tf) of each word with its corresponding idf value. [get_tf_idf]
        
        `tf_idf(wi) = math.log10(freq(wi) + 1) * idf_map[wi]`
      
   4. Compute the Rocchio score by normalizing the TF-IDF vectors to the second degree and applying the following formula to rank all vocabulary words (excluding those already in the original query) by their Rocchio score.
   5. Select the top two words from the original query to generate a new query.
   6. Generate a dictionary of n-grams, keeping track of the occurrences of n-grams in all documents (here, n is set to 2).[generate_ngrams]
   7. Use permutations to generate all possible candidate queries with different word orders and select the candidate with the highest occurrence of the selected n-gram.[generate_groups]
   8. Return the updated query for use in the search process in the main.py file.

6. Testing Key:
   * Google Custom Search Engine JSON API Key
   ```
   *************
   ```
   * Engine ID
   ```
   56f4e4ae2f4944372
   ```
7. Additional information
   * Result(see `logs_for_testcase.txt`):
     1. Look for information on the Per Se restaurant in New York City, starting with the query `per se`.
        
        With the threshold set as 0.9, the program can stop at the second iteration with precesion rate =1.
     
        query = python main.py 0.9 "per se"
     
        first input = (y,n,y,y,y,n,n,y,n,n), precision rate =0.5   new query: per se michelin restaurant
     
        second input = (y,y,y,y,y,y,y,y,y,y), precision rate = 1

     2. Look for information on 23andMe cofounder Anne Wojcicki, starting with the query `wojcicki`.
        
        No relevant result from the return. @2024.2.18
     
     3. Look for information on COVID-19 cases, starting with the query `cases`.
        
        With the threshold set as 0.9, the program can stop at the second iteration with precesion rate =1.
     
        query = python main.py 0.9 "cases"
     
        first input = (n,n,y,n,n,n,n,n,n,n), precision rate =0.1   new query:  covid cases statistics
     
        second input = (y,y,y,y,y,y,y,y,y,y), precision rate = 1
     3. Look for information on jaguar the car, starting with the query `jaguar`.
        With the threshold set as 0.9, the program can stop at the second iteration with precesion rate =1.
     4. Look for information on jaguar the animal, starting with the query `jaguar`.
        With the threshold set as 0.9, the program can stop at the second iteration with precesion rate =1.
     
   * Fetch the content: In our initial approach, we attempted to incorporate the content from the web pages along with the snippets. However, we discovered that the web content often contained a significant amount of irrelevant information, leading to deviations in the search results. Consequently, we opted to focus solely on the title and snippet, as they are more likely to offer concise and pertinent information.
   * stemming: In our initial approach, we attempted to incorporate the stemming technique in tokenization process. However, we discovered that the stemmed word does not help to increase the accuracy. The reason might be that 1) loss of the meaning, with all words reduce to their root may potentially lose the nuances of meaning present in different word forms. This loss of granularity can result in less precise query expansion. 2)search engine algorithm, Google search engine may already handle variants of words effectively without the need for stemming.
   
