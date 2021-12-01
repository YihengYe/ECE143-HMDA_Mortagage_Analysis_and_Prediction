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
    allDir = os.getcwd().split('\\')
    for i in range(len(allDir)):
        if allDir[i] in ['src', 'notebooks']:
            result = os.getcwd()[:-(sum(map(len, allDir[i:])) + 1 * (len(allDir) - i))]
            return result
    return os.getcwd()


def get_code_map():
    """
    get the code map and change all str code to integer

    :return: the code map for all values
    """
    parent_path = get_parent_path()
    js_road = parent_path + "/src/data_processing/code_map.json"
    with open(js_road, 'r') as fh:
        code_map = json.load(fh)
        for i in code_map.keys():
            code_map[i] = {int(m): n for m, n in code_map[i].items()}
    return code_map


def Ethnicity_coding(code_map):
    """
    Shorten the original name for code 4 to "Information not provided by applicant"

    :param code_map: the originial code map
    :return: The updated gender code map
    """
    EthnicityMap = code_map['ethnicity'].copy()
    EthnicityMap[3] = 'Unknown'
    EthnicityMap[4] = 'Unknown'
    return EthnicityMap


def Generate_Ethnicity_Plots(df, genderMap, parent_path, image_path):
    """
    Generate Gender Analysis Plots

    :param df: the skimmed data set
    :param genderMap: the Gender code map
    :param parent_path: root parent path
    :param image_path: the image path
    """
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    Ethnicity_total=skimmed_df['applicant_ethnicity'].replace(EthnicityMap).value_counts()
    # Draw Gender composition for All applicants
    plt.figure()
    Ethnicity_total = Ethnicity_total.rename(index=EthnicityMap)
    Ethnicity_total.plot.pie(legend=False, title='Ethnicity Composition for All Applicants', autopct='%1.1f%%')
    plt.savefig(image_path + 'Total_applicant_ethnicity.png', bbox_inches='tight')
    plt.close()

    # Making analysis on applicant sex vs approval
    Sex_result = df[['applicant_sex', 'action_taken']]
    Ethnicity_result = skimmed_df[['applicant_ethnicity', 'action_taken']]
    RecodeAction = {1: "Institution approved", 2: "Institution approved", 3: 'Institution denied',
                    7: 'Institution denied', 8: 'Institution approved'}
    Ethnicity_result_b = pd.DataFrame()
    Ethnicity_result_b['action'] = Ethnicity_result['action_taken'].replace(RecodeAction)
    Ethnicity_result_b['applicant_ethnicity'] = Ethnicity_result['applicant_ethnicity'].replace(EthnicityMap)
    Ethnicity_result_a1 = Ethnicity_result_b.pivot_table(index='applicant_ethnicity', columns='action', aggfunc='size',
                                                         fill_value=0)
    plt.figure()
    Ethnicity_result_a1.plot.bar(title='Application Result Counts vs Ethnicity')
    plt.ylabel('count')
    plt.xticks(rotation=360)
    plt.savefig(image_path + 'Application_result_count_ethnicity.png', bbox_inches='tight')
    plt.close()

    totalSA1 = Ethnicity_result_a1.sum(axis=1)
    Ethnicity_result_a2 = Ethnicity_result_a1.T
    temp = Ethnicity_result_a2 / totalSA1.values
    Ethnicity_result_a2 = temp.T * 100
    plt.figure()
    SA2B = Ethnicity_result_a2.plot.bar(title='Application Result Precentage vs Ethnicity')
    for p in SA2B.patches:
        SA2B.annotate(str("%.2f" % p.get_height()) + '%', xy=(p.get_x(), p.get_height() * 1.01))
    plt.xticks(rotation=360)
    plt.ylabel('percentage')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.savefig(image_path + 'Application_result_percentage_ethnicity.png', bbox_inches='tight')
    plt.close()

    Ethnicity_result_approve = Ethnicity_result_a1['Institution approved'].replace(EthnicityMap).reindex(
        index=['Hispanic or Latino', 'Not Hispanic or Latino', 'Unknown'])
    Ethnicity_result_approve = Ethnicity_result_approve.rename("")
    plt.figure()
    Ethnicity_result_approve.plot.pie(legend=False, title='Ethnicity Composition for Approved Applicants',
                                      autopct='%1.1f%%')
    plt.savefig(image_path + 'Approved_applicant_Ethnicity.png', bbox_inches='tight')
    plt.close()

    Ethnicity_result_approve = Ethnicity_result_a1['Institution denied'].replace(EthnicityMap).reindex(
        index=['Hispanic or Latino', 'Not Hispanic or Latino', 'Unknown'])
    Ethnicity_result_approve = Ethnicity_result_approve.rename("")
    plt.figure()
    Ethnicity_result_approve.plot.pie(legend=False, title='Ethnicity Composition for Denied Applicants',
                                      autopct='%1.1f%%')
    plt.savefig(image_path + 'Denied_applicant_Ethnicity.png', bbox_inches='tight')
    plt.close()
    return


