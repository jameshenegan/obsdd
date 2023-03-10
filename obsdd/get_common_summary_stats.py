from obsdd.get_observed_data_type import get_observed_data_type


def get_common_summary_stats(series):
    """
    Get a dictionary of common summary statistics for a pandas Series.

    Parameters
    ----------
    series : pandas.Series
        A pandas Series to get summary statistics for.

    Returns
    -------
    dict
        A dictionary containing the following keys and values:
            'number_of_observed_values': The number of non-missing values in the Series.
            'number_of_distinct_values': The number of distinct values in the Series.
            'string_of_missing_stats': A string describing the number and percentage of missing values in the Series.
            'observed_data_type': A string describing the data type of the non-missing values in the Series.

    Notes
    -----
    This function uses several helper functions to compute summary statistics for
    a pandas Series. The helper functions are documented separately.
    """
    number_of_observed_values = get_number_of_observed_values(series)
    number_of_distinct_values = get_number_of_distinct_values(series)
    string_of_missing_stats = get_string_of_missing_stats(series)
    observed_data_type = get_observed_data_type(series)
 
    common_summary_stats = {}
    common_summary_stats['number_of_observed_values'] = number_of_observed_values
    common_summary_stats['number_of_distinct_values'] = number_of_distinct_values
    common_summary_stats['string_of_missing_stats'] = string_of_missing_stats
    common_summary_stats['observed_data_type'] = observed_data_type

    return common_summary_stats


def get_number_of_observed_values(series):
    """
    Get the number of non-missing values in a pandas Series.

    Parameters
    ----------
    series : pandas.Series
        A pandas Series to count non-missing values in.

    Returns
    -------
    int
        The number of non-missing values in the Series.
    """
    number_of_observed_values = series.dropna().shape[0]
    return number_of_observed_values


def get_number_of_distinct_values(series):
    """
    Get the number of distinct values in a pandas Series.

    Parameters
    ----------
    series : pandas.Series
        A pandas Series to count distinct values in.

    Returns
    -------
    int
        The number of distinct values in the Series.
    """
    number_of_distinct_values = len(list(series.unique()))
    return number_of_distinct_values


def get_string_of_missing_stats(series):
    """
    Get a string describing the number and percentage of missing values in a pandas Series.

    Parameters
    ----------
    series : pandas.Series
        A pandas Series to count missing values in.

    Returns
    -------
    str
        A string describing the number and percentage of missing values in the Series.
    """
    num_missing = series[series.isna()].shape[0]
    prop_missing = num_missing / series.shape[0]
    pct_missing = f'{round(100 * prop_missing, 2)}%'
    string_of_missing_stats = f'{num_missing} ({pct_missing})'
    return string_of_missing_stats
