raw_columns = ['as_of_year', 'respondent_id', 'agency_name', 'agency_abbr', 'agency',
               'agency_code', 'loan_type_name', 'loan_type', 'property_type_name',
               'property_type', 'loan_purpose_name', 'loan_purpose',
               'owner_occupancy_name', 'owner_occupancy', 'loan_amount_000s',
               'preapproval_name', 'preapproval', 'action_taken_name', 'action_taken',
               'msamd_name', 'msamd', 'state_name', 'state_abbr', 'state_code', 'state',
               'county_name', 'county_code', 'county', 'census_tract_number',
               'applicant_ethnicity_name', 'applicant_ethnicity',
               'co_applicant_ethnicity_name', 'co_applicant_ethnicity',
               'applicant_race_name_1', 'applicant_race_1', 'applicant_race_name_2',
               'applicant_race_2', 'applicant_race_name_3', 'applicant_race_3',
               'applicant_race_name_4', 'applicant_race_4', 'applicant_race_name_5',
               'applicant_race_5', 'co_applicant_race_name_1', 'co_applicant_race_1',
               'co_applicant_race_name_2', 'co_applicant_race_2',
               'co_applicant_race_name_3', 'co_applicant_race_3',
               'co_applicant_race_name_4', 'co_applicant_race_4',
               'co_applicant_race_name_5', 'co_applicant_race_5', 'applicant_sex_name',
               'applicant_sex', 'co_applicant_sex_name', 'co_applicant_sex',
               'applicant_income_000s', 'purchaser_type_name', 'purchaser_type',
               'denial_reason_name_1', 'denial_reason_1', 'denial_reason_name_2',
               'denial_reason_2', 'denial_reason_name_3', 'denial_reason_3',
               'rate_spread', 'hoepa_status_name', 'hoepa_status', 'lien_status_name',
               'lien_status', 'edit_status_name', 'edit_status', 'sequence_number',
               'population', 'minority_population', 'hud_median_family_income',
               'tract_to_msamd_income', 'number_of_owner_occupied_units',
               'number_of_1_to_4_family_units', 'application_date_indicator']


'''
numerics are the manually selected columns who are actual numerical values, instead of code/enumerate values
these columns will be applied with 'to_numeric' and converted to float64
'''
numerics = ['loan_amount_000s', 'applicant_income_000s', 'population', 'minority_population',
            'hud_median_family_income', 'tract_to_msamd_income', 'number_of_owner_occupied_units',
            'number_of_1_to_4_family_units', 'application_date_indicator', 'rate_spread']


def read_raw_csv_numeric(raw_path, with_dtype=True):
    '''
    read raw csv files with numeric lines, and rest as string
    :param with_dtype, whether we use the dtype for read_csv
    :return: pd.DataFrame, the converted csv
    '''
    import pandas as pd
    if not with_dtype:
        return pd.read_csv(raw_path, low_memory=False, na_values=' ')
    dtypes = dict(zip(raw_columns, ['string'] * len(raw_columns)))
    for num in numerics:
        dtypes[num] = 'float64'
    # Here we have to specify the na_values, otherwise it won't transmit to numerical dtypes
    df = pd.read_csv(raw_path, low_memory=False, na_values=' ', dtype=dtypes)
    return df
