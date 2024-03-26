# Project2: Information Extraction - Iterative Set Expansion (ISE)
## Purpose
This project is about information extraction on the web, or the task of extracting "structured" information that is embedded in natural language text on the web.
This project implements both a "traditional" information extraction approach (using SpanBERT) that involves multiple steps of data annotation, as well as an approach that reflects the ongoing paradigm shift from multi-step data pipelines with specialized models for extraction tasks to strong "few-shot" learners (using Google's Gemini API).

The objective of this project is to:
   1. Retrieve and parse webpages
   2. Prepare and annotate text on the webpages for subsequent analysis
   3. Extract structured information from the webpages

This is a project is developed in Spring 2024 for the course COMS 6111 Advanced Database Systems taught by Professor Luis Gravano at Columbia University.
    
Reference: https://www.cs.columbia.edu/~gravano/cs6111/Proj2/
   
## Detail
1. Group members: Dawei Yin, dy2482 & Yenchu Chen, yc4360
2. List of files:
    * `main.py`: This Python script is designed for running an information extraction process using either SpanBERT or Google Gemini for relation extraction from web content, based on a given seed query. It responsible for collecting search results, using spaCy library to extract named entities, and implementing SpenBert.
    * `gemini.py`: This Python script integrates Google's Generative AI (Gemini API) for relation extraction tasks. It defines functions to generate prompts for Gemini, fetch responses from the API, and extract relation tuples.
    * `README.md`: This file contains a description of the project, providing an overview of its purpose and functionality.
    * `requirements.txt`: This file lists all the packages used in the project, ensuring compatibility and ease of setup for other users.
    * `transcript_spanbert.txt`: This file contains the results using SpanBERT classifier with input parameters:`-spanbert 2 0.7 "bill gates microsoft" 10`.
    * `transcript_gemini.txt`: This file contains the results using Google's Generative AI(Gemini 1.0 Pro model) with input parameters:`-gemini 2 0.0 "bill gates microsoft" 10`.
   The format of transcript follow this reference: https://www.cs.columbia.edu/~gravano/cs6111/Proj2/Proj2-Transcripts/.
      
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

5. Description of SpanBERT and GEMINI method:

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
   AIzaSyDB1xiTbkdr2O8KhnWdHrCJ8jBAfdnxii4
   ```
   * Engine ID
   ```
   56f4e4ae2f4944372
   ```
7. Additional information
   
