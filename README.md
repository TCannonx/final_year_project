# Final year project Repository

This repository contains the code and datasets necessary to complete an analysis on predicting football player positions and identifying similarities between players from the world's top football leagues. The objective of this project is to utilize data retrieved from a 3rd party source to make accurate predictions on players' positions and explore clustering and classification methods using past season's performance data.

### Dataset
The dataset used in this project is a combination of data from FBREF, encompassing the most recent season of football from the top 11 leagues worldwide. The dataset contains over 100 data points for each individual player, providing comprehensive information on their performance throughout the season. Another dataset containing player positon labels was also used throughout the course of this project which was kindly supplied by @Jase_Ziv83 on Twiitter.

### Objective
The primary goal of this project is to develop a machine learning model that can accurately predict football players' positions. Additionally, the project aims to identify similarities between players using various clustering and classification methods. By achieving accurate predictions and identifying player similarities, the project aims to facilitate talent identification, scouting, and analysis of transfer prospects for professional football clubs and scouts.

### Methods
Several machine learning methods and technologies were analyzed throughout the course of this project. Some of the methods tested include:  
  
K Means clustering  
K-Nearest Neighbors (KNN)  
Support Vector Machines (SVM)  
Transfer learning, specifically through the use of Support Vector Machines, was applied to the raw data to create a high-level vector space, with the aim of improving prediction accuracy  

### Results
The highest accuracies achieved by the various models created are as follows:  
  
Players Position Category through SVM: 88.3% accuracy  
Players Sub-Position through SVM: 74.84% accuracy  
Furthermore, a more accurate model was developed to identify similar players across different leagues. The effectiveness of this model was verified through a questionnaire distributed to participants with an interest in football. The results of a T-test indicated a significant preference for the output of the proposed improved model.  
  
### Repository Structure
The repository is structured as follows:  
  
#### Code:
Analysis_Notebook.ipynb: Main Notebook for Analysis  
fbref_scraping.ipynb: Notebook used to obtain fbref data using web scraping techniques  
questionnaire-analysis.ipynb: To analyse the results of the choices made by teh participants of the questionnaire  
Dahsboard.py: dashboarding app created as a result of the analysis  

#### Datasets:
all_leagues_s1_22.csv: Contains all player performance data used for the purpose of the analysis  
manual_test.csv: manual testing dataset whcih was removed from the training and validation set to validate the finished models  
players.csv: Player positional data provided by @Jase_Ziv83 on Twiitter  
