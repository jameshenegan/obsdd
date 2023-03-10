from obsdd.get_observed_data_type import every_value_is_an_integer

def make_lu_obs_df_for_var(series):
    """
    Returns a Pandas DataFrame containing a lookup table of observed values and their counts.

    Args:
    - series: Pandas Series object

    Returns:
    - Pandas DataFrame object containing a lookup table of observed values and their counts.
    """

    total = series.shape[0]
    total_non_missing = series.dropna().shape[0]

    # Get value counts
    value_counts = series.value_counts()
    value_counts_with_index = value_counts.reset_index()
    vc = value_counts_with_index

    # Rename columns and add percentage columns
    vc = vc.rename(columns = {"index" : "var_value", series.name : "value_count"}) 
    vc['val_pct_keep_missing_in_total'] = vc['value_count'].apply(lambda x: f'{round(100 * x/total, 2)}%')
    vc['val_pct_drop_missing_in_total'] = vc['value_count'].apply(lambda x: f'{round(100 * x/total_non_missing, 2)}%')

    # Add the variable name
    vc['var_name'] = series.name

    # Rearrange column order
    new_col_order = ['var_name']
    new_col_order += [c for c in vc.columns if c not in new_col_order]
    vc = vc[new_col_order]

    # If the 'var_value' count is full of integers, then convert to integer
    if every_value_is_an_integer(vc['var_value']):
        vc['var_value'] = vc['var_value'].astype(int)

    return vc
