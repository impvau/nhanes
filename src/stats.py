
import pandas as pd
import numpy as np
from indices import *

def rnd(x,n):               return round(x,n)       
def avg(df, field, dp = 1): return rnd(df[field].mean(),dp)
def pct(df1, df2, dp = 1):  return rnd( (df1['SEQN'].count()/df2['SEQN'].count())*100, dp)  

def df_mean(df):    return df.groupby(iSampleNo).mean().reset_index()       ### Collapse to mean of samples
def df_cnt(df):     return df[iSampleNo].count()

def pct_w(df1, df2, dp = 1):
    
    ratio = df1[iSampWeight].sum()/df2[iSampWeight].sum()
    return rnd(ratio*100,dp)

    '''
    try:
        #weights1 = df1.apply(lambda row: row[iSampleWeight05_06] if pd.isna(row[iSampleWeight]) else row[iSampleWeight], axis=1)
        #weights2 = df2.apply(lambda row: row[iSampleWeight05_06] if pd.isna(row[iSampleWeight]) else row[iSampleWeight], axis=1)
        ratio = df1[iSampWeight].sum()/df2[iSampWeight].sum()
        return rnd(ratio*100,dp)

    except:
        ratio = df1[iSampleWeight05_06].sum()/df2[iSampleWeight05_06].sum()
        return rnd(ratio*100,dp)
    '''

def avg_w(df, field, dp = 1):
    
    return rnd((df[field] * df[iSampWeight]).sum() / df[iSampWeight].sum(), dp)

    '''
    try:
        weights = df.apply(lambda row: row[iSampleWeight05_06] if pd.isna(row[iSampleWeight]) else row[iSampleWeight], axis=1)
        return rnd((df[field] * weights).sum() / weights.sum(), dp)

    except:
        return rnd((df[field]*df[iSampleWeight05_06]).sum()/df[iSampleWeight05_06].sum(),dp)       
    '''

def avg_w_n(df, field, dp=1):
    
      # Calculate the variance for the specified field
      variance = df[field].var()

      # Check for a zero variance to avoid division by zero
      if variance == 0:
            raise ValueError("Variance is zero, can't compute pooled weighted mean")

      # Calculate the weight as the inverse of the variance
      weight = 1 / variance

      # Calculate the sum of the weighted field values
      sum_weighted_field = (df[field] * weight).sum()

      # Calculate the sum of the weights
      sum_weights = weight * len(df)

      # Calculate the pooled weighted mean
      pooled_weighted_mean = sum_weighted_field / sum_weights

      # Round to the specified decimal places
      return round(pooled_weighted_mean, dp)

def corr_w(df, dfPbf, dfW):

    # Convert dataframe to series if it's a DataFrame
    if isinstance(df, pd.DataFrame):
        df = df.iloc[:, 0]

    # Drop missing values
    combined_data = pd.concat([df, dfPbf, pd.Series(dfW)], axis=1)
    combined_data.dropna(inplace=True)

    df_filtered = combined_data.iloc[:, 0]
    dfPbf_filtered = combined_data.iloc[:, 1]
    dfW_filtered = combined_data.iloc[:, 2]

    # Calculate weighted means
    x_weighted_mean = np.sum(np.multiply(dfW_filtered, df_filtered)) / np.sum(dfW_filtered)
    y_weighted_mean = np.sum(np.multiply(dfW_filtered, dfPbf_filtered)) / np.sum(dfW_filtered)

    # Calculate weighted covariance and variances
    cov_weighted = np.sum(dfW_filtered * (df_filtered - x_weighted_mean) * (dfPbf_filtered - y_weighted_mean))
    var_x_weighted = np.sum(dfW_filtered * (df_filtered - x_weighted_mean)**2)
    var_y_weighted = np.sum(dfW_filtered * (dfPbf_filtered - y_weighted_mean)**2)

    # Calculate weighted correlation
    return cov_weighted / np.sqrt(var_x_weighted * var_y_weighted)

def corr_w_mat(df, dfW):
    """
    Calculate a weighted correlation matrix for a DataFrame.

    :param df: A pandas DataFrame where each column represents a variable.
    :param dfW: A pandas Series or a list of sample weights.
    :return: A weighted correlation matrix.
    """
    # If dfW is a DataFrame with one column, convert it to a Series
    if isinstance(dfW, pd.DataFrame):
        if dfW.shape[1] == 1:
            dfW = dfW.iloc[:, 0]
        else:
            raise ValueError("dfW should be a Series or a DataFrame with only one column of weights.")
        
    # Ensure dfW is a pandas Series
    dfW = pd.Series(dfW) if not isinstance(dfW, pd.Series) else dfW

    # Initialize an empty DataFrame to store the weighted correlation matrix
    corr_matrix = pd.DataFrame(index=df.columns, columns=df.columns)

    # Iterate over combinations of columns to calculate pairwise weighted correlations
    for col1 in df.columns:
        for col2 in df.columns:
            combined_data = pd.concat([df[col1], df[col2], dfW], axis=1).dropna()
            w = combined_data.iloc[:, 2]

            # Calculate the means
            mean1 = np.average(combined_data.iloc[:, 0], weights=w)
            mean2 = np.average(combined_data.iloc[:, 1], weights=w)

            # Calculate the sum of weights for non-null pairs
            w_sum = w.sum()

            # Calculate weighted covariance
            cov_weighted = np.sum(w * (combined_data.iloc[:, 0] - mean1) * (combined_data.iloc[:, 1] - mean2)) / w_sum

            # Calculate weighted variances
            var1_weighted = np.sum(w * (combined_data.iloc[:, 0] - mean1)**2) / w_sum
            var2_weighted = np.sum(w * (combined_data.iloc[:, 1] - mean2)**2) / w_sum

            # Calculate the weighted correlation
            corr = cov_weighted / np.sqrt(var1_weighted * var2_weighted)

            # Assign the correlation to the correct place in the matrix
            corr_matrix.loc[col1, col2] = corr

    return corr_matrix.astype(float)

def scorr_w_mat(df, dfW):

    """
    Calculate a weighted Spearman correlation matrix for a DataFrame.

    :param df: A pandas DataFrame where each column represents a variable.
    :param dfW: A pandas Series or a DataFrame with a single column of sample weights.
    :return: A weighted Spearman correlation matrix.
    """
    # If dfW is a DataFrame with one column, convert it to a Series
    if isinstance(dfW, pd.DataFrame):
        if dfW.shape[1] == 1:
            dfW = dfW.iloc[:, 0]
        else:
            raise ValueError("dfW should be a Series or a DataFrame with only one column of weights.")

    # Ensure dfW is a pandas Series
    dfW = pd.Series(dfW) if not isinstance(dfW, pd.Series) else dfW

    # Rank the data
    ranked_df = df.rank(method="average")

    # Use the Pearson correlation function on ranked data to get Spearman correlation
    return corr_w_mat(ranked_df, dfW)
