'''
 * @file
 * @author andy@impv.au
 * @version 1.0
 * @brief 
 *   Filter functions for the NHANES replication of Woolcots work
 *   Additional work for our publication
 * 
'''

from indices import *

### Sex filtering
def f_wom(df):  return df[df[iSex] == 2]    # Filter women
def f_men(df):  return df[df[iSex] == 1]    # Filter men

### Race filtering
def f_mex(df):  return df[df[iRace] == 1]       # Filter mex-am
def f_eur(df):  return df[df[iRace] == 3]       # Filter eur-am
def f_afr(df):  return df[df[iRace] == 4]       # Filter afr-am
def f_race(df): return df[(df[iRace] == 1)|(df[iRace] == 3)|(df[iRace] == 4)]  # Filter mex-am, eur-am, afr-am

### Age-based filtering
def f_age_y(df):    return df[(df[iAge] >= 20) & (df[iAge] <= 39)]  # Filter young (20-39)
def f_age_m(df):    return df[(df[iAge] >= 40) & (df[iAge] <= 59)]  # Filter young (20-39)
def f_age_a(df):    return df[(df[iAge] >= 60)]                     # Filter aged (>=60)
def f_age_o(df):    return df[(df[iAge] >= 60) & (df[iAge] <= 85)]  # Filter old (60-85)
def f_age_20(df):   return df[(df[iAge] >= 20)]                     # Filter more than 20
def f_age_60(df):   return df[(df[iAge] >= 60)]                     # Filter more than 60
def f_age_70(df):   return df[(df[iAge] >= 20) & (df[iAge] <= 69)]  # Filter more than 20, less than 70
def f_age_tr(df):   return f_age_20(df)
def f_age_te(df):   return f_age_70(df)

### BMI-based filtering
def f_bmi_u(df):    return df[df[iBMI] < 18.5]                      # Filter underweight (<18.5)
def f_bmi_n(df):    return df[(df[iBMI] >= 18.5) & (df[iBMI] < 25)] # Filter normal (18.5-24.9)
def f_bmi_o(df):    return df[(df[iBMI] >= 25) & (df[iBMI] < 30)]   # Filter overweight (25-29.9)
def f_bmi_ob(df):   return df[df[iBMI] >= 30]                       # Filter obese (>=30)    

### Filter imputation
def f_imp(df, isTr):    return df[df[iImpFlag] == 1] if isTr else df[df[iImpFlag05_06] == 1]
def f_nimp(df, isTr):   return df[df[iImpFlag] != 1] if isTr else df[df[iImpFlag05_06] != 1]

### Filter minimum indicies
def f_vars(df, isTr = True):

    if isTr: return df[[iBodyFatPct, iBMI, iWaist, iArm, iWeight, iTricep, iThigh, iSubscap, iCalf, iArmLen, iHeight, iLegLen]], df[[iSampleWeight]]
    else: raise Exception("Not implemented")

### Fitler na's according to Woolcots paper
def f_na_paper(df): 

    # Filter out incomplete DXX data
    df = df.dropna(subset=[iBodyFatPct])
    df = df.dropna(subset=[iWeight])          # Exclude missing body weight
    df = df.dropna(subset=[iHeight])          # Exclude missing height
    df = df.dropna(subset=[iWaist])           # Exclude missing waist circumference
    return df

### Apply all filters according to Woolcots paper
def f_all_paper(df, isTr = True):

    # Filter by age
    if isTr:        df = f_age_tr(df)
    else:           df = f_age_te(df)

    df = f_na_paper(df)
    
    return df

### Apply additional filters according to our paper
def f_all_ours(df, isTr = True):

    df = f_all_paper(df, isTr)                  # Do all Woolcot does
    df = f_race(df)                             # Filter by race classes we are considering !!! Authors do not do this      
    df = df.dropna(subset=iConsider, axis=0)    # Drop na values in other fields    

    return df
