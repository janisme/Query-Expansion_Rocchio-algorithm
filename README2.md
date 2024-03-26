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
    * `transcript_gemini.txt`: This file contains the results using Google Gemini API(Gemini 1.0 Pro model) with input parameters:`-gemini 2 0.0 "bill gates microsoft" 10`.
   
The format of transcript follow this reference: https://www.cs.columbia.edu/~gravano/cs6111/Proj2/Proj2-Transcripts/.
      
3. Instruction to run the project:
    Enter into the directory: proj2 where main.py file is located, then activate the environment.
   ```
   source dbproj/bin/activate
   ```
   
   Run: python3 main.py -$model_name “$JSON_API_KEY” “$Engine_ID” “$Gemini API key" $relation $extract_threshold $seed_query $output_len
   ```
   python3 main.py -spanbert "AIzaSyBdPoK9zbUZXnDHG4LMMu972zSH7nGdnM8" "56f4e4ae2f4944372" "xxx" 2 0.7 "bill gates microsoft" 10
   ```
* $model_name: indicating the extraction model used. Options: "-spanbert" for SpanBERT or "-gemini" for Google Gemini.
* $relation: indicating the type of relation to extract. Options: an integer; where Schools_Attended(1), Work_For(2), Live_In(3), Top_Member_Employees(4).
* $extract_threshold: indicating the "extraction confidence threshold," which is the minimum extraction confidence that we request for the tuples in the output. Option: a float between 0~1. -gemini ignores this parameter.
* $seed_query: template of a plausible tuple. A list of words in double quotes corresponding to a plausible tuple for the relation to extract. Example:"bill gates microsoft".
* $output_len: indicating the number of tuples that are requested in the output. Option: an integer >0
   
4. Description of the internal design of this project:

   * High-level Concept[ISE]:
     1. Load the SpanBert pre-trained classifier.
     2. Use the Engine ID with the server we set and the query to get the search result(top-10 webpages), and parse the web content. [search_by_query, parse_response].
     3. Loop over URLs, and filter out the URL that have seen.
     4. For each unseen URL, extract the content and do extract named entities using spaCy. If the content characters >10000, trim the webpage content to 10000. Determine by the model specified, run SB or run_gemini to do information extraction.[information_extraction, page_extraction]
     5. For each query iteration, print out all the extracted relations.[print_pretty_relations]
     6. If the number of extracted relations < $output_len, concatenating the original query with relation that has the highest confident rate and jump back to step 2.
     7. If the number of extracted relations > $output_len, teriminate the program. The result relations sets remain all the tuples extractd which may > k.

   * External libraries used:
     1. 

5. Description of SpanBERT and GEMINI method:
   *SpanBERT[SB]:

   * Gemini[run_gemini]:
     Input Web content:doc that has been processed by spaCy, entities_of_interest and relation_index, GEMINI_KEY, relation sets: X; update relation sets: X
     1. Loop over sentences in doc.
     2. Check if the sentence has required named entities pair(s) using spaCy.[create_entity_pairs]
     3. If yes, generate the prompt with the plain-text sentence and designated relation. In this part, the prompt is originally a one-shot learners, and will expand with extracted relations 
 to maximum 3-shot learners.[gemini.generate_prompt]
     4. Feed the prompt into Gemini model and get response.[get_gemini_completion]
     5. Process response. Parse the response into lists of list and if the form of the list is correct update the relation in relation sets. In this step, since we update the dictionary by setting "tuple of relation:1", where 1 is the default confidence for all relationship extracted by Gemini, we do not have to handle the diplicate promblem.
   ** Note: To avoid termination with Gemini Resource Exhausted, the program will rest for 10 seconds when catch this error.
   ** Note: If the sentence is processced by Gemini but the return relation is not coherent with the defined format, the # of extracted annotaion from Gemini will increase, but no relation will be added to the finel set.
   **Gemini configuration is set as followed:
```
model_name ="gemini-1.0-pro"
max_tokens =  100 #0-8192, expecting short response
temperature = 0.2 #more deterministic, 0-1, control the return format
top_k = 32 #next-token can,1-40, default =32
top_p = 1 #select cum. threshold, 0-1, default =1
```

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
   * When handling the output of the Gemini, we should be careful of the return format. Since Gemini generate next token by the largest possibility, the format of the output might varies. We can set lower temperature or more specific prompt to reduce this incoherent.
   
