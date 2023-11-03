
'''
from download.download import get_map
import pandas as pd

#The two-year sample weights (WTINT2YR, WTMEC2YR) should be used for NHANES 1999-2000
#analyses and the four-year sample weights (

### Pre-processing filtering
def f_age(dfTrain, dfTest):
      # Filter by age (>20 for train, 20-69 for test)
      return dfTrain[dfTrain[iAge] >= 20], dfTest[(dfTest[iAge] >= 20) & (dfTest[iAge] <= 69)]

def f_na(dfTrain, dfTest):
      # Filter by na values in iBodyFatPct, iWeight, iHeight, iWaist

      # Filter out incomplete DXX data
      dfTrain = dfTrain.dropna(subset=[iBodyFatPct])

      # Filter out incomplete DXX data
      dfTrain = dfTrain.dropna(subset=[iWeight])          # Exclude missing body weight
      dfTrain = dfTrain.dropna(subset=[iHeight])          # Exclude missing height
      dfTrain = dfTrain.dropna(subset=[iWaist])           # Exclude missing waist circumference

      # Apply for test
      dfTest = dfTest.dropna(subset=[iBodyFatPct])
      dfTest = dfTest.dropna(subset=[iWeight])          # Exclude missing body weight
      dfTest = dfTest.dropna(subset=[iHeight])          # Exclude missing height
      dfTest = dfTest.dropna(subset=[iWaist])       # Exclude missing waist circumference

      return dfTrain, dfTest

def f_all(dfTrain, dfTest):
      # Filter both f_age and f_na
      dfTrain, dfTest = f_age(dfTrain, dfTest)
      dfTrain, dfTest = f_na(dfTrain, dfTest)
      dfTrain, dfTest = f_race(dfTrain, dfTest)
      return dfTrain, dfTest

def f_imp(dfTrain, dfTest):
      # Filter by imputation flag
      #return dfTrain[dfTrain[iImpFlag] == 1], dfTest[dfTest[iImpFlag] == 1]
      # Warning; the dfTrain array does not have the imputation flag, so we use the dfTest array so we take no action on it
      return dfTrain[dfTrain[iImpFlag] == 1], dfTest[dfTest[iImpFlag05_06] == 1]

def f_nimp(dfTrain, dfTest):
      # Filter by imputation flag. based on the data there is either 1 or 5.4e^-79, so we use != 1 just in case
      #return dfTrain[dfTrain[iImpFlag] != 1], dfTest[dfTest[iImpFlag] != 1]

      # Warning; the dfTrain array does not have the imputation flag, so we use the dfTest array so we take no action on it
      return dfTrain[dfTrain[iImpFlag] != 1], dfTest[dfTest[iImpFlag05_06] != 1]

### Collapse to mean of samples
def df_mean(dfTrain, dfTest):

      # Prepare averages with correct sequence numbers
      dfTrain_avg = dfTrain.groupby(iSampleNo).mean().reset_index()
      dfTest_avg = dfTest.groupby(iSampleNo).mean().reset_index()

      return dfTrain_avg, dfTest_avg


### 
def build_data(imp = 2):

      # imp = 0; only non-imputed data
      # imp = 1; only imputed data
      # imp = 2; both non-imputed and imputed data

      dfs = {}
      for year, datasets in get_map(dir).items():
            for dataset in datasets:

                  with open( f"{dataset[1]}", 'rb') as f:
            
                        fullDs = dataset[1].split('/')[-1].split('.')[0]
                        logicalDs = fullDs.replace("_S", "")
                        
                        df = pd.read_sas(f, format='xport')
                        #df['year'] = year
                        #df['dataset'] = fullDs

                        if '1999' in year or '2001' in year or '2003' in year:
                              logicalDs = logicalDs.replace("_B", "")
                              logicalDs = logicalDs.replace("_C", "")
                              logicalDs = logicalDs+"_Train"
                              print(f"Train: {fullDs} {df[iSampleNo].nunique()}")
                        
                        elif '2005' in year:
                              logicalDs = logicalDs.replace("_D", "")
                              logicalDs = logicalDs+"_Test"
                              print(f"Test: {fullDs} {df[iSampleNo].nunique()}")
                                    
                        # If the dataset type is already in our dictionary, append the data.
                        # Otherwise, initialize a new dataframe for this dataset type.
                        if logicalDs in dfs:
                              dfs[logicalDs] = pd.concat([dfs[logicalDs], df], ignore_index=True)
                        else:
                              dfs[logicalDs] = df

      dfTrain = dfs['DEMO_Train'].merge(dfs['DXX_Train'], on=iSampleNo, how='left') 
      dfTrain = dfTrain.merge(dfs['BMX_Train'], on=iSampleNo, how='left') 

      dfTest = dfs['DEMO_Test'].merge(dfs['DXX_Test'], on=iSampleNo, how='left') 
      dfTest = dfTest.merge(dfs['BMX_Test'], on=iSampleNo, how='left') 

      # Add BMI fields
      dfTrain[iBMICalc] = (dfTrain[iWeight] / ((dfTrain[iHeight] / 100) ** 2)) 
      dfTest[iBMICalc] = (dfTest[iWeight] / ((dfTest[iHeight] / 100) ** 2))

      dfTrain, dfTest = f_all(dfTrain, dfTest)

      return dfTrain, dfTest


###

def rnd(x,n):
    return round(x,n)

def cnt(df):
    return df[iSampleNo].count()

def pct(df1, df2, dp = 1):

      ratio = df1['SEQN'].count() / df2['SEQN'].count()
      return rnd(ratio*100,dp)  

def pct_w(df1, df2, dp = 1):
    
      #global dbg
      #if dbg == True:
      #    df.loc[cond].to_csv('dfWomen.t.20-40.csv', index=False)
      #    dbg = False

      #print(f"sum: {df.loc[cond, iSampleWeight].sum()}, total:{df[iSampleWeight].sum()}, cnt:{df.loc[cond, iSampleNo].count()}  all:{df[iSampleNo].count()}")

      try:
      
            index4 = iSampleWeight
            index2 = iSampleWeight05_06

            weights1 = df1.apply(lambda row: row[index2] if pd.isna(row[index4]) else row[index4], axis=1)
            weights2 = df2.apply(lambda row: row[index2] if pd.isna(row[index4]) else row[index4], axis=1)
     
            ratio = weights1.sum() / weights2.sum()
            return rnd(ratio*100,dp)
    
      except:
          
            ratio = df1[iSampleWeight05_06].sum() / df2[iSampleWeight05_06].sum()
            return rnd(ratio*100,dp)

def avg(df, field, dp = 1):
    return rnd(df[field].mean(),dp)

def avg_w(df, field, dp = 1):
    
      try:

            index4 = iSampleWeight
            index2 = iSampleWeight05_06
            weights = df.apply(lambda row: row[index2] if pd.isna(row[index4]) else row[index4], axis=1)

            return rnd((df[field] * weights).sum() / weights.sum(), dp)
            #return rnd((df[field]*df[iSampleWeight]).sum()/df[iSampleWeight].sum(),dp)
    
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
'''