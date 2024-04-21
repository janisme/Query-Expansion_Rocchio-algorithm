# Project3: Association Rules Extraction
## Purpose
This project is an associate rules extraction system designed to find the implied associate rules given minimum support and confidence rates.

   The project takes a user query, specifying the location of the .csv file that contains the “market basket,” a minimum support rate, and a minimum confidence rate, as input. The system will run the apriori algorithm to find the frequent itemsets with a support rate greater or equal to the minimum support rate. After finding all the frequent itemsets, the system will generate only association rules with exactly one item on the right side and at least one item on the left side and retain only the rules with a confidence of at least a minimum confidence rate. 

  The objective is to correctly implement this system of the association rule mining algorithm on official New York City data sets.

   This project was developed in Spring 2024 for the course COMS 6111 Advanced Database Systems taught by Professor Luis Gravano at Columbia University.
   Reference: https://www.cs.columbia.edu/~gravano/cs6111/proj3.html
## Detail
1. Group members: Dawei Yin, dy2482 & Yenchu Chen, yc4360
2. Folder Structure
```sh
|-data ## The data_root for our evaluation dataset
|   |-data_cleaner.py # This Python script is designed to clean data downloaded from the NYC Open Data portal.
|   |-INTEGRATED-DATASET.csv # Cleaned data
|-main.py  
|-apriori_algo 
|-example-run.txt
|-requirements.txt
```
3. List of files:
    * `data`: This file contains the script to clean the data downloaded from the NY Open data portal and the cleaned data.
    * `main.py`: This is the main Python file responsible for processing the input user query, preprocess the transaction from csv file, generating L1 frequent itemset and running the apriori algorithm .
    * `apriori_algo.py`: This Python file contains several functions used to generate the frequent itemsets list and associate rules.
    * `README.md`: This file contains a description of the project, providing an overview of its purpose and functionality.
    * `requirements.txt`: This file lists all the packages used in the project, ensuring compatibility and ease of setup for other users.
    * `example-run.txt`: This file contains the results of our project.
    
4. Instruction to run the project:
   
      Enter into the directory where the main.py file is located. Install Python Packages.
      ```
      pip install -r requirements.txt
      ```

      Run: python3 main.py <dataset_file> <min_support_rate> <min_confidence_rate>
    * Testing with toy sample, take min_support_rate as 0.75, min_confidence_rate as 0.8 with toy dataset 'toy'.
      
      ```
      python3 main.py toy 0.75 0.8
      ```
      
      result:
       ```
      Finding k =  1 itemset, ck length:  3
      Finding k =  2 itemset, ck length:  0
      =====Frequent itemsets (min_sup=75.0%)
      [pen], Supp: 100.00%
      [diary], Supp: 75.00%
      [ink], Supp: 75.00%
      [diary,pen], Supp: 75.00%
      [ink,pen], Supp: 75.00%
      Total number of frequent itemsets:  5
      =====High-confidence association rules (min_conf80.0%)
      [diary] => [pen] :  (Conf: 100.00%, Supp: 75.00%)
      [ink] => [pen] :  (Conf: 100.00%, Supp: 75.00%)
      Total number of associate rules:  2
        ```
      
5. Description of the data:

   a. Which NYC Open Data data set(s) we used to generate the INTEGRATED-DATASET file?

   The NYC Open Data we use is the “NYPD Arrest Data (Year to Date)” from https://data.cityofnewyork.us/Public-Safety/NYPD-Arrest-Data-Year-to-Date-/uip8-fykc/about_data. This is a breakdown of every arrest effected in NYC by the NYPD during the year of 2023.
 This data is manually extracted every quarter and reviewed by the Office of Management Analysis and Planning.


   b. What (high-level) procedure we used to map the original NYC Open Data data set(s) into INTEGRATED-DATASET file?
   
   The data cleaning process is outlined as follows:
      1. Column Evaluation: We assess the columns in the original dataset and retain those that are relevant to our analysis which are "ARREST_DATE","OFNS_DESC", "LAW_CAT_CD","ARREST_BORO","AGE_GROUP","PERP_SEX", "PERP_RACE".
      2. Null Value Filtering and Date Simplification: We filter out any rows containing null values across all columns. Additionally, dates in the format of mm/dd/yyyy are simplified to retain only the month (mm).
      3. Conversion to Dummy Values: The data is then transformed into dummy variables for further analysis.
  
   c. What makes your choice of INTEGRATED-DATASET file compelling?

   Our selection of the NYC Open Data dataset on criminal records is driven by a profound curiosity about the patterns and backgrounds associated with criminal activities within New York City. This dataset presents an invaluable opportunity for an in-depth analysis of the correlation between specific types of crimes and their occurrence in particular regions, as well as the potential connections between these crimes and the backgrounds of the individuals involved. By dissecting this data, we aim to uncover insights that could contribute to a better understanding of the dynamics of crime in the city, potentially guiding preventive strategies and policy making to enhance safety and justice for all New Yorkers.

   d. columns explanation:
   * ARREST_DATE : [1~12], represent the month of arrest for the reported event.
   * OFNS_DESC : Description of internal classification.
   * LAW_CAT_CD: Level of offense: felony, misdemeanor, violation.
   * ARREST_BORO: Borough of arrest. B(Bronx), S(Staten Island), K(Brooklyn), M(Manhattan), Q(Queens).
   * AGE_GROUP: Perpetrator’s age within a category.{'AGE_GROUP_18-24', 'AGE_GROUP_25-44', 'AGE_GROUP_45-64', 'AGE_GROUP_65+', 'AGE_GROUP_<18'}
   * PERP_SEX: Perpetrator’s sex description.{'PERP_SEX_F', 'PERP_SEX_M', 'PERP_SEX_U'}
   * PERP_RACE: Perpetrator’s race description.{'PERP_RACE_AMERICAN INDIAN/ALASKAN NATIVE', 'PERP_RACE_ASIAN / PACIFIC ISLANDER', 'PERP_RACE_BLACK', 'PERP_RACE_BLACK HISPANIC', 'PERP_RACE_UNKNOWN', 'PERP_RACE_WHITE', 'PERP_RACE_WHITE HISPANIC'}
  
