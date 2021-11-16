import json

import pandas as pd


def align_code_name(raw_df, code_column, name_column):
    '''
    align code_column with name_column
    :return: dictionary, mapping code_column value to name_column, return empty one if can't map together
    '''
    assert isinstance(raw_df, pd.DataFrame)
    assert code_column in raw_df.columns and name_column in raw_df.columns
    code_cnt = raw_df[code_column].value_counts().sort_values()
    name_cnt = raw_df[name_column].value_counts().sort_values()
    print(code_cnt)
    print(name_cnt)

    if len(code_cnt) != len(name_cnt):
        return {}
    res = {}
    for code, name in zip(code_cnt.index, name_cnt.index):
        if code_cnt[code] != name_cnt[name]:
            return {}
        res[code] = name
    return res


def load_code_map_dict(code_map_path):
    '''
    code map uses dictionary instead of JSON for using integer value as key
    :param: code_map_path, path to the code_map dictionary
    :return: dictionary, code map for different columns
    '''
    with open(code_map_path, 'r') as f:
        code_map = eval(f.readline())
    return code_map


def load_code_map_json(code_map_path):
    '''
    code map uses JSON
    :param: code_map_path, path to the code_map JSON
    :return: dictionary, code map for different columns
    '''
    import json
    with open(code_map_path, 'r') as f:
        code_map = json.load(f)
    return code_map


def remove_names(df):
    '''
    drop name columns
    :return: dictionary, code map for different columns
    '''
    return df.drop(columns=[x for x in df.columns if "name" in x])


def generate_code_dataset(raw_df, path="", cover=False):
    '''
    Generate dataset with only enum codes, remove all name columns
    :param raw_df: pd.DataFrame, big raw dataset
    :param path: path to save the code-only dataset, if not exists
    :param cover: whether to cover the current file, default to False
    :return: pd.DataFrame, generated code-only dataset
    '''
    import os
    code_only = remove_names(raw_df)

    # Tidy the column names
    code_rename = dict(zip([x for x in code_only.columns if "code" in x], [x.split('_')[0] for x in code_only.columns if "code" in x]))
    print(code_rename)
    code_only.rename(columns=code_rename, inplace=True)
    print(code_only.columns)

    if len(path) > 0:
        if cover or not os.path.exists(path):
            code_only.to_csv(path, index=False)
    return code_only


def validate_code_map(raw_df, code_map):
    '''
    Check if a enumeration column have the same value with its code column
    :param raw_df: pd.DataFrame, big raw dataset
    :param code_map: code map in dictionary
    '''
    for cat, maps in code_map.items():
        feat, name = cat, cat + "_name"
        if feat in ['race', 'ethnicity', 'sex']:
            # Applicant info, not check co-applicant
            feat = "applicant_" + feat
            name = "applicant_" + name
        code = feat
        if code in ['agency', 'county']:
            code += "_code"
        if name not in raw_df.columns:
            # Applicant info with multiple columns, check the first one
            code += "_1"
            name += "_1"
        # print(code, name)
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
    from numeric import read_raw_csv_numeric
    raw_path = "../../data/raw/hmda_2017_ca_all-records_labels.csv"

    # REMINDER: to use vanilla read_csv for dictionary-like map, because then the keys would be integers/floats
    raw_df = read_raw_csv_numeric(raw_path, with_dtype=True)
    code_only_path = "../../data/code-only/hmda_2017_ca_all-records_code_only_no_county_dtype.csv"

    # code_only = read_raw_csv_numeric(code_only_path)
    # print(code_only.columns)
    # print(code_only.dtypes)

    # county = align_code_name(raw_df, 'county_code', 'county_name')
    code_map_path = "./code_map_dict"
    code_map_dict = load_code_map_dict(code_map_path)
    # code_map_dict['county'] = county
    # with open(code_map_path, 'w') as f:
    #     f.write(str(code_map_dict))

    code_json_path = "./code_map.json"
    code_map_json = load_code_map_json(code_json_path)
    # code_map_json['county'] = county
    # with open(code_json_path, 'w') as f:
    #     json.dump(code_map_json, f)

    if not os.path.exists(os.path.dirname(code_only_path)):
        os.mkdir(os.path.dirname(code_only_path))

    # Have to set low_memory as False to read raw data_processing
    validate_code_map(raw_df, code_map_json)
    _ = generate_code_dataset(raw_df, code_only_path, cover=True)