def Co_vs_Non_co_ethnicity(skimmed_df, genderMap, image_path):
    """
    Analysis for applications with co-applicants vs those without co-applicants

    :param skimmed_df: Downscaled data set
    :param genderMap: code map for gender
    :param image_path: output path for result graphs
    """
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    def pie_helper(value_counter, image_path, out_path, title):
        """
        a helper function for generating pie chart

        :param value_counter: value_counts dataframe
        :param image_path: out put image path
        :param out_path: out put image file name+.png
        :param title: picture title
        """
        df = value_counter.reindex(index=['Hispanic or Latino', 'Not Hispanic or Latino', 'Unknown'])
        df = df.rename("")
        df.plot.pie(legend=False, title=title, autopct='%1.1f%%')
        plt.savefig(image_path + out_path, bbox_inches='tight')
        plt.close()
        return

    def bar_helper(df, image_path, out_path, title, EthnicityMap):
        """
        a helper function for generating percentage bar chart

        :param df: original dataframe
        :param image_path: out put image path
        :param out_path: out put image file name+.png
        :param title: picture title
        :param EthnicityMap: gender code map
        """
        Ethnicity_result = df[['applicant_ethnicity', 'action_taken']]
        RecodeAction = {1: "Institution approved", 2: "Institution approved", 3: 'Institution denied',
                        7: 'Institution denied', 8: 'Institution approved'}
        Ethnicity_result_b = pd.DataFrame()
        Ethnicity_result_b['action'] = Ethnicity_result['action_taken'].replace(RecodeAction)
        Ethnicity_result_b['applicant_ethnicity'] = Ethnicity_result['applicant_ethnicity'].replace(EthnicityMap)
        Ethnicity_result_a1 = Ethnicity_result_b.pivot_table(index='applicant_ethnicity', columns='action',
                                                             aggfunc='size', fill_value=0)
        totalSA1 = Ethnicity_result_a1.sum(axis=1)
        Ethnicity_result_a2 = Ethnicity_result_a1.T
        temp = Ethnicity_result_a2 / totalSA1.values
        Ethnicity_result_a2 = temp.T * 100
        plt.figure()
        SA2B = Ethnicity_result_a2.plot.bar(title=title)
        for p in SA2B.patches:
            SA2B.annotate(str("%.2f" % p.get_height()) + '%', xy=(p.get_x(), p.get_height() * 1.01))
        plt.xticks(rotation=360)
        plt.ylabel('percentage')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.savefig(image_path + out_path, bbox_inches='tight')
        plt.close()
        return

    def pivot_value_helper(df, EthnicityMap):
        """
        get pivot table with gender value counts

        :param df: original data frame
        :return: the pivot table with gender value counts
        """
        Ethnicity_result = df[['applicant_ethnicity', 'action_taken']]
        RecodeAction = {1: "Institution approved", 2: "Institution approved", 3: 'Institution denied',
                        7: 'Institution denied', 8: 'Institution approved'}
        Ethnicity_result_b = pd.DataFrame()
        Ethnicity_result_b['action'] = Ethnicity_result['action_taken'].replace(RecodeAction)
        Ethnicity_result_b['applicant_ethnicity'] = Ethnicity_result['applicant_ethnicity'].replace(EthnicityMap)
        Ethnicity_result_a1 = Ethnicity_result_b.pivot_table(index='applicant_ethnicity', columns='action',
                                                             aggfunc='size', fill_value=0)
        return Ethnicity_result_a1

    # Total
    Coappli = skimmed_df[skimmed_df['co_applicant_ethnicity'] != 5]
    Nonco = skimmed_df[skimmed_df['co_applicant_ethnicity'] == 5]
    plt.figure()
    plt.pie([len(Coappli), len(Nonco)], labels=['With co-applicant', 'Without co-applicant'], autopct='%1.1f%%')
    plt.title('Composition for Applications with/without co-applicant')
    plt.savefig(image_path + 'Composition_for_Applications_with_or_without_co-applicant.png', bbox_inches='tight')
    plt.close()

    Noncopv = pivot_value_helper(Nonco, EthnicityMap)
    Coapplipv = pivot_value_helper(Coappli, EthnicityMap)
    # No co-applicant
    pie_helper(Nonco['applicant_ethnicity'].replace(EthnicityMap).value_counts(), image_path,
               'Ethnicity_composition_for_all_applicants_no_co-applicant.png',
               'Ethnicity Composition for All Applicants with No Co-applicant')
    bar_helper(Nonco, image_path,
               'Application_result_percentage_vs_ethnicity_no_co-applicant.png',
               'Application Result Precentage vs Ethnicity, No co-applicant cases', EthnicityMap)
    pie_helper(
        Noncopv['Institution approved'].reindex(index=['Hispanic or Latino', 'Not Hispanic or Latino', 'Unknown']),
        image_path,
        'Approved_applicants_ethnicity_no_co-applicant.png',
        'Ethnicity Composition for Approved Applicants with No Co-applicant')
    pie_helper(Noncopv['Institution denied'].reindex(index=['Hispanic or Latino', 'Not Hispanic or Latino', 'Unknown']),
               image_path,
               'Denied_applicants_ethnicity_no_co-applicant.png',
               'Ethnicity Composition for Denied Applicants with No Co-applicant')
    # Have co-applicant
    pie_helper(Coappli['applicant_ethnicity'].replace(EthnicityMap).value_counts(), image_path,
               'Ethnicity_composition_for_all_applicants_co-applicant.png',
               'Ethnicity Composition for All Applicants with Co-applicant')
    bar_helper(Coappli, image_path,
               'Application_result_percentage_vs_ethnicity_co-applicant.png',
               'Application Result Precentage vs Ethnicity With co-applicant cases', EthnicityMap)
    pie_helper(
        Coapplipv['Institution approved'].reindex(index=['Hispanic or Latino', 'Not Hispanic or Latino', 'Unknown']),
        image_path,
        'Approved_applicants_Ethnicity_co-applicant.png',
        'Ethnicity Composition for Approved Applicants with Co-applicant')
    pie_helper(
        Coapplipv['Institution denied'].reindex(index=['Hispanic or Latino', 'Not Hispanic or Latino', 'Unknown']),
        image_path,
        'Denied_applicants_Ethnicity_co-applicant.png', 'Ethnicity Composition for Denied Applicants with Co-applicant')
    return


