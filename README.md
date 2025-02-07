# Final

<h2> Project's Title </h2>

Automating Matching of NOTAM to Space Vehicle Operations

<h2> Project Description </h2> 

The Federal Aviation Administration’s (FAA) Systems Analysis & Requirements Services Modeling Division has a requirement to measure the impact of Space Vehicle Operations (SVOs) on the National Airspace as it pertains to operational efficiency.  The goal of this project is to match past Notice to Air Missions (NOTAM) messages to historical SVOs to establish a baseline measure of the impacts of these operations.  The FAA will be able to predict the impacts of future SVOs by extrapolating from this baseline.  Historical efforts to establish such a baseline have been based on keywords and manual evaluation of the data which proved time-consuming and produced limited results. For our analysis, we applied basic machine learning techniques to achieve more comprehensive results.  For our initial processing, we decoded the NOTAM contractions and abbreviations into plain text, removed stopwords and then applied multiple NLP models (Topic Modeling, SVM, XG Boost and Logistic Regression) in order to engineer features associated with each NOTAM message.  All supervised NLP models were trained and evaluated using hand labelled datasets created by the FAA as well as a second data set created by our team. We then applied a Faceted Search to match the results to specific SVOs using several filters applied sequentially including message attribute filters (Start/End Date , Max Alt., Classification, Location Code), geospatial filters, topic filter, and an ensemble voting filter using a stack model.  The dataset used consisted of a 1.6 million NOTAM records and 518 SVOs.  After applying our technique, we matched a total of 1404 NOTAM records to 191 different SVOs.  These results showed considerable improvement over the 452 matches to 62 SVOs produced by the previous analyses.

**Keywords:** Topic Modeling, Support Vector Machines (SVM), XG Boost, Logistic Regression, NOTAM

<h2> How to Install and Run the Project </h2> 

1. Required Python Libraries
    - sklearn (v0.0) - https://scikit-learn.org/stable/ 
    - nltk (v3.7) - https://www.nltk.org/
    - numpy (v1.22.3) - https://numpy.org/
    - pandas (v1.4.2) - https://pandas.pydata.org/
    - pyLDAvis (v3.3.1) - https://pyldavis.readthedocs.io/en/latest/index.html
    - matplotlib (v3.4.3) - https://matplotlib.org/
    - wordcloud (1.8.1) - http://amueller.github.io/word_cloud/
    - Shapely (v1.8.2) - https://shapely.readthedocs.io/en/stable/index.html
    - geopandas (v0.11.0) - https://geopandas.org/en/stable/
    - xgboost (v1.6.1) - https://xgboost.readthedocs.io/en/stable/
    
2. Notebook Descriptions and Run Order (SRC Folder)
    1. DataProcessing.ipynb - reads in original source files and cleans the columns needed for the model.  Also saves the resulting dataframe as a pickle (.pkl) file.
    2. AddTopics.ipynb - reads in the .pkl file from the processing step creates a topic model for all NOTAM text.  Topic analysis using pyLDAvis as well as word clouds is also included.  All topic predictions are added to the dataframe and saved as a .pkl file.
    3. DataGenerator.ipynb - read in .pkl file and uses various facet filters to generate a new test dataset used in the classification NLP models.  This dataset is used to augment the given matched dataset from the FAA.  New dataset is saved as .csv files.
    4. NLP_ModelCompare.ipynb - reads in FAA matched dataset as well as the handmade (team generated) dataset and creates several classification models using the datasets.  Notebook also contains our model analysis, namely cross validation accuracy plots, receiver operating curves (ROC), and Area Under the Curve (AUC).  Model predictions are then added to the dataframe and saved in .pkl file.
    5. DataFiltering-NoKeywords - performs facet search for matches using no keywords (uses topics instead).  Also shows matchings analysis based on FAA matched set.
    6. DataFiltering-WithKeywords - performs facet search for matches using keywords.  Also shows matchings analysis based on FAA matched set.
    7. PlotLaunch.ipynb - reads in matched results and allows user to plot any launch results and associated NOTAM polygons.
    8. MatchedAnalysis.ipynb - read in .pkl file and FAA annotated matches datasets. Generates Topic and Classification histograms, and prints the E-code message of selected NOTAM to allow comparison of the data between the full unlabelled dataset and the FAA matched dataset.

3.  Notebook Descriptions and Run Order (EDA Folder)
    1. eda_basic_all.ipynb - reads original source files (not included here due to size) to do basic EDA
    2. explore_NOTAM_in_pkl.ipynb - reads notam in pkl after topics and augmented text functions complete; performs EDA on this updated data set
    3. file_EDA_NOTAM_before_pkl.py - reads original notam data file and performs EDA, focus on start and stop dates by year
    4. human_annotated_notam_analysis.ipynb - reads labeled data set and performs EDA funcitons; all labeled data between 2016 and 2020
    5. launch_time_analysis_3.ipynb - reads launch data and notam in pkl after topics and augmented text functions complete; does detailed launch vs notam time analysis
    6. launch_time_compare_before_pkl.py - reads original launch and notam files without pre-processing; does initial launch vs notam time analysis
    7. notam_analysis_1.ipynb - detailed eda on the original large notam file
    8. count_results.py - counts the total number of unique NOTAM matched to launches in our output results/csv file


<h2> Credits </h2> 

   1. Teresa Bray - https://github.com/stbray
   2. Kevin Brensike - https://github.com/GarBearII
   3. Sergio Rego - https://github.com/srego
   4. Douglas Williamson - https://github.com/dougwilliamson
   5. James Woods - https://github.com/jwoods-rpa
