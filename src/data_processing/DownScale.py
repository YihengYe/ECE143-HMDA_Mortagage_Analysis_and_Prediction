import pandas as pd
import os


"""
The library for downscale the original data set
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

def DownScale(data_path, parent_path):
    """
    down scale your data set into a dataset contains only coded column

    :param data_path: the path to read the original data set (exclude the parent path)
    :param parent_path: the root directory for this project
    """
    record=parent_path+"/"+data_path
    df=pd.read_csv(record, low_memory=False)
    simpDF=df[df['action_taken'].isin([1,3,7,2,8])]
    removedDF=simpDF.drop(columns=[x for x in df.columns if "name" in x])
    removedDF.to_csv(parent_path+"/data/csvs/hmda_2017_ca_noname.csv", index=False)
    print('Save the updated data set with coded only and decisions of approve/denial to', "/data/csvs/hmda_2017_ca_noname.csv")

if __name__ == "__main__":
    data_path='data/raw/hmda_2017_ca_all-records_labels.csv'
    parent=get_parent_path()
    DownScale(data_path, parent)