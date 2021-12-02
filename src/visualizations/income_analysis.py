import pandas as pd
import os
from pathlib import Path
import matplotlib.pyplot as plt
import json
import numpy as np
import matplotlib as mpl
mpl.rcParams['agg.path.chunksize'] = 10000

"""
Generating visualization for Income in the data set
"""

def get_parent_path():
    """
    get root parent path for this file

    :return: the root parent path
    """
    if '/' in os.getcwd():
        allDir=os.getcwd().split('/')
    else:
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

def divi(x):
    if x >=500:
        return 500000
    elif x==x:
        flor = x//30
        return flor*30000
    else:
        return -1

def Generate_Income_Plots(income, parent_path, image_path):
    """
    Generate Income Analysis Plots

    :param df: the skimmed data set
    :param parent_path: root parent path
    :param image_path: the image path
    """
    accp = income.loc[(income['action_taken'] == 1) | (income['action_taken'] == 2) | (income['action_taken'] == 8)]
    deny = income.loc[(income['action_taken'] == 3) | (income['action_taken'] == 7)]
    
    plt.figure()
    accp['applicant_income_000s'].apply(divi).value_counts().sort_index().plot.bar(title='Institution_approved_income_dist')
    plt.savefig(image_path+'Institution_approved_income_dist.png',bbox_inches='tight')
    plt.show()
    plt.close()

    plt.figure()
    deny['applicant_income_000s'].apply(divi).value_counts().sort_index().plot.bar(title='Institution_denied_income_dist')
    plt.savefig(image_path+'Institution_denied_income_dist.png',bbox_inches='tight')
    plt.show()
    plt.close()


    RecodeAction={1:"Institution approved",2:"Institution approved", 3:'Institution denied', 7:'Institution denied',8:'Institution approved'}
    income_b=income
    income_b['action']= income['action_taken'].replace(RecodeAction)


    income_b['income_group'] = income_b['applicant_income_000s'].apply(divi)
    #print(income_b)
    income_a1=income_b.pivot_table(index='income_group', columns='action',aggfunc='size',fill_value=0)
    plt.figure()
    income_a1.plot.bar(title='Application Result Counts vs Income')
    plt.ylabel('count')
    plt.savefig(image_path+'Application Result Counts vs Income.png',bbox_inches='tight')
    plt.show()
    plt.close()


if __name__ == "__main__":
    parent=get_parent_path()

    data = pd.read_csv(parent+"/data/csvs/hmda_2017_ca_noname.csv")
    income = data[['applicant_income_000s','action_taken']]
    image_path=parent+'/result/eda/income_analysis/'

    if not os.path.exists(image_path):
        os.makedirs(image_path)

    Generate_Income_Plots(income, parent, image_path)
