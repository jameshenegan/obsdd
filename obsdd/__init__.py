"""
ObsDD: Observed Data Dictionary

ObsDD is a package for generating a description of the variables and their statistical properties in a pandas DataFrame.

"""

import pandas as pd

from obsdd.get_common_summary_stats import get_common_summary_stats
from obsdd.get_stats_for_list_type_var import get_stats_for_list_type_var
from obsdd.get_stats_for_numeric_type_var import get_stats_for_numeric_type_var
from obsdd.make_lu_obs_df_for_var import make_lu_obs_df_for_var

def make_obs_dd(df):
    """
    Generate an observed data dictionary (ObsDD) of the input pandas DataFrame.

    Args:
    df: pandas DataFrame containing the data to be described.

    Returns:
    obs_dd: pandas DataFrame containing the ObsDD.
    lu_obs: pandas DataFrame containing the Look-Up (LU) Observations.

    """

    obs_dd_records = []
    lu_obs_dfs = []

    col_names = list(df.columns)

    # Loop over all columns in the input DataFrame
    for col_name in col_names:

        series = df[col_name]

        summary_stats = {}
        summary_stats['var_name'] = col_name

        common_summary_stats = get_common_summary_stats(series)
        summary_stats.update(common_summary_stats)

        observed_data_type = summary_stats['observed_data_type']

        if observed_data_type in ['NumberList', 'StringList']:
            stats_for_list_type_var = get_stats_for_list_type_var(series, observed_data_type)
            summary_stats.update(stats_for_list_type_var)

            # Make Look-Up (LU) Observations for variable
            lu_obs_for_var = make_lu_obs_df_for_var(series)
            lu_obs_dfs.append(lu_obs_for_var)


        if observed_data_type in ['Integer', 'Decimal']:
            stats_for_numeric_var = get_stats_for_numeric_type_var(series)
            summary_stats.update(stats_for_numeric_var)
            
        obs_dd_records.append(summary_stats)

    # Combine all ObsDD records into a single DataFrame
    obs_dd = pd.DataFrame(obs_dd_records)

    # Combine all Look-Up (LU) Observations into a single DataFrame
    if len(lu_obs_dfs) > 0:
      lu_obs = pd.concat(lu_obs_dfs)
      lu_obs = lu_obs.reset_index(drop = True)
    
    else:
      lu_obs = pd.DataFrame()

    return obs_dd, lu_obs
