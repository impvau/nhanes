import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from indices import *
from filters import *
from stats import *
from globals import *
from tabulate import tabulate

filename = f"{outRepDir}/FIG2.md"
file = open(filename, 'w')

dfTrain = None
dfTest = None
dfWomen = None
dfMen = None
dfWomenNonImp = None
dfWomenImp = None
dfMenNonImp = None
dfMenImp = None

def rfm(height, waist, sex):
    """Compute Relative Fat Mass (RFM)"""
    return 64 - (20 * (height/waist)) + (12 * sex)

def weighted_rmse(y_true, y_pred, sample_weights):
    """Compute weighted RMSE."""
    weighted_sq_errors = sample_weights * ((y_true - y_pred) ** 2)
    return np.sqrt(sum(weighted_sq_errors) / sum(sample_weights))

def compute_metrics(y, y_pred, sample_weights):
    """Compute R^2 and weighted RMSE%."""
    r2 = np.corrcoef(y, y_pred)[0, 1] ** 2
    rmse = weighted_rmse(y, y_pred, sample_weights)
    #rmse_percent = (rmse / np.mean(y)) * 100
    return r2, rmse

def pf2_print(dfMen, dfWomen, filename):

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

    # Body Fat Percentage vs BMI
    men_r2_bmi, men_rmse_bmi = compute_metrics(dfMen[iBodyFatPct], dfMen[iBMICalc], dfMen[iSampleWeight05_06])
    women_r2_bmi, women_rmse_bmi = compute_metrics(dfWomen[iBodyFatPct], dfWomen[iBMICalc], dfWomen[iSampleWeight05_06])
    overall_r2_bmi, overall_rmse_bmi = compute_metrics(pd.concat([dfMen, dfWomen])[iBodyFatPct], pd.concat([dfMen, dfWomen])[iBMICalc], pd.concat([dfMen, dfWomen])[iSampleWeight05_06])

    sns.scatterplot(x=dfMen[iBMICalc], y=dfMen[iBodyFatPct], ax=ax1, color='blue', label=f"Men (R^2: {men_r2_bmi:.2f}; RMSE: {men_rmse_bmi:.2f}%)", alpha=0.5)
    sns.scatterplot(x=dfWomen[iBMICalc], y=dfWomen[iBodyFatPct], ax=ax1, color='red', label=f"Women (R^2: {women_r2_bmi:.2f}; RMSE: {women_rmse_bmi:.2f}%)", alpha=0.5)
    sns.regplot(x=dfMen[iBMICalc], y=dfMen[iBodyFatPct], ax=ax1, color='blue', scatter=False, line_kws={'label':'_nolegend_'})
    sns.regplot(x=dfWomen[iBMICalc], y=dfWomen[iBodyFatPct], ax=ax1, color='red', scatter=False, line_kws={'label':'_nolegend_'})
    sns.regplot(x=pd.concat([dfMen, dfWomen])[iBMICalc], y=pd.concat([dfMen, dfWomen])[iBodyFatPct], ax=ax1, color='gray', scatter=False, label=f"Overall Trend (R^2: {overall_r2_bmi:.2f}; RMSE: {overall_rmse_bmi:.2f}%)")

    ax1.set_title('Body Fat Percentage vs BMI')
    ax1.set_xlabel('BMI')
    ax1.set_ylabel('Body Fat Percentage')
    ax1.legend()
    ax1.set_xlim(0, 80)
    ax1.set_ylim(0, 80)
    ax1.set_xticks(range(0, 81, 20))
    ax1.set_yticks(range(0, 81, 20))

    # Body Fat Percentage vs RFM
    men_r2_rfm, men_rmse_rfm = compute_metrics(dfMen[iBodyFatPct], dfMen['RFM'], dfMen[iSampleWeight05_06])
    women_r2_rfm, women_rmse_rfm = compute_metrics(dfWomen[iBodyFatPct], dfWomen['RFM'], dfWomen[iSampleWeight05_06])
    overall_r2_rfm, overall_rmse_rfm = compute_metrics(pd.concat([dfMen, dfWomen])[iBodyFatPct], pd.concat([dfMen, dfWomen])['RFM'], pd.concat([dfMen, dfWomen])[iSampleWeight05_06])
    
    sns.scatterplot(x=dfMen['RFM'], y=dfMen[iBodyFatPct], ax=ax2, color='blue', label=f"Men (R^2: {men_r2_rfm:.2f}; RMSE: {men_rmse_rfm:.2f}%)", alpha=0.5)
    sns.scatterplot(x=dfWomen['RFM'], y=dfWomen[iBodyFatPct], ax=ax2, color='red', label=f"Women (R^2: {women_r2_rfm:.2f}; RMSE: {women_rmse_rfm:.2f}%)", alpha=0.5)
    sns.regplot(x=dfMen['RFM'], y=dfMen[iBodyFatPct], ax=ax2, color='blue', scatter=False, line_kws={'label':'_nolegend_'})
    sns.regplot(x=dfWomen['RFM'], y=dfWomen[iBodyFatPct], ax=ax2, color='red', scatter=False, line_kws={'label':'_nolegend_'})
    sns.regplot(x=pd.concat([dfMen, dfWomen])['RFM'], y=pd.concat([dfMen, dfWomen])[iBodyFatPct], ax=ax2, color='gray', scatter=False, label=f"Overall Trend (R^2: {overall_r2_rfm:.2f}; RMSE: {overall_rmse_rfm:.2f}%)")

    ax2.set_title('Body Fat Percentage vs RFM')
    ax2.set_xlabel('RFM')
    ax2.set_ylabel('Body Fat Percentage')
    ax2.legend()
    ax2.set_xlim(0, 80)
    ax2.set_ylim(0, 80)
    ax2.set_xticks(range(0, 81, 20))
    ax2.set_yticks(range(0, 81, 20))

    fig.tight_layout(pad=5.0)
    fig.savefig( filename, dpi=300, bbox_inches='tight')

def pf2(dfTe):

    # Exact replication
    file.write("# Replication \n\n")
    dfTest = f_all_paper(dfTe, False)
    dfWomen = f_wom(dfTest)
    dfMen = f_men(dfTest)

    # Calculate RFM
    dfMen['RFM'] = rfm(dfMen[iHeight], dfMen[iWaist], 0)
    dfWomen['RFM'] = rfm(dfWomen[iHeight], dfWomen[iWaist], 1)
    pf2_print(dfWomen, dfMen, f"{outRepDir}/fig2-paper.png")
    file.write("![Paper Replication](fig2-paper.png)")
    file.write("\n\n")

    # Our data
    file.write("# Ours \n\n")
    dfTest = f_all_ours(dfTe, False)
    dfWomen = f_wom(dfTest)
    dfMen = f_men(dfTest)

    # Calculate RFM
    dfMen['RFM'] = rfm(dfMen[iHeight], dfMen[iWaist], 0)
    dfWomen['RFM'] = rfm(dfWomen[iHeight], dfWomen[iWaist], 1)
    pf2_print(dfWomen, dfMen, f"{outRepDir}/fig2-ours.png")
    file.write("![Our Data](fig2-ours.png)")
    file.write("\n\n")
