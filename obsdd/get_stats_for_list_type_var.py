def get_stats_for_list_type_var(series, observed_data_type):
    """
    Computes statistics for a series column of type 'NumberList' or 'StringList'
    
    Parameters:
        series (pandas.Series): The series column to compute statistics for
        observed_data_type (str): The observed data type of the series column
    
    Returns:
        dict: A dictionary containing statistics for the series column
    """
    
    permissible_values = get_permissible_values(series, observed_data_type)
    pv_pcts = get_pv_pcts(series, observed_data_type)
    
    stats_for_list_type_var = {}
    stats_for_list_type_var['permissible_values'] = permissible_values
    stats_for_list_type_var['pv_pcts'] = pv_pcts

    return stats_for_list_type_var


def get_permissible_values(series, observed_data_type):
    """
    Computes the permissible values for a series column of type 'NumberList' or 'StringList'
    
    Parameters:
        series (pandas.Series): The series column to compute permissible values for
        observed_data_type (str): The observed data type of the series column
    
    Returns:
        list: A list of permissible values for the series column
    """

    permissible_values = list(series.dropna().unique())

    if observed_data_type == "NumberList":
        permissible_values = [int(pv) for pv in permissible_values]
        permissible_values.sort()
        
    return permissible_values


def get_pv_pcts(series, observed_data_type):
    """
    Computes the percentages of each permissible value for a series column of type 'NumberList' or 'StringList'
    
    Parameters:
        series (pandas.Series): The series column to compute permissible value percentages for
        observed_data_type (str): The observed data type of the series column
    
    Returns:
        str: A string representation of a list of dictionaries containing permissible value percentages
    """

    no_missing = series.dropna()
    length = no_missing.shape[0]
    props = no_missing.value_counts() / length
    pcts = props.apply(lambda x: f'{round(100 * x , 2)}%')
    
    pcts = pcts.reset_index()
    pcts = pcts.rename(columns = {"index" : "value", series.name : "pct"})
    if observed_data_type == "NumberList":
        pcts['value'] = pcts['value'].astype(int)
    
    pcts = pcts.to_dict(orient = "records")
    pcts = str(pcts)
    
    return pcts
