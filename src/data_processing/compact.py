drop_columns = ['respondent_id', 'census_tract_number', 'sequence_number', 'application_date_indicator',  # Identity
                'as_of_year', 'state_abbr', 'state',  # Common Info
                'applicant_ethnicity', 'co_applicant_ethnicity',  # Overlap with race info
                'agency_abbr', 'agency',  # Abandoned features
                'msamd', 'rate_spread', 'hoepa_status',
                'lien_status', 'population',
                'minority_population', 'hud_median_family_income',
                'tract_to_msamd_income', 'number_of_owner_occupied_units',
                'number_of_1_to_4_family_units',  # Overlapping geolocational info
                'edit_status', 'purchaser_type']


def clean_float_str(df, col):
    '''
    Get rid of the ".0" for float-like string columns representing code
    :return: df
    '''
    assert col in df.columns
    assert df[col].dtype == 'string'
    df[col] = df[col].str[:1]


def compact_races(df):
    "compact race values into one string"
    for i in range(1, 6):
        df['applicant_race_' + str(i)].fillna('', inplace=True)
    df['applicant_races'] = df[['applicant_race_1', 'applicant_race_2', 'applicant_race_3',
                                          'applicant_race_4', 'applicant_race_5']].agg(''.join, axis=1)


def select_approve(df, map_path="../src/data_processing/code_map.json"):
    "use values in 'action_taken' to generate approved label"
    approve_actions = ['1', '2', '4', '6', '8']
    # from .code import load_code_map_json
    # code_map = load_code_map_json(map_path)
    # print("Generate approved label using:", " AND ".join([code_map[a] for a in approve_actions]))
    df['approved'] = df['action_taken'].isin(approve_actions)


def build_has_co_applicant(df):
    assert 'co_applicant_sex' in df.columns
    df['has_co_applicant'] = df['co_applicant_sex'] != '5'


if __name__ == "__main__":
    from numeric import read_raw_csv_numeric
    code_data = "../../data/code-only/hmda_2017_ca_all-records_code_only_no_county.csv"

    df = read_raw_csv_numeric(code_data)
    drop_float = ['applicant_race_'+str(i) for i in range(1,6)] + ['co_applicant_race_'+str(i) for i in range(1,6)] + ['msamd']
    for col in drop_float:
        clean_float_str(df, col)

    build_has_co_applicant(df)

    select_approve(df)

    compact_races(df)

    print(df.columns)

    dropped = df.drop(drop_columns, axis=1)

    dropped.to_csv("../../data/cleaned/hmda_2017_ca_all-records_code_only_agg_sex_new.csv", index=False)