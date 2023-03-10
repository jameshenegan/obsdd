import re


def string_series_is_series_of_blsa_dates(series):
    """
    Check if a pandas Series of strings represents a series of valid BLSA dates.

    Parameters
    ----------
    series : pandas.Series
        A pandas Series of strings.

    Returns
    -------
    bool
        True if all non-missing values in the series match the BLSA date pattern
        ('YYYY-MM-DD'), False otherwise.
    """
    # Remove missing values from the series
    no_missing = series.dropna()

    # Get the number of non-missing values in the series
    num_in_series = no_missing.shape[0]

    # Count the number of non-missing values that match the BLSA date pattern
    num_matching_blsa_date_pattern = no_missing.apply(lambda x: string_is_blsa_date(x)).sum()

    # Check if all non-missing values match the BLSA date pattern
    return num_matching_blsa_date_pattern == num_in_series


def string_series_is_series_of_extended_blsa_dates(series):
    """
    Check if a pandas Series of strings represents a series of valid extended BLSA dates.

    Parameters
    ----------
    series : pandas.Series
        A pandas Series of strings.

    Returns
    -------
    bool
        True if all non-missing values in the series match the extended BLSA date pattern
        ('YYYY-MM-DD HH:MM:SS'), False otherwise.
    """
    # Remove missing values from the series
    no_missing = series.dropna()

    # Get the number of non-missing values in the series
    num_in_series = no_missing.shape[0]

    # Count the number of non-missing values that match the extended BLSA date pattern
    num_matching_blsa_date_pattern = no_missing.apply(lambda x: string_is_extended_blsa_date(x)).sum()

    # Check if all non-missing values match the extended BLSA date pattern
    return num_matching_blsa_date_pattern == num_in_series


def string_series_is_series_of_td_dates(series):
    """
    Check if a pandas Series of strings represents a series of valid Stata TD dates.

    Parameters
    ----------
    series : pandas.Series
        A pandas Series of strings.

    Returns
    -------
    bool
        True if all non-missing values in the series match the Stata TD date pattern
        ('DDMONYYYY'), False otherwise.
    """
    # Remove missing values from the series
    no_missing = series.dropna()

    # Get the number of non-missing values in the series
    num_in_series = no_missing.shape[0]

    # Count the number of non-missing values that match the Stata TD date pattern
    num_matching_td_date_pattern = no_missing.apply(lambda x: string_is_stata_td_date(x)).sum()

    # Check if all non-missing values match the Stata TD date pattern
    return num_matching_td_date_pattern == num_in_series


def string_is_blsa_date(string):
    """
    Check if a string represents a valid BLSA date.

    Parameters
    ----------
    string : str
        A string to check.

    Returns
    -------
    bool
        True if the string matches the BLSA date pattern ('YYYY-MM-DD'), False otherwise.
    """
    # Compile regular expression pattern for BLSA dates
    blsa_date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    
    # Check if the input string matches the pattern
    return blsa_date_pattern.match(str(string)) is not None


def string_is_extended_blsa_date(string):
    """
    Check if a string represents a valid extended BLSA date.

    Parameters
    ----------
    string : str
        A string to check.

    Returns
    -------
    bool
        True if the string matches the extended BLSA date pattern
        ('YYYY-MM-DD HH:MM:SS'), False otherwise.
    """
    # Compile regular expression pattern for extended BLSA dates
    blsa_date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
    
    # Check if the input string matches the pattern
    return blsa_date_pattern.match(str(string)) is not None


def string_is_stata_td_date(string):
    """
    Check if a string represents a valid Stata TD date.

    Parameters
    ----------
    string : str
        A string to check.

    Returns
    -------
    bool
        True if the string matches the Stata TD date pattern ('DDMONYYYY'), False otherwise.
    """
    # List of valid Stata TD month abbreviations
    list_of_months = ['mar', 'jan', 'may', 'nov', 'dec', 'aug', 'oct', 'sep', 'jun', 'jul', 'feb', 'apr']
    
    # Check if the input string is a valid Stata TD date
    if len(str(string)) != 9:
        return False
    elif not re.compile(r'\d{2}\b').match(str(string)[:2]):
        return False
    elif not re.compile(r'\d{4}\b').match(str(string)[-4:]):
        return False
    elif str(string)[2:5] not in list_of_months:
        return False
    else:
        return True
