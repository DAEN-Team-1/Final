# Final

<h2> Project's Title </h2>

Automating Matching of NOTAM to Space Vehicle Operations

<h2> Project Description </h2> 

The Federal Aviation Administration’s (FAA) Systems Analysis & Requirements Services Modeling Division has a requirement to measure the impact of Space Vehicle Operations (SVOs) on the National Airspace as it pertains to operational efficiency.  The goal of this project is to match past Notice to Airmen (NOTAM) messages to historical SVOs to establish a baseline measure of the impacts of these operations.  The FAA will be able to predict the impacts of future SVOs by extrapolating from this baseline.  Historical efforts to establish such a baseline have been based on keywords and manual evaluation of the data which proved time-consuming and produced limited results. For our analysis, we applied basic machine learning techniques to achieve more comprehensive results.  For our initial processing, we decoded the NOTAM contractions and abbreviations into plain text, removed stopwords and then applied multiple NLP models (Topic Modeling, SVM, XG Boost and Logistic Regression) in order to engineer features associated with each NOTAM message.  All supervised NLP models were trained and evaluated using hand labelled datasets created by the FAA as well as a second data set created by our team. We then applied a Faceted Search to match the results to specific SVOs using several filters applied sequentially including message attribute filters (Start/End Date , Max Alt., Classification, Location Code,), geospatial filters, topic filter, and an ensemble voting filter using a stack model.  The dataset used consisted of a 1.6 million NOTAM records and 518 SVOs.  After applying our technique, we matched a total of XX NOTAM records to XX different SVOs.  These results showed considerable improvement over the 452 matches to 62 SVOs produced by the previous analyses.

**Keywords:** Topic Modeling, Support Vector Machines (SVM), XG Boost, Logistic Regression, NOTAM

<h2> How to Install and Run the Project </h2> 

1. Required SW
    - xxx
    - yyy
    - xxx
    - ddd
    
3. Notebook Description and Run Order
    - sdfdf
    - dfdfg

<h2> Credits </h2> 

   1. Teresa Bray
   2. Kevin Brensike - https://github.com/GarBearII
   3. Sergio Rego
   4. Douglas Williamson - https://github.com/dougwilliamson
   5. James Woods - https://github.com/jwoods-rpa
