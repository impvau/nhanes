
import pandas as pd

from download import *
from filters import *
from indices import *
from stats import *

def preproc(dir):

    dfs = {}
    for year, datasets in get_map(dir).items():

        for dataset in datasets:

            with open( f"{dataset[1]}", 'rb') as f:

                fullDs = dataset[1].split('/')[-1].split('.')[0]
                logicalDs = fullDs.replace("_S", "")
                
                df = pd.read_sas(f, format='xport')

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

    # Fill 4Y sample weight with 2Y sample weight where 4 does not exist
    dfTrain[iSampleWeight] = dfTrain[iSampleWeight].fillna(dfTrain[iSampleWeight05_06])

    # Take means
    dfTrain = df_mean(dfTrain)
    dfTest = df_mean(dfTest)

    # Adjust values if necessary
    dfTrain.loc[:, iBodyFat] = dfTrain[iBodyFat].div(1000, fill_value=0)
    dfTrain.loc[:, iFatFreeMass] = dfTrain[iFatFreeMass].div(1000, fill_value=0)
    dfTest.loc[:, iBodyFat] = dfTest[iBodyFat].div(1000, fill_value=0)
    dfTest.loc[:, iFatFreeMass] = dfTest[iFatFreeMass].div(1000, fill_value=0)

    return dfTrain, dfTest