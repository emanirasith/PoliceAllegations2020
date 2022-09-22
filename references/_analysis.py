import pandas as pd

def aggregates_analysis(df):
    
    df = df.assign(gender = q_data['complainant_gender'].replace({'Male':1,'Female':2}))
    tmp = df.groupby(['allegation'])['gender'].mean() 
    out = (tmp == 2) | (tmp==1)
    alle = out[out].index
    new_data = df[~df['allegation'].isin(alle)]
    types = new_data.allegation.unique()

    return types

def shuffle(df, n, col_name):
    
    tvds = []
    for _ in range(n):
        

        shuffled_col = (
            df[col_name]
            .sample(replace=False, frac=1)
            .reset_index(drop=True)
        )
        

        shuffled = (
            df
            .assign(**{
                col_name: shuffled_col,
                'is_null': df['complainant_ethnicity'].isnull()
            })
        )
        

        shuffled = (
            shuffled
            .pivot_table(index='is_null', columns=col_name, aggfunc='size')
            .apply(lambda x:x / x.sum(), axis=1)
        )
        
        tvd = shuffled.diff().iloc[-1].abs().sum() / 2

        
        tvds.append(tvd)
        
    return tvds

def empirical_distr(df, col_name):

    new_df = df.assign(is_null=df.complainant_ethnicity.isnull())\
        .pivot_table(index='is_null', columns=col_name, aggfunc='size')\
            .apply(lambda x:x / x.sum(), axis=1)

    return new_df 

def hypothesis_testing(df, alleg, n):

    differences = []
    for i in alleg:
        lst = []
        for j in range(n):
            filt = df[df['allegation'] == i].reset_index(drop=True)

            shuffled_successes = (
                filt['success']
                .sample(replace=False, frac=1)
                .reset_index(drop=True)
            )


            shuffled = (
                filt
                .assign(**{'shuffled success': shuffled_successes})
            )


            group_means = (
                shuffled
                .groupby('complainant_gender')
                .mean()
                .loc[:, 'shuffled success']
            )
            difference = group_means.diff().iloc[-1]

        
            lst.append(abs(difference))
        differences.append(lst)

    return differences

def observed(df, alleg):

    obs_diff = []
    for i in alleg:
        filt = df[df['allegation'] == i].reset_index(drop=True)
        observed_difference = (
            filt
            .groupby('complainant_gender')['success']
            .mean()
            .diff()
            .iloc[-1]
        )
        obs_diff.append(observed_difference)
    
    return obs_diff
