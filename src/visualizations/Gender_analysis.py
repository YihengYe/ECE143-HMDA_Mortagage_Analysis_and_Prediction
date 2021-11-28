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
    plt.figure() #plot percentage
    SA2B=Sex_result_a2.plot.bar(title='Application Result Precentage vs Gender')
    for p in SA2B.patches:
        SA2B.annotate(str("%.2f"%p.get_height())+'%', xy=(p.get_x(), p.get_height()*1.01))
    plt.xticks(rotation=360)
    plt.ylabel('percentage')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.savefig(image_path+'Application_result_percentage_gender.png', bbox_inches='tight')
    plt.close()

    Sex_result_approve=Sex_result_a1['Institution approved'].reindex(index=['Male','Female','Unknown'])
    plt.figure() # plot pie chart for approved applicants
    Sex_result_approve.plot.pie(legend=False, title='Gender Composition for Approved Applicants',autopct='%1.1f%%')
    plt.savefig(image_path+'Approved_applicant_gender.png', bbox_inches='tight')
    plt.close()

    Sex_result_denied=Sex_result_a1['Institution denied'].reindex(index=['Male','Female','Unknown'])
    plt.figure() #plot pie chart for deniend applicants
    Sex_result_denied.plot.pie(legend=False, title='Gender Composition for Denied Applicants',autopct='%1.1f%%')
    plt.savefig(image_path+'Denied_applicant_gender.png', bbox_inches='tight')
    plt.close()
    return

def Co_vs_Non_co_gender(skimmed_df,genderMap,image_path):
    """
    Analysis for applications with co-applicants vs those without co-applicants

    :param skimmed_df: Downscaled data set
    :param genderMap: code map for gender
    :param image_path: output path for result graphs
    """
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    def pie_helper(value_counter,image_path,out_path,title):
        """
        a helper function for generating pie chart

        :param value_counter: value_counts dataframe
        :param image_path: out put image path
        :param out_path: out put image file name+.png
        :param title: picture title
        """
        df=value_counter.reindex(index=['Male','Female','Unknown'])
        plt.figure()
        df.plot.pie(legend=False, title=title,autopct='%1.1f%%')
        plt.savefig(image_path+out_path, bbox_inches='tight')
        plt.close()
        return
    
    def bar_helper(df,image_path,out_path,title,genderM):
        """
        a helper function for generating percentage bar chart

        :param df: original dataframe
        :param image_path: out put image path
        :param out_path: out put image file name+.png
        :param title: picture title
        :param genderM: gender code map
        """
        Sex_result=df[['applicant_sex','action_taken']]
        RecodeAction={1:"Institution approved",2:"Institution approved", 3:'Institution denied', 7:'Institution denied',8:'Institution approved'}
        Sex_result_b=pd.DataFrame()
        Sex_result_b['action']= Sex_result['action_taken'].replace(RecodeAction)
        Sex_result_b['applicant_sex']=Sex_result['applicant_sex'].replace(genderM)
        Sex_result_a1=Sex_result_b.pivot_table(index='applicant_sex', columns='action',aggfunc='size',fill_value=0)
        totalSA1=Sex_result_a1.sum(axis=1)
        Sex_result_a2=Sex_result_a1.T
        temp=Sex_result_a2/totalSA1.values
        Sex_result_a2=temp.T*100
        plt.figure()
        SA2B=Sex_result_a2.plot.bar(title=title)
        for p in SA2B.patches:
            SA2B.annotate(str("%.2f"%p.get_height())+'%', xy=(p.get_x(), p.get_height()*1.01))
        plt.xticks(rotation=360)
        plt.ylabel('percentage')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.savefig(image_path+out_path, bbox_inches='tight')
        plt.close()
        return

    def pivot_value_helper(df,genderM):
        """
        get pivot table with gender value counts

        :param df: original data frame
        :param genderM: gender code map
        :return: the pivot table with gender value counts
        """
        Sex_result=df[['applicant_sex','action_taken']]
        RecodeAction={1:"Institution approved",2:"Institution approved", 3:'Institution denied', 7:'Institution denied',8:'Institution approved'}
        Sex_result_b=pd.DataFrame()
        Sex_result_b['action']= Sex_result['action_taken'].replace(RecodeAction)
        Sex_result_b['applicant_sex']=Sex_result['applicant_sex'].replace(genderM)
        Sex_result_a1=Sex_result_b.pivot_table(index='applicant_sex', columns='action',aggfunc='size',fill_value=0)
        return Sex_result_a1
    #Total
    Coappli=skimmed_df[skimmed_df['co_applicant_sex']!=5]
    Nonco=skimmed_df[skimmed_df['co_applicant_sex']==5]
    plt.figure()
    plt.pie([len(Coappli),len(Nonco)],labels=['With co-applicant', 'Without co-applicant'],autopct='%1.1f%%')
    plt.title('Composition for Applications with/without co-applicant')
    plt.savefig(image_path+'Composition_for_Applications_with_or_without_co-applicant.png',bbox_inches='tight')
    plt.close()

    
    Noncopv=pivot_value_helper(Nonco,genderMap)
    Coapplipv=pivot_value_helper(Coappli,genderMap)
    # No co-applicant
    pie_helper(Nonco['applicant_sex'].replace(genderMap).value_counts(),image_path,
           'Gender_composition_for_all_applicants_no_co-applicant.png','Gender Composition for All Applicants with No Co-applicant')
    bar_helper(Nonco,image_path,
           'Application_result_percentage_vs_gender_no_co-applicant.png',
           'Application Result Precentage vs Gender, No co-applicant cases' , genderMap)
    pie_helper(Noncopv['Institution approved'].reindex(index=['Male','Female','Unknown']),image_path,
           'Approved_applicants_gender_no_co-applicant.png','Gender Composition for Approved Applicants with No Co-applicant')
    pie_helper(Noncopv['Institution denied'].reindex(index=['Male','Female','Unknown']),image_path,
           'Denied_applicants_gender_no_co-applicant.png','Gender Composition for Denied Applicants with No Co-applicant')
    # Have co-applicant
    pie_helper(Coappli['applicant_sex'].replace(genderMap).value_counts(),image_path,
           'Gender_composition_for_all_applicants_co-applicant.png','Gender Composition for All Applicants with Co-applicant')
    bar_helper(Coappli,image_path,
           'Application_result_percentage_vs_gender_co-applicant.png',
           'Application Result Precentage vs Gender,With co-applicant cases' , genderMap)
    pie_helper(Coapplipv['Institution approved'].reindex(index=['Male','Female','Unknown']),image_path,
           'Approved_applicants_gender_co-applicant.png','Gender Composition for Approved Applicants with Co-applicant')
    pie_helper(Coapplipv['Institution denied'].reindex(index=['Male','Female','Unknown']),image_path,
           'Denied_applicants_gender_co-applicant.png','Gender Composition for Denied Applicants with Co-applicant')
    return

