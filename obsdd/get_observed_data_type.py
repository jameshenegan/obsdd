from obsdd.date_helpers import (
    string_series_is_series_of_blsa_dates,
    string_series_is_series_of_extended_blsa_dates,
    string_series_is_series_of_td_dates
)

def get_observed_data_type(series):
    """
    Infer the data type of a pandas Series based on its contents.

    Parameters
    ----------
    series : pandas.Series
        A pandas Series to classify.

    Returns
    -------
    str
        A string representing the inferred data type of the Series.

    Notes
    -----
    This function uses a set of heuristics to infer the data type of a pandas
    Series based on its contents. The heuristics used are as follows:

    1. If the Series is classified as datetime64 by pandas, return "DateTime".
    2. If the Series is classified as object by pandas and appears to contain
       dates, return "DateTime".
    3. If the Series is classified as numeric by pandas and contains only
       integers, return "Integer".
    4. If the Series is classified as numeric by pandas and contains non-integer
       values, return "Decimal".
    5. If the Series is classified as object by pandas and contains a small
       number of unique values, return "StringList".
    6. If none of the above conditions hold, return "String".
    """
    if classified_as_datetime_by_pandas(series):
        return "DateTime"

    elif classified_as_object_by_pandas(series) and appears_to_be_date(series):
        return "DateTime"

    elif classified_as_numeric_by_pandas(series) and every_value_is_an_integer(series) and has_small_number_of_unique_values(series):
        return "NumberList"

    elif classified_as_numeric_by_pandas(series) and not every_value_is_an_integer(series):
        return "Decimal"

    elif classified_as_object_by_pandas(series) and has_small_number_of_unique_values(series):
        return "StringList"

    else:
        return "String"


def classified_as_datetime_by_pandas(series):
    """
    Check if a pandas Series is classified as datetime64 by pandas.

    Parameters
    ----------
    series : pandas.Series
        A pandas Series to check.

    Returns
    -------
    bool
        True if the Series is classified as datetime64 by pandas, False otherwise.
    """
    return str(series.dtype) == "datetime64"


def classified_as_numeric_by_pandas(series):
    """
    Check if a pandas Series is classified as numeric by pandas.

    Parameters
    ----------
    series : pandas.Series
        A pandas Series to check.

    Returns
    -------
    bool
        True if the Series is classified as numeric by pandas (either int64 or float64), False otherwise.
    """
    return str(series.dtype) in ['int64', 'float64']


def classified_as_object_by_pandas(series):
    """
    Check if a pandas Series is classified as object by pandas.

    Parameters
    ----------
    series : pandas.Series
        A pandas Series to check.

    Returns
    -------
    bool
        True if the Series is classified as object by pandas, False otherwise.
    """
    return str(series.dtype) == "object"


def has_small_number_of_unique_values(series):
    """
    Check if a pandas Series has a small number of unique values.

    Parameters
    ----------
    series : pandas.Series
        A pandas Series to check.

    Returns
    -------
    bool
        True if the Series has 15 or fewer unique values, False otherwise.
    """
    SMALL_NUMBER = 15
    num_unique_vales = len(list(series.unique()))
    return num_unique_vales <= SMALL_NUMBER


def appears_to_be_date(series):
    """
    Check if a pandas Series appears to contain dates.

    Parameters
    ----------
    series : pandas.Series
        A pandas Series to check.

    Returns
    -------
    bool
        True if the Series appears to contain dates, False otherwise.

    Notes
    -----
    This function checks if the Series appears to contain dates by checking if
    all non-missing values in the Series match one of several recognized date
    formats. Specifically, it checks if the Series is a series of BLSA dates,
    extended BLSA dates, or Stata TD dates.
    """
    if not classified_as_object_by_pandas(series):
        return False

    if string_series_is_series_of_blsa_dates(series):
        return True
      
    if string_series_is_series_of_extended_blsa_dates(series):
        return True
    
    if string_series_is_series_of_td_dates(series):
        return True
      
    else:
        return False


def every_value_is_an_integer(series):
    """
    Check if all values in a pandas Series are integers.

    Parameters
    ----------
    series : pandas.Series
        A pandas Series to check.

    Returns
    -------
    bool
        True if all values in the Series are integers, False otherwise.

    Notes
    -----
    This function checks if all values in the Series are integers by comparing
    the "int" version of each value to its "decimal" form. If the "int" version
    of each value is the same as the "decimal" form, then the value is an
    integer. This method works even if the Series contains missing values.
    """
    if not classified_as_numeric_by_pandas(series):
        return False

    all_integers = False

    temp_1 = series.dropna().apply(lambda x: int(x))
    temp_2 = series.dropna()

    difference = temp_1 - temp_2
    
    squared_difference = difference.apply(lambda x: x*x)

    sum_squared_difference = squared_difference.sum()

    if sum_squared_difference == 0:
        all_integers = True

    return all_integers
