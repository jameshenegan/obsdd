# `obsdd`

## Introduction

The `obsdd` package lets a user create an **observed data dictionary** for a pandas DataFrame.

### What is an observed data dictionary?

Suppose that `df` is a pandas DataFrame. Then an observed data dictionary for `df` would be a DataFrame that contains **summary statistics** for the fields of the original DataFrame `df`.

#### A simple example

We can illustrate the basic idea behind an observed data dictionary with the following DataFrame:

| age_years | height_cm | weight_kg |
| --------- | --------- | --------- |
| 60        | 192       | 90        |
| 42        | 170       | 82        |
| 85        | 180       | 85        |
| 70        | 167       | 84        |

A relatively straightforward observed data dictionary for this DataFrame might look something like this:

| var_name  | count | mean   | std     | min | 25%    | 50%  | 75%   | max |
| --------- | ----- | ------ | ------- | --- | ------ | ---- | ----- | --- |
| age_years | 4     | 64.25  | 18.043  | 42  | 55.5   | 65   | 73.75 | 85  |
| height_cm | 4     | 177.25 | 11.2952 | 167 | 169.25 | 175  | 183   | 192 |
| weight_kg | 4     | 85.25  | 3.40342 | 82  | 83.5   | 84.5 | 86.25 | 90  |

#### Additional Summary Statistics

While the observed data dictionary in the example shown above can be created with a few lines of code, we can imagine that one may want additional summary statistics. The purpose of the obsdd package is to help people create a more detailed observed data dictionary than the one shown above.

## Observed Data Types

The summary statistics shown for a variable will depend on that variable's **observed data type**.

We will consider the following data types:

- Integer
- Decimal
- NumberList
- StringList
- DateTime
- String

## Common Summary Statistics

No matter the observed data type, a variable will have the following summary statistics:

- `obs_numobs`: Number of non-missing values
- `obs_distinct`: Number of distinct values
- `obs_data_type`: The data type that was determined by guess_data_type.py.
- `obs_missing`: A string field of the form "N (p%)", where N is the number of missing values and p is the percentage of values that are missing.

### Summary Statistics for Numeric Variables

If the obs_data_type for a variable is either Integer or Decimal, then we provide the following summary statistics:

- `obs_min`: The minimum observed value
- `obs_max`: The maximum observed value
- `obs_mean`: The observed mean
- `obs_anomalies`: Values considered to be "anomalies" by an "anomaly detection algorithm"
- `obs_p_5`: The fifth percentile of the observed data
- `obs_p_10`
- `obs_p_25`
- `obs_median`
- `obs_p_75`
- `obs_p_90`
- `obs_p_95`

### Summary Statistics for List-Type Variables

If the `obs_data_type` for a variable is either StringList or NumberList, then we provide the following summary statistics:

- `obs_permissible_values`: A list of the observed permissible values for the variable
- `obs_pv_pcts`: A list of objects the keys "value" and "pct", where "value" is a permissible value for the variable and "pct" is the percentage of non-missing observations with that value.

#### LUobs

In addition to the two fields shown above, the obsdd package also creates a DataFrame containing information on the observed permissible value percentages in long format. Traditionally, this DataFrame is called LUobs and has the following schema:

- `var_name`: Name of the variable
- `var_value`: Value of the variable
- `val_count`: The number of observations that have the given value
- `val_pct_drop_missing_in_total`: This equals val_count divided by df[var_name].dropna().shape[0]
- `val_pct_keep_missing_in_total`: This equals val_count divided by df.shape[0]

## Usage

First, import the ObsDD package:

```python
import obsdd
```

To generate a summary of the data in a Pandas DataFrame, call the make_obs_dd() function with the DataFrame as an argument:

```python
df = pd.read_csv("my_data.csv")
obs_dd, lu_obs = obsdd.make_obs_dd(df)
```

obs_dd is a Pandas DataFrame containing summary statistics for each variable in the original DataFrame. lu_obs is a Pandas DataFrame containing value counts for each variable in the original DataFrame.