def pair_analysis(skimmed_df,image_path):
    """
    Analysis for Applicant-Co applicant pairs

    :param skimmed_df: original data frame
    :param image_path: image output path
    """
    Coappli=skimmed_df[skimmed_df['co_applicant_sex']!=5]
    Cover=Coappli.copy()
    Cover['Pair_Gender']=Cover['applicant_sex'].astype(str)+Cover['co_applicant_sex'].astype(str)
    PairDict={'11':"Main:Male,Co:Male",'12':'Main:Male,Co:Female','13':'Main:Male,Co:Unknown','14':'Main:Male,Co:Unknown',
         '21':"Main:Female,Co:Male",'22':'Main:Female,Co:Female','23':'Main:Female,Co:Unknown','24':'Main:Female,Co:Unknown',
         '31':"Main:Unknown,Co:Male",'32':'Main:Unknown,Co:Female','33':'Main:Unknown,Co:Unknown','34':'Main:Unknown,Co:Unknown',
         '41':"Main:Unknown,Co:Male",'42':'Main:Unknown,Co:Female','43':'Main:Unknown,Co:Unknown','44':'Main:Unknown,Co:Unknown'}
    Sex_result_pair=Cover[['Pair_Gender','action_taken']]
    RecodeAction={1:"Institution approved",2:"Institution approved", 3:'Institution denied', 7:'Institution denied',8:'Institution approved'}
    Sex_result_b_pair=pd.DataFrame()
    Sex_result_b_pair['action']= Sex_result_pair['action_taken'].replace(RecodeAction)
    Sex_result_b_pair['Pair_Gender']=Sex_result_pair['Pair_Gender'].replace(PairDict)
    Sex_result_a1_pair=Sex_result_b_pair.pivot_table(index='Pair_Gender', columns='action',aggfunc='size',fill_value=0)
    plt.figure() #draw total bar chart
    Sex_result_a1_pair.plot.bar(title='Application Result Counts vs Gender Pairs')
    plt.ylabel('count')
    plt.xticks(rotation=45,ha='right')
    plt.savefig(image_path+'Application_result_count_gender_pair.png', bbox_inches='tight')
    plt.close()

    totalSA1_pair=Sex_result_a1_pair.sum(axis=1)
    Sex_result_a2_pair=Sex_result_a1_pair.T
    temp=Sex_result_a2_pair/totalSA1_pair.values
    Sex_result_a2_pair=temp.T*100
    plt.figure() #draw application result percentage chart
    SA2B_pair=Sex_result_a2_pair.plot.bar(title='Application Result Precentage vs Gender Pairs')
    for p in SA2B_pair.patches:
        SA2B_pair.annotate(str("%.2f"%p.get_height())+'%', xy=(p.get_x(), p.get_height()*1.01))
    plt.xticks(rotation=45,ha='right')
    plt.ylabel('percentage')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.savefig(image_path+'Application_result_percentage_gender_pair.png', bbox_inches='tight')
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

    # Generating Analysis Plots
    Generate_Gender_Plots(skimmed_df,genderM,parent,image_path)
    print('Finished Generating Gender Analysis Plots For All applicant')
    Co_vs_Non_co_gender(skimmed_df,genderM,image_path)
    print('Finished Generating Gender Analysis plots For co-applicant condition analysis')
    pair_analysis(skimmed_df,image_path)
    print('Finished Generating Gender Analysis plots For Applicant Pairs analysis')