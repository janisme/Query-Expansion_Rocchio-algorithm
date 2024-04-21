# Project3: Association Rules Extraction
## Purpose
This project is an associate rules extraction system designed to find the implied associate rules given minimum support and confidence rates.

   The project takes a user query, specifying the location of the .csv file that contains the “market basket,” a minimum support rate, and a minimum confidence rate, as input. The system will run the apriori algorithm to find the frequent itemsets with a support rate greater or equal to the minimum support rate. After finding all the frequent itemsets, the system will generate only association rules with exactly one item on the right side and at least one item on the left side and retain only the rules with a confidence of at least a minimum confidence rate. 

  The objective is to correctly implement this system of the association rule mining algorithm on official New York City data sets.

   This project was developed in Spring 2024 for the course COMS 6111 Advanced Database Systems taught by Professor Luis Gravano at Columbia University.
   Reference: https://www.cs.columbia.edu/~gravano/cs6111/proj3.html
## Detail
1. Group members: Dawei Yin, dy2482 & Yenchu Chen, yc4360
2. List of files:
   Folder Structure
```sh
|-data ## The data_root for our evaluation dataset
|   |-data_cleaner.py # This Python script is designed to clean data downloaded from the NYC Open Data portal.
|   |-INTEGRATED-DATASET.csv # Cleaned data
|-main.py  
|-apriori_algo 
|-example-run.txt
|-requirements.txt
```

    * `main.py`: This is the main Python file responsible for processing the input user query, preprocess the transaction from csv file, generating L1 frequent itemset and running the apriori algorithm .
    * `apriori_algo.py`: This Python file contains several functions used to generate the frequent itemsets list and associate rules.
    * `README.md`: This file contains a description of the project, providing an overview of its purpose and functionality.
    * `requirements.txt`: This file lists all the packages used in the project, ensuring compatibility and ease of setup for other users.
    * `example-run.txt`: This file contains the results of our project.
    * `data`: This file contains the script to clean the data downloaded from the NY Open data portal and the cleaned data.
    
3. Instruction to run the project:

 Enter into the directory where the main.py file is located. Install Python Packages
   ```pip install -r requirements.txt   ```

Run: python3 main.py <dataset_file> <min_support_rate> <min_confidence_rate>
    * Take min_support_rate as 0.07, min_confidence_rate as 0.85 with datafile location as data/INTEGRATED-DATASET.csv.
   ```
python3 main.py data/INTEGRATED-DATASET.csv 0.07 0.85 > example-run.txt
   ```