def pair_analysis(skimmed_df, image_path):
    """
    Analysis for Applicant-Co applicant pairs

    :param skimmed_df: original data frame
    :param image_path: image output path
    """
    Coappli = skimmed_df[skimmed_df['co_applicant_ethnicity'] != 5]
    Cover = Coappli.copy()
    Cover['Pair_Ethnicity'] = Cover['applicant_ethnicity'].astype(str) + Cover['co_applicant_ethnicity'].astype(str)
    PairDict = {'11': "Main:Hispanic or Latino,Co:Hispanic or Latino",
                '12': 'Main:Hispanic or Latino,Co:Not Hispanic or Latino', '13': 'Main:Hispanic or Latino,Co:Unknown',
                '14': 'Main:Hispanic or Latino,Co:Unknown',
                '21': "Main:Not Hispanic or Latino,Co:Hispanic or Latino",
                '22': 'Main:Not Hispanic or Latino,Co:Not Hispanic or Latino',
                '23': 'Main:Not Hispanic or Latino,Co:Unknown', '24': 'Main:Not Hispanic or Latino,Co:Unknown',
                '31': "Main:Unknown,Co:Hispanic or Latino", '32': 'Main:Unknown,Co:Hispanic or Latino',
                '33': 'Main:Unknown,Co:Unknown', '34': 'Main:Unknown,Co:Unknown',
                '41': "Main:Unknown,Co:Hispanic or Latino", '42': 'Main:Unknown,Co:Hispanic or Latino',
                '43': 'Main:Unknown,Co:Unknown', '44': 'Main:Unknown,Co:Unknown'}


    Ethnicity_result_pair = Cover[['Pair_Ethnicity', 'action_taken']]
    RecodeAction = {1: "Institution approved", 2: "Institution approved", 3: 'Institution denied',
                    7: 'Institution denied', 8: 'Institution approved'}
    Ethnicity_result_b_pair = pd.DataFrame()
    Ethnicity_result_b_pair['action'] = Ethnicity_result_pair['action_taken'].replace(RecodeAction)
    Ethnicity_result_b_pair['Pair_Ethnicity'] = Ethnicity_result_pair['Pair_Ethnicity'].replace(PairDict)
    Ethnicity_result_a1_pair = Ethnicity_result_b_pair.pivot_table(index='Pair_Ethnicity', columns='action',
                                                                   aggfunc='size', fill_value=0)
    plt.figure()
    Ethnicity_result_a1_pair.plot.bar(title='Application Result Counts vs Pair_Ethnicity')
    plt.ylabel('count')
    plt.xticks(rotation=45, ha='right')
    plt.savefig(image_path + 'Application_result_count_Pair_Ethnicity.png', bbox_inches='tight')
    plt.close()

    totalSA1_pair = Ethnicity_result_a1_pair.sum(axis=1)
    Ethnicity_result_a2_pair = Ethnicity_result_a1_pair.T
    temp = Ethnicity_result_a2_pair / totalSA1_pair.values
    Ethnicity_result_a2_pair = temp.T * 100
    plt.figure()
    SA2B_pair = Ethnicity_result_a2_pair.plot.bar(title='Application Result Precentage vs Ethnicity Pairs')
    for p in SA2B_pair.patches:
        SA2B_pair.annotate(str("%.2f" % p.get_height()) + '%', xy=(p.get_x(), p.get_height() * 1.01))
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('percentage')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.savefig(image_path + 'Application_result_percentage_Ethnicity_pair.png', bbox_inches='tight')
    plt.close()
    return


if __name__ == "__main__":
    # preparation
    parent = get_parent_path()
    EthnicityMap = Ethnicity_coding(get_code_map())
    removed_csv = parent + "/data/csvs/hmda_2017_ca_noname.csv"
    numerics = ['loan_amount_000s', 'applicant_income_000s', 'population', 'minority_population',
                'hud_median_family_income', 'tract_to_msamd_income', 'number_of_owner_occupied_units',
                'number_of_1_to_4_family_units', 'application_date_indicator', 'rate_spread']
    dtypes = {}
    for num in numerics:
        dtypes[num] = 'float64'
    skimmed_df = pd.read_csv(removed_csv, low_memory=False, dtype=dtypes, na_values=' ')
    image_path = parent + '/result/eda/'

    # Generating Analysis Plots
    Generate_Ethnicity_Plots(skimmed_df, EthnicityMap, parent, image_path)
    print('Finished Generating Ethnicity Analysis Plots For All applicant')
    Co_vs_Non_co_ethnicity(skimmed_df, EthnicityMap, image_path)
    print('Finished Generating Ethnicity Analysis plots For co-applicant condition analysis')
    pair_analysis(skimmed_df, image_path)
    print('Finished Generating Ethnicity Analysis plots For Applicant Pairs analysis')