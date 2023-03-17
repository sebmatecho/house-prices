# Housing Dynamics in King County (USA)
### Proposed by [Sébastien Lozano-Forero](https://www.linkedin.com/in/sebastienlozanoforero/)

Project deployed [here](https://dashboardhouseprices2.herokuapp.com/).
## Project information
This project was proposed as way to showcase my skills, as part of my [Data Science Portfolio](https://sebmatecho.github.io/Portfolio/). This end-to-end project starts with raw data (thanks Kaggle!) and ends with an app running in production able to describe housing dynamics and suggesting prices using a Machine Learning model.  
#### Methods used
- Exploratory Data Analysis (EDA)
- Data Visualization
- Machine Learning 
- Software Development
#### Technologies
- Python (Pandas, Folium, Sckit-Learn, etc)
- Streamlit 
- Heroku

## Project Overview
This project aims to generate value out of one year of historical information of housing dynamics in King County (WA). This dataset is available in [Kaggle](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction). The dataset contains information about number of rooms, bathrooms, location (latitude and longitude), number of floors, waterfront, view of water mark, construction assessment, footage and specially, price, among others.

Based on the provided information, we aim to add value to such data in two ways:
i. Developing a tool to better understand dynamics in the housing market of such region, and
ii. Propose a suitable and reasonable manner to suggest prices to given properties. 

## Used Approach

The CRoss-Industry Standard Process for data mining (CRISP) methodology was used. This is, the life cycle of the project is given by the following figure.

<img src="img/IBM.jpg" width="400" height="400" />

## Data Overview

In general, the data was pretty clean (thanks again, Kaggle!). The following properties were observed: 
- Data contains properties sales within a year of observation (May 2014 to May 2015)
- ~21K data rows were observed
- 22 variables were included in the dataset, including price. 
- 95% of the properties would cost less than 1M USD. Some properties displayed a considerably high value (over 2M USD)
- In general, prices were driven by the quality of the view of water, footage and assesment of the construction, mainly. 

## Machine Learning
After an exhaustive process of algorithm adjustment including various data preparation strategies, the following metrics were found.

| Model | MAE |MAPE |RMSE | R2 |
| --- | --- | --- | --- | --- |
|Linear Regression |	0.25016+/-0.01|	0.09774+/-0.01|	0.31239+/-0.01	|0.59502+/-0.01|
|Ridge Regression |	0.25011+/-0.01|	0.09769+/-0.01|	0.31231+/-0.01|	0.59526+/-0.01|
|Lasso Regression |	0.25012+/-0.01|	0.09769+/-0.01|	0.31231+/-0.01|	0.59525+/-0.01|
|Elastic Regression| 0.25012+/-0.01	|0.09769+/-0.01|	0.31231+/-0.01|	0.59525+/-0.01|
|k nearest neighbor| 0.25469+/-0.01	|0.10378+/-0.01|	0.32156+/-0.02|	0.57125+/-0.03|
|Decision Tree |	0.24418+/-0.01	|0.09579+/-0.01|	0.30906+/-0.02|	0.60391+/-0.02|
|Random Forest|	0.2433+/-0.01	|0.09753+/-0.01|	0.31194+/-0.02|	0.59635+/-0.02|
|XGboost	|0.23545+/-0.01|	0.08861+/-0.01|	0.29738+/-0.01|	0.63314+/-0.01|
|RANSAC	|0.2501+/-0.01	|0.09769+/-0.01|	0.3123+/-0.01|	0.59529+/-0.01|

After selecting the XGBoost model, a random search procedure was implemented in order to get the best possible model out of the XGBoost category. For this, a grid of potential values for the parameter model (n_estimators, eta, max_depth, subsample, colsample_bytree and min_child_weight, see [here](https://xgboost.readthedocs.io/en/stable/parameter.html9) for more) was assessed. After a extensive search process, an adequate set of parameters was found and implemented. The final model displayed the following goodness of fit metrics. 

| Model | MAE |MAPE |RMSE | R2 |
| --- | --- | --- | --- | --- |
|XGboost	|0.23538+/-0.01|	0.08858+/-0.01|	0.29733+/-0.01	|0.634+/-0.01|
## Deployment

The entire app was developed using Streamlit. It would include two main pages, one providing information for the dynamics of the housing market while the second one would suggest prices, based on the Machine Learning model, once the specifics of the property of interest were input by user. It was deployed within Heroku and the final version (fully functional) might be found [here](https://dashboardhouseprices2.herokuapp.com/). 

## Feedback
Feedback is always a gift, specially the constructive it. Please, feel free to reach out to slozanof1991 at gmail dot com to provide any, if available. Thank you. 