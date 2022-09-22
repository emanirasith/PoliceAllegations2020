import numpy as np
import pandas as pd

def cleaning(df):
    
    #replaces "unknown" in complainant_ethnicity with NaN and replaces "not described" in complainant_gender with NaN and replaces 'No contact" in contact_reason
    df['complainant_ethnicity'] = df ['complainant_ethnicity'].replace('Unknown', np.NaN)
    df['complainant_gender'] = df['complainant_gender'].replace('Not described', np.NaN)
    df['contact_reason'] = df['contact_reason'].replace('No contact', np.NaN)

    #if anyone is under the age of 0 then the row is removed
    df['complainant_age_incident'] = df['complainant_age_incident'].apply(lambda x: np.NaN if x < 0 else x)
    
    #relevant columns to our question
    useful_cols = ['complainant_ethnicity',
            'complainant_gender',
            'complainant_age_incident',
            'allegation',
            'contact_reason',
           'outcome_description',
           'board_disposition',
              ]
    
    #acquires allegations that are only by a "Male" or "Female"
    only_binary = df[(df['complainant_gender'] == 'Male') | (df['complainant_gender'] == 'Female')]
    q_data = only_binary.loc[:, useful_cols]

    #creates the success column which quantifies if an allegation was a success or not based on if the board_disposition was 
    #unsubstantiated/exonerated for unsuccessful and substantiated for successful 
    q_data['success'] = only_binary['board_disposition'].apply(lambda x: 0 if x in ['Unsubstantiated', 'Exonerated'] else 1)

    return q_data.reset_index(drop=True)