6. Description of the internal design of this project:
   * High-level Concept:
     1. In `main.py`, the system initiates data preparation, generating the initial frequent itemset (L1) and compiling a list of transactions for analysis.
     2. It then invokes the `apriori` function, supplying it with these initial itemsets, the list of transactions, and a specified support threshold, to identify all frequent itemsets.
     3. Within the `apriori` function, an iterative process seeks out k-itemsets by crafting candidate sets (Ck) through the apriori_gen_with_prune method, drawing from the previously identified frequent itemset (Lk-1). It retains only those subsets present in transactions, subsequently calculating each subset's occurrence rate by dividing its count by the total number of transactions, and recording these in a dictionary.
     4. The `apriori_gen_with_prune` function constructs candidate itemsets (Ck) from Lk-1, excluding any that lack complete subsets in Lk-1, ensuring only potentially frequent itemsets proceed to the next stage of analysis.
     5. With a comprehensive list of frequent itemsets at hand, the system employs the `calculate_conf` function to assess potential rules' confidence levels. This is achieved by comparing the support of the composite itemset (LHS U RHS) against that of the LHS alone. Only those rules that surpass the predefined confidence threshold are retained.

        
7. Explanation of the result:
   After running the following query
      ```
      python3 main.py data/INTEGRATED-DATASET.csv 0.07 0.8
      ```
   The system find itemsets that contain <= 3 items and generated 106 frequent itemsets and 27 association rules.

   The analysis of the high-confidence association rules, especially with a minimum confidence threshold of 80%, reveals significant patterns within the context of criminal offenses and demographics in New York City. These rules are compelling for several reasons:

      1. High Confidence in Offense to Law Category Mapping: The rules with 100% confidence linking offense descriptions like "Felony Assault" and "Assault 3 & Related Offenses" to specific law categories (F for felony and M for misdemeanor) indicate a direct correlation between the nature of the offense and its legal classification.
      2. Demographic Patterns in Offenses: The rules reveal demographic patterns in offenses, such as "Assault 3 & Related Offenses" being predominantly associated with males (PERP_SEX_M) and specific age groups (25-44). This points towards demographic trends in criminal behavior, which can be critical for law enforcement agencies to develop targeted preventive measures or community programs.
      3. Racial and Gender Disparities: The association of "PERP_RACE_BLACK HISPANIC" and "PERP_RACE_BLACK" with male perpetrators at high confidence levels (ranging from 81.26% to 83.90%) sheds light on racial and gender disparities in recorded offenses. This could reflect societal, systemic, or enforcement biases that require further investigation and action to ensure equitable justice practices.
      4. Geographical Insights: The appearance of "ARREST_BORO" (borough of arrest) in the rules suggests geographical patterns in crime, with specific boroughs like Brooklyn (B), Manhattan (M), and Queens (Q) showing a higher association with male perpetrators. This geographic specificity can aid in allocating resources more efficiently and tailoring interventions to the unique needs of each borough.
      5. Temporal Patterns: Rules associating arrest dates with male perpetrators, although with slightly lower confidence, hint at temporal patterns in criminal activities. This could inform law enforcement and community leaders about potential seasonal or periodic trends in crime rates, enabling proactive measures.
      Overall, these rules not only affirm expected patterns within crime data, such as the strong link between certain offenses and their legal categories but also uncover deeper demographic, geographical, and temporal insights. The clear gender, race, and age-related patterns, in particular, call for a nuanced understanding and response from policymakers, law enforcement, and community organizations to address the underlying causes and ensure a fair justice system.

8. Additional information:
   None.
   
