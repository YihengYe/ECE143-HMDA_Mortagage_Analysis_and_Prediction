import pandas as pd


def load_code_map(code_map_path):
    '''
    code map uses dictionary instead of JSON for using integer value as key
    :param: code_map_path, path to the code_map dictionary
    :return: dictionary, code map for different columns
    '''
    with open(code_map_path, 'r') as f:
        code_map = eval(f.readline())
    return code_map


def remove_names(df, take_county):
    '''
    drop name columns
    :return: dictionary, code map for different columns
    '''
    return df.drop(columns=[x for x in df.columns if "name" in x and not (take_county and x == "county_name")])


def generate_code_dataset(raw_df, path="", take_county=True):
    '''
    Generate dataset with only enum codes, remove all name columns
    :param raw_df: pd.DataFrame, big raw dataset
    :param path: path to save the code-only dataset
    :param take_county: boolean, if we drop the name of counties
    :return: pd.DataFrame, generated code-only dataset
    '''
    code_only = remove_names(raw_df, take_county)
    if len(path) > 0:
        code_only.to_csv(path, index=False)
    return code_only


def validate_code_map(raw_df, code_map_path):
    '''
    Check if a enumeration column have the same value with its code column
    :param raw_df: pd.DataFrame, big raw dataset
    :param code_map_path: path to dictionary
    '''
    code_map = load_code_map(code_map_path)
    for cat, maps in code_map.items():
        feat, name = cat, cat + "_name"
        if feat in ['race', 'ethnicity', 'sex']:
            # Applicant info, not check co-applicant
            feat = "applicant_" + feat
            name = "applicant_" + name
        code = feat
        if code == 'agency':
            code += "_code"
        if name not in raw_df.columns:
            # Applicant info with multiple columns, check the first one
            code += "_1"
            name += "_1"
        print(code, name)
        code_counts = raw_df[code].value_counts()
        name_counts = raw_df[name].value_counts()
        for enum in code_counts.index:
            enum_name = maps[enum]
            if feat + "_abbr" in raw_df.columns:
                # For agency (with _abbr), I currently include both abbr. & name in code_map, using ": " as separator
                enum_name = enum_name.split(': ')[-1]
            if code_counts[enum] != name_counts[enum_name]:
                print("Inconsistency in {0}: code:{1}, enum:{2}".format(feat, enum, code_counts[enum]))


if __name__ == "__main__":
    import os
    code_map_path = "./code_map_dict"
    raw_path = "../../data/raw/hmda_2017_ca_all-records_labels.csv"
    code_only_path = "../../data/code-only/hmda_2017_ca_all-records_code_only.csv"

    if not os.path.exists(os.path.dirname(code_only_path)):
        os.mkdir(os.path.dirname(code_only_path))

    # Have to set low_memory as False to read raw data_processing
    raw_df = pd.read_csv(raw_path, low_memory=False)
    validate_code_map(raw_df, code_map_path)
    _ = generate_code_dataset(raw_df, code_only_path)

