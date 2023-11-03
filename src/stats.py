
import pandas as pd
import numpy as np
from indices import *

def rnd(x,n):               return round(x,n)       
def avg(df, field, dp = 1): return rnd(df[field].mean(),dp)
def pct(df1, df2, dp = 1):  return rnd( (df1['SEQN'].count()/df2['SEQN'].count())*100, dp)  

def df_mean(df):    return df.groupby(iSampleNo).mean().reset_index()       ### Collapse to mean of samples
def df_cnt(df):     return df[iSampleNo].count()

def pct_w(df1, df2, dp = 1):
    
      try:
            weights1 = df1.apply(lambda row: row[iSampleWeight05_06] if pd.isna(row[iSampleWeight]) else row[iSampleWeight], axis=1)
            weights2 = df2.apply(lambda row: row[iSampleWeight05_06] if pd.isna(row[iSampleWeight]) else row[iSampleWeight], axis=1)
            ratio = weights1.sum()/weights2.sum()
            return rnd(ratio*100,dp)
    
      except:
            ratio = df1[iSampleWeight05_06].sum()/df2[iSampleWeight05_06].sum()
            return rnd(ratio*100,dp)

def avg_w(df, field, dp = 1):
    
      try:
            weights = df.apply(lambda row: row[iSampleWeight05_06] if pd.isna(row[iSampleWeight]) else row[iSampleWeight], axis=1)
            return rnd((df[field] * weights).sum() / weights.sum(), dp)
    
      except:
            return rnd((df[field]*df[iSampleWeight05_06]).sum()/df[iSampleWeight05_06].sum(),dp)       

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
