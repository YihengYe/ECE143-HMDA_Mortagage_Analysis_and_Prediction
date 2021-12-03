# ECE143-HMDA_Mortagage_Analysis_and_Prediction

This is the project made by ECE 143 Group 12 to analyze and predict HMDA Mortage. Please find our result visualizations in Report.ipynb at the root directory and run our code according to the guideline below. Our presentation is ECE143 Group12 Presentation.pdf. Our results visualizations (pngs) are under the result directory. Our large csv files are store with git lfs, so please install git lfs (type "git lfs install") in your local repository before you try to pull our repository, or you can 
download them manually.

### Project Team Members:
- Yiheng Ye, yiy291@ucsd.edu
- Zhiyin Liu, zhl114@ucsd.edu
- Luobin Chen, luc004@ucsd.edu
- Zicheng Wei, z7wei@ucsd.edu
- Yanzhi Yao, yayao@ucsd.edu

### Requirements:
- python 3.9
- pandas 1.3.4
- numpy 1.21.4
- matplotlib 3.5.0
- sklearn 1.01

### CSV Structure:
- There are several csvs file in the data directory to be used for our analysis. Basically, there are columns which encoding the features into numerical number beginning with 1 in our data set, and thus we leave those columns alone to make an easier analysis (The other csvs that not mentioned in this list are mid-point data
sets that we temporarily used in our analysis process, which are irrevlevant in final results, but we still keep them as a reference):
- data/raw/hmda_2017_ca_all_records_labels.csv: Our raw data set with all column of features (including corresponding coding columns)。
- data/csvs/hmda_2017_ca_all_records_labels.csv: The same one as the above one. This one is used for analysis purpose。
- data/csvs/hmda_2017_ca_noname.csv: Leave only columns with coding values and numerical values for easier and more efficient analysis. It only contains rows whose column "action_taken" value is in [1,2,3,8,7]. In our EDA process, action [1,2,8] is "approved", and [3,7] is denied.
- data/cleaned/hmda_2017_ca_all-records_agg_sex.csv: aggregate code values of applicant_sex & add compacted features like has_applicant, approved etc.

### Code, Purpose, and Guideline:
- First of all, our notebook that represents all our visualization result is "Report.ipynb", which is at the root directory. The notebooks directory is only for our coding process and communication for each individual discoveries.
- Report.ipynb: our report for all the visualizations we created in this project. Please keep it in the root directory when running it.
- src/data_processing/DownScale.py: downscale the raw data into hmda_2017_ca_noname.csv. You can just run it by "python DownScale.py"
- src/data_processing/code_map.json: code map for numerical code and string column values for different feature. Important for other analysis scripts.
- src/data_processing
  - code.py: generate code value map for categorical data (include the validation function)
  - numeric.py: categorize features into groups, read the .csv dataset with strict dtypes
  - compact.py: USED FOR PREDICTION, generate compacted features
- src/models
  - feature.py: pre-processing for different kinds of features
  - regression_model.py: train the logistic regression model and print out corresponding outcomes
- Python scripts in src/visualizations: Those scripts represent our analysis and visualizations process on each different features stated in their file names. Please check if you have data/csvs/hmda_2017_ca_noname.csv before running them, or, please running src/data_processing/DownScale.py before running those scripts. Those scripts are designed only to be ran under the root directory/src directory and its child directories/notebook directory, and please do not put our root directory under some directores named "src" or "notebook" before trying running those scripts. Use "python filename.py" to run those scripts. When running the scripts, the visualizations we make will pop out and one needs to close them after taking a look at them to proceed the script running. After the running process is done, the visualizations generated will be placed in result/eda directory.

### Responsibilities:
- Yiheng Ye: Set up the directory and managed the coding workflow. Downscaled the data set by writing the DownScale.py Wrote visualizations for gender in Gender_analysis.py. Debugged others' code. Wrote the EDA part in Report.ipynb and parts of Readme documentation including document structure and some code guideline.
Discussed analysis contents with teammates to organize project structure. Collaborated in making the presentation slides.
- Zicheng Wei: Set up code value maps for categorical data and determined dtypes for pandas dataframe. Wrote data pre-processing (i.e. dummy encoding, log operation) for model training and logistic regression model. Researched into the model training procedure including data augmentation and visualized corresponding outcome. Collaborated in making the presentation slides.
- Yanzhi Yao: Analyze and visualise the race and ethnicity section. Discussed analysis contents with teammates and help to organize the visualise style. Wrote the Raw_EDA_3_Race analysis.ipynb and Raw_EDA_4_Ethnicity_analysis.ipynb notebook. Modified and reorganized the code of race and ethnicity anaysis into 
Race_analysis.py and Ethnicity_analysis.py. Collaborated in making the presentation slides.
- Luobin Chen:Participating in choosing data base. Actively discussed EDA analysis contents with teammates and develop visualizations for "income" attribute in income_analysis.py. Collaborated in making the presentation Slide. Group dataset to be good to be visualized. 
- Zhiyin Liu: Worked on the Naive Bayes Classifier. Worked on creating the presentaion slides with others. Actively discuss with teammates of the prediction model result and issues we have to deal with while working on the classifier.

### References:
- HMDA data set, https://www.consumerfinance.gov/data-research/hmda/historic-data/
- Code Explanation for LAR data, https://files.consumerfinance.gov/hmda-historic-data-dictionaries/lar_record_codes.pdf

