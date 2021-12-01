import pandas as pd
import os
import matplotlib.pyplot as plt
import json

"""
Generating visualization for Race in the data set
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


def Race_coding(code_map):
    """
    Shorten the original name for code 4 to "Information not provided by applicant"

    :param code_map: the originial code map
    :return: The updated Race code map
    """
    RaceMap = code_map['race'].copy()
    RaceMap[6] = 'Unknown'
    RaceMap[7] = 'Unknown'
    return RaceMap


def Generate_Race_Plots(df, genderMap, parent_path, image_path):
    """
    Generate Race Analysis Plots

    :param df: the skimmed data set
    :param genderMap: the Race code map
    :param parent_path: root parent path
    :param image_path: the image path
    """
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    Race_total = skimmed_df['applicant_race_1'].replace(RaceMap).value_counts()
    plt.figure(figsize=(8, 8))
    Race_total = Race_total.rename(index=RaceMap)
    Race_total.plot.pie(legend=False, title='Race Composition for All Applicants', autopct='%1.1f%%')
    plt.savefig(image_path + 'Total_applicant_race.png', bbox_inches='tight')
    plt.close()

    # Making analysis on applicant sex vs approval
    Race_result = skimmed_df[['applicant_race_1', 'action_taken']]
    RecodeAction = {1: "Institution approved", 2: "Institution approved", 3: 'Institution denied',
                    7: 'Institution denied', 8: 'Institution approved'}
    Race_result_b = pd.DataFrame()
    Race_result_b['action'] = Race_result['action_taken'].replace(RecodeAction)
    Race_result_b['applicant_race_1'] = Race_result['applicant_race_1'].replace(RaceMap)
    Race_result_a1 = Race_result_b.pivot_table(index='applicant_race_1', columns='action', aggfunc='size', fill_value=0)
    plt.figure(figsize=(20, 20))
    Race_result_a1.plot.bar(title='Application Result Counts vs Race')
    plt.ylabel('count')
    plt.xticks(rotation=90)
    plt.savefig(image_path + 'Application_result_count_race.png', bbox_inches='tight')
    plt.close()

    totalSA1 = Race_result_a1.sum(axis=1)
    Race_result_a2 = Race_result_a1.T
    temp = Race_result_a2 / totalSA1.values
    Race_result_a2 = temp.T * 100
    plt.figure(figsize=(10, 10))
    SA2B = Race_result_a2.plot.bar(title='Application Result Precentage vs Race')
    for p in SA2B.patches:
        SA2B.annotate(str("%.2f" % p.get_height()) + '%', xy=(p.get_x(), p.get_height() * 1.01))
    plt.xticks(rotation=90)
    plt.ylabel('percentage')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.savefig(image_path + 'Application_result_percentage_race.png', bbox_inches='tight')
    plt.close()

    l1 = list(RaceMap.values())
    Race_l = sorted(set(l1), key=l1.index)
    Race_l = Race_l[0:6]

    Race_result_approve = Race_result_a1['Institution approved'].replace(RaceMap).reindex(index=Race_l)
    plt.figure(figsize=(10, 10))
    Race_result_approve.plot.pie(legend=False, title='Race Composition for Approved Applicants', autopct='%1.1f%%')
    plt.savefig(image_path + 'Approved_applicant_race.png', bbox_inches='tight')
    plt.close()

    Race_result_approve = Race_result_a1['Institution denied'].replace(RaceMap).reindex(index=Race_l)
    plt.figure(figsize=(10, 10))
    Race_result_approve.plot.pie(legend=False, title='Race Composition for denied Applicants', autopct='%1.1f%%')
    plt.savefig(image_path + 'Denied_applicant_race.png', bbox_inches='tight')
    plt.close()
    return


def Co_vs_Non_co_race(skimmed_df, RaceMap, image_path):
    """
    Analysis for applications with co-applicants vs those without co-applicants

    :param skimmed_df: Downscaled data set
    :param genderMap: code map for Race
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
        df = value_counter.reindex(index=Race_l)
        plt.figure(figsize=(10, 10))
        df.plot.pie(legend=False, title=title, autopct='%1.1f%%')
        plt.savefig(image_path + out_path, bbox_inches='tight')
        plt.close()
        return

    def bar_helper(df, image_path, out_path, title, RaceM):
        """
        a helper function for generating percentage bar chart

        :param df: original dataframe
        :param image_path: out put image path
        :param out_path: out put image file name+.png
        :param title: picture title
        :param RaceM: gender code map
        """
        Race_result = df[['applicant_race_1', 'action_taken']]
        RecodeAction = {1: "Institution approved", 2: "Institution approved", 3: 'Institution denied',
                        7: 'Institution denied', 8: 'Institution approved'}
        Race_result_b = pd.DataFrame()
        Race_result_b['action'] = Race_result['action_taken'].replace(RecodeAction)
        Race_result_b['applicant_race_1'] = Race_result['applicant_race_1'].replace(RaceM)
        Race_result_a1 = Race_result_b.pivot_table(index='applicant_race_1', columns='action', aggfunc='size',
                                                   fill_value=0)
        totalSA1 = Race_result_a1.sum(axis=1)
        Race_result_a2 = Race_result_a1.T
        temp = Race_result_a2 / totalSA1.values
        Race_result_a2 = temp.T * 100
        plt.figure()
        SA2B = Race_result_a2.plot.bar(title=title)
        for p in SA2B.patches:
            SA2B.annotate(str("%.2f" % p.get_height()) + '%', xy=(p.get_x(), p.get_height() * 1.01))
        plt.xticks(rotation=90)
        plt.ylabel('percentage')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.savefig(image_path + out_path, bbox_inches='tight')
        plt.close()
        return

    def pivot_value_helper(df, RaceM):
        """
        get pivot table with gender value counts

        :param df: original data frame
        :return: the pivot table with race value counts
        """
        Race_result = df[['applicant_race_1', 'action_taken']]
        RecodeAction = {1: "Institution approved", 2: "Institution approved", 3: 'Institution denied',
                        7: 'Institution denied', 8: 'Institution approved'}
        Race_result_b = pd.DataFrame()
        Race_result_b['action'] = Race_result['action_taken'].replace(RecodeAction)
        Race_result_b['applicant_race_1'] = Race_result['applicant_race_1'].replace(RaceM)
        Race_result_a1 = Race_result_b.pivot_table(index='applicant_race_1', columns='action', aggfunc='size',
                                                   fill_value=0)
        return Race_result_a1

    l1 = list(RaceMap.values())
    Race_l = sorted(set(l1), key=l1.index)
    Race_l = Race_l[0:6]
    # Total
    Coappli = skimmed_df[skimmed_df['co_applicant_race_1'] != 8]
    Nonco = skimmed_df[skimmed_df['co_applicant_race_1'] == 8]

    plt.figure()
    plt.pie([len(Coappli), len(Nonco)], labels=['With co-applicant', 'Without co-applicant'], autopct='%1.1f%%')
    plt.title('Composition for Applications with/without co-applicant')
    plt.savefig(image_path + 'Composition_for_Applications_with_or_without_co-applicant.png', bbox_inches='tight')
    plt.close()

    Noncopv = pivot_value_helper(Nonco, RaceMap)
    Coapplipv = pivot_value_helper(Coappli, RaceMap)
    # No co-applicant
    pie_helper(Nonco['applicant_race_1'].replace(RaceMap).value_counts(), image_path,
               'Race_composition_for_all_applicants_no_co-applicant.png',
               'Race Composition for All Applicants with No Co-applicant')
    bar_helper(Nonco, image_path,
               'Application_result_percentage_vs_race_no_co-applicant.png',
               'Application Result Precentage vs Race, No co-applicant cases', RaceMap)
    pie_helper(Noncopv['Institution approved'].reindex(index=Race_l), image_path,
               'Approved_applicants_race_no_co-applicant.png',
               'Race Composition for Approved Applicants with No Co-applicant')
    pie_helper(Noncopv['Institution denied'].reindex(index=Race_l), image_path,
               'Denied_applicants_race_no_co-applicant.png',
               'Race Composition for Denied Applicants with No Co-applicant')
    # Have co-applicant
    pie_helper(Coappli['applicant_race_1'].replace(RaceMap).value_counts(), image_path,
               'Race_composition_for_all_applicants_co-applicant.png',
               'Race Composition for All Applicants with Co-applicant')
    bar_helper(Coappli, image_path,
               'Application_result_percentage_vs_race_co-applicant.png',
               'Application Result Precentage vs Race with co-applicant cases', RaceMap)
    pie_helper(Coapplipv['Institution approved'].reindex(index=Race_l), image_path,
               'Approved_applicants_race_co-applicant.png',
               'Race Composition for Approved Applicants with Co-applicant')
    pie_helper(Coapplipv['Institution denied'].reindex(index=Race_l), image_path,
               'Denied_applicants_race_co-applicant.png', 'Race Composition for Denied Applicants with Co-applicant')
    return


if __name__ == "__main__":
    # preparation
    parent = get_parent_path()
    RaceMap = Race_coding(get_code_map())
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
    Generate_Race_Plots(skimmed_df, RaceMap, parent, image_path)
    print('Finished Generating Race Analysis Plots For All applicant')
    Co_vs_Non_co_race(skimmed_df, RaceMap, image_path)
    print('Finished Generating Race Analysis plots For co-applicant condition analysis')
    # pair_analysis(skimmed_df, image_path)
    # print('Finished Generating Race Analysis plots For Applicant Pairs analysis')