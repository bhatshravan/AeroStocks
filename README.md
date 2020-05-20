# AeroStocks

A stock market prediction platform for parsing and predicting stock market index prices based on news articles and machine learning.


## Folder Structure Overview
* documentation - Some of our presentation and various notes taken.
* python - All the code.
* website - Contains the code for our website

#### Requirements.txt will be uploaded soon

## Running the project
1. You need to download all news articles by manually specifying parameters in python/download/news/threads.py. It does multithreading and downloads parallelly saving time.
* You have to manually uncomment each line and check dates. This will download news to python/data/news/[newspaper]/lists/[various-file]
* Then run merge.py and specify parameters to merge all the news files.

2. Run the NLP classifier.
* Run python/nlp/classify.py and give input file as in_csv variable. Specify output file location in output_file in makeKeyWordList function and ensure write_to_file variable is set to 1.
* This outputs multiple files in output location which needs to be merged again with merge.py

3. Do machine learning for prediction.
* Append the header to csv as `date,stock,vader,secscore,assoc,perc,percword,sector,index,news` and feed that as input to python/classifier/Predict.ipynb to see all results.
