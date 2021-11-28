import pandas as pd
import os
import matplotlib.pyplot as plt
import json

"""
Generating visualization for Gender in the data set
"""

def get_parent_path():
    """
    get root parent path for this file

    :return: the root parent path
    """
    allDir=os.getcwd().split('\\')
    for i in range(len(allDir)):
        if allDir[i] in ['src', 'notebooks']:
            result=os.getcwd()[:-(sum(map(len,allDir[i:]))+1*(len(allDir)-i))]
            return result
    return os.getcwd()

def get_code_map():
    """
    get the code map and change all str code to integer

    :return: the code map for all values
    """
    parent_path=get_parent_path()
    js_road=parent_path+"/src/data_processing/code_map.json"
    with open(js_road, 'r') as fh:
        code_map=json.load(fh)
        for i in code_map.keys():
            code_map[i]={int(m):n for m, n in code_map[i].items()}
    return code_map

def Gender_coding(code_map):
    """
    Shorten the original name for code 4 to "Information not provided by applicant"

    :param code_map: the originial code map
    :return: The updated gender code map
    """
    gender_dict=code_map['sex'].copy()
    gender_dict[3]='Unknown'
    gender_dict[4]='Unknown'
    return gender_dict

def Generate_Gender_Plots(df,genderMap, parent_path, image_path):
    """
    Generate Gender Analysis Plots

    :param df: the skimmed data set
    :param genderMap: the Gender code map
    :param parent_path: root parent path
    :param image_path: the image path
    """
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    
    
    Sex_total=df['applicant_sex'].replace(genderMap).value_counts()
    # Draw Gender composition for All applicants
    plt.figure()
    Sex_total.plot.pie(legend=False, title='Gender Composition for All Applicants',autopct='%1.1f%%')
    plt.savefig(image_path+'Total_applicant_gender.png', bbox_inches='tight')
    plt.close()

    # Making analysis on applicant sex vs approval 
    Sex_result=df[['applicant_sex','action_taken']]
    RecodeAction={1:"Institution approved",2:"Institution approved", 3:'Institution denied', 7:'Institution denied',8:'Institution approved'}
    Sex_result_b=pd.DataFrame()
    Sex_result_b['action']= Sex_result['action_taken'].replace(RecodeAction)
    Sex_result_b['applicant_sex']=Sex_result['applicant_sex'].replace(genderMap)
    Sex_result_a1=Sex_result_b.pivot_table(index='applicant_sex', columns='action',aggfunc='size',fill_value=0)
    plt.figure() #Gender application resultcount
    Sex_result_a1.plot.bar(title='Application Result Counts vs Gender')
    plt.xticks(rotation=45)
    plt.ylabel('count')
    plt.savefig(image_path+'Application_result_count_gender.png', bbox_inches='tight')
    plt.close()

    totalSA1=Sex_result_a1.sum(axis=1)
    Sex_result_a2=Sex_result_a1.T
    temp=Sex_result_a2/totalSA1.values
    Sex_result_a2=temp.T*100
    plt.figure()
    SA2B=Sex_result_a2.plot.bar(title='Application Result Precentage vs Gender')
    for p in SA2B.patches:
        SA2B.annotate(str("%.2f"%p.get_height())+'%', xy=(p.get_x(), p.get_height()*1.01))
    plt.xticks(rotation=360)
    plt.ylabel('percentage')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.savefig(image_path+'Application_result_percentage_gender.png', bbox_inches='tight')
    plt.close()
    return

if __name__ == "__main__":
    #preparation 
    parent=get_parent_path()
    genderM=Gender_coding(get_code_map())
    removed_csv=parent+"/data/csvs/hmda_2017_ca_noname.csv"
    numerics = ['loan_amount_000s', 'applicant_income_000s', 'population', 'minority_population',
            'hud_median_family_income', 'tract_to_msamd_income', 'number_of_owner_occupied_units',
            'number_of_1_to_4_family_units', 'application_date_indicator', 'rate_spread']
    dtypes={}
    for num in numerics:
        dtypes[num] = 'float64'
    skimmed_df=pd.read_csv(removed_csv, low_memory=False, dtype=dtypes, na_values=' ')
    image_path=parent+'/result/eda/'

    # Generating Plots
    Generate_Gender_Plots(skimmed_df,genderM,parent,image_path)
    print('Finished Generating Gender Anlysis Plots')