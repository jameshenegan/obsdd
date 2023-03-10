import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

def get_stats_for_numeric_type_var(series):
    """
    Calculates various statistics for a numeric type variable.

    Args:
        series (pandas.Series): A pandas Series object.

    Returns:
        dict: A dictionary of various statistics for a numeric type variable.
    """
    mean = series.mean()
    median = series.median()

    stats_for_numeric_var = {}

    stats_for_numeric_var['max'] = series.max()
    stats_for_numeric_var['min'] = series.min()
    stats_for_numeric_var['mean'] = round(mean, 2)
    stats_for_numeric_var['median'] = round(median, 2)
    stats_for_numeric_var['potential_anomalies'] = get_potential_anomalies(series)

    quantiles = [0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95]
        
    for q in quantiles:
        stats_for_numeric_var[f'percentile_{round(100*q)}'] = round(series.quantile(q = q), 2)
        
    return stats_for_numeric_var


def get_potential_anomalies(series):
    """
    Uses DBSCAN algorithm to identify potential anomalies in a numeric type variable.

    Args:
        series (pandas.Series): A pandas Series object.

    Returns:
        list: A list of potential anomalies (outliers) in the variable.
    """
    # Prepare data for algorithm
    X_raw = series.dropna()        
    X = np.array(X_raw).reshape(-1,1)
    X = StandardScaler().fit_transform(X)

    # Instantiate the dbscan and fit X 
    db = DBSCAN(eps=0.8, min_samples=10).fit(X)

    # The potential anomalies are observations with a label of -1
    labels = db.labels_
    potential_anomalies = list(X_raw[labels == -1])

    # Help with presentation
    potential_anomalies = [round(po, 4) for po in potential_anomalies]
    potential_anomalies.sort()

    return potential_anomalies
