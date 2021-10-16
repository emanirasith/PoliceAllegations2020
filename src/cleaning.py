import numpy as np
import pandas as pd

def cleaning(df):
    
    df['complainant_ethnicity'] = df ['complainant_ethnicity'].replace('Unknown', np.NaN)
    df['complainant_gender'] = df['complainant_gender'].replace('Not described', np.NaN)
    df['contact_reason'] = df['contact_reason'].replace('No contact', np.NaN)

    df['complainant_age_incident'] = df['complainant_age_incident'].apply(lambda x: np.NaN if x < 0 else x)
    
    useful_cols = ['complainant_ethnicity',
            'complainant_gender',
            'complainant_age_incident',
            'allegation',
            'contact_reason',
           'outcome_description',
           'board_disposition',
              ]
    
    only_binary = df[(df['complainant_gender'] == 'Male') | (df['complainant_gender'] == 'Female')]
    q_data = only_binary.loc[:, useful_cols]

    q_data['success'] = only_binary['board_disposition'].apply(lambda x: 0 if x in ['Unsubstantiated', 'Exonerated'] else 1)
    
    new_df = q_data.reset_index(drop=True)

    return new_df

