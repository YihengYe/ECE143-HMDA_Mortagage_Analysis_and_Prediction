# ECE143-HMDA_Mortagage_Analysis_and_Prediction

This is the project made by ECE 143 Group 12 to analyze and predict HMDA Mortage. Please find our result visualizations in Report.ipynb at the root directory and run our code according to the guideline below. Our results visualizations (pngs) are under the result directory。

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

### CSV Structure:
- There are several csvs file in the data directory to be used for our analysis. Basically, there are columns which encoding the features into numerical number beginning with 1 in our data set, and thus we leave those columns alone to make an easier analysis:
- data/raw/hmda_2017_ca_all_records_labels.csv: Our raw data set with all column of features (including corresponding coding columns)。
- data/csvs/hmda_2017_ca_all_records_labels.csv: The same one as the above one. This one is used for analysis purpose。
- data/csvs/hmda_2017_ca_noname.csv: Leave only columns with coding values and numerical values for easier and more efficient analysis. It only contains rows whose column "action_taken" value is in [1,2,3,8,7]. In our EDA process, action [1,2,8] is "approved", and [3,7] is denied.


### Code, Purpose, and Guideline:
- First of all, our notebook that represents all our visualization result is "Report.ipynb", which is at the root directory. The notebooks directory is only for our coding process and communication for each individual discoveries.
- Report.ipynb: our report for all the visualizations we created in this project. Please keep it in the root directory when running it.
- src/data_processing/DownScale.py: downscale the raw data into hmda_2017_ca_noname.csv. You can just run it by "python DownScale.py"
- src/data_processing/code_map.json: code map for numerical code and string column values for different feature. Important for other analysis scripts.
- src/data_processing: WIP, please fill out in those lines about other script.
- Python scripts in src/visualizations: Those scripts represent our analysis and visualizations process on each different features stated in their file names. Please check if you have data/csvs/hmda_2017_ca_noname.csv before running them, or, please running src/data_processing/DownScale.py before running those scripts. Those scripts are designed only to be ran under the root directory/src directory and its child directories/notebook directory, and please do not put our root directory under some directores named "src" or "notebook" before trying running those scripts. When running the scripts, the visualizations we make will pop out and one needs to close them after taking a look at them to proceed the script running. After the running process is done, the visualizations generated will be placed in result/eda directory.

### Responsibilities:
- Yiheng Ye: Set up the directory and managed the coding workflow. Downscaled the data set by writing the DownScale.py Wrote visualizations for gender in Gender_analysis.py. Debugged others' code. Wrote the EDA part in Report.ipynb and parts of Readme documentation including document structure and some code guideline.
Discussed analysis contents with teammates to organize project structure. Collaborated in making the presentation PPT.