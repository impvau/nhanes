import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import nhanes_funcs as nh

def rfm(height, waist, sex):
    """Compute Relative Fat Mass (RFM)"""
    return 64 - (20 * (height/waist)) + (12 * sex)


#def weighted_rmse(y_true, y_pred, sample_weights):
#    """Compute weighted RMSE."""
#    weighted_sq_error = np.sum(sample_weights * ((y_true - y_pred) ** 2)) / np.sum(sample_weights)
#    return np.sqrt(weighted_sq_error)

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

def pf2():
    dfTest = nh.build_data()[1].copy()
    dfTest = nh.df_mean(dfTest, dfTest)[1].copy()
    dfWomenTest = nh.f_wom(dfTest, dfTest)[1].copy()
    dfMenTest = nh.f_men(dfTest, dfTest)[1].copy()

    # Calculate RFM
    dfMenTest['RFM'] = rfm(dfMenTest[nh.iHeight], dfMenTest[nh.iWaist], 0)
    dfWomenTest['RFM'] = rfm(dfWomenTest[nh.iHeight], dfWomenTest[nh.iWaist], 1)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

    # Body Fat Percentage vs BMI
    men_r2_bmi, men_rmse_bmi = compute_metrics(dfMenTest[nh.iBodyFatPct], dfMenTest[nh.iBMICalc], dfMenTest[nh.iSampleWeight05_06])
    women_r2_bmi, women_rmse_bmi = compute_metrics(dfWomenTest[nh.iBodyFatPct], dfWomenTest[nh.iBMICalc], dfWomenTest[nh.iSampleWeight05_06])
    overall_r2_bmi, overall_rmse_bmi = compute_metrics(pd.concat([dfMenTest, dfWomenTest])[nh.iBodyFatPct], pd.concat([dfMenTest, dfWomenTest])[nh.iBMICalc], pd.concat([dfMenTest, dfWomenTest])[nh.iSampleWeight05_06])

    sns.scatterplot(x=dfMenTest[nh.iBMICalc], y=dfMenTest[nh.iBodyFatPct], ax=ax1, color='blue', label=f"Men (R^2: {men_r2_bmi:.2f}; RMSE: {men_rmse_bmi:.2f}%)", alpha=0.5)
    sns.scatterplot(x=dfWomenTest[nh.iBMICalc], y=dfWomenTest[nh.iBodyFatPct], ax=ax1, color='red', label=f"Women (R^2: {women_r2_bmi:.2f}; RMSE: {women_rmse_bmi:.2f}%)", alpha=0.5)
    sns.regplot(x=dfMenTest[nh.iBMICalc], y=dfMenTest[nh.iBodyFatPct], ax=ax1, color='blue', scatter=False, line_kws={'label':'_nolegend_'})
    sns.regplot(x=dfWomenTest[nh.iBMICalc], y=dfWomenTest[nh.iBodyFatPct], ax=ax1, color='red', scatter=False, line_kws={'label':'_nolegend_'})
    sns.regplot(x=pd.concat([dfMenTest, dfWomenTest])[nh.iBMICalc], y=pd.concat([dfMenTest, dfWomenTest])[nh.iBodyFatPct], ax=ax1, color='gray', scatter=False, label=f"Overall Trend (R^2: {overall_r2_bmi:.2f}; RMSE: {overall_rmse_bmi:.2f}%)")

    ax1.set_title('Body Fat Percentage vs BMI')
    ax1.set_xlabel('BMI')
    ax1.set_ylabel('Body Fat Percentage')
    ax1.legend()
    ax1.set_xlim(0, 80)
    ax1.set_ylim(0, 80)
    ax1.set_xticks(range(0, 81, 20))
    ax1.set_yticks(range(0, 81, 20))

    # Body Fat Percentage vs RFM
    men_r2_rfm, men_rmse_rfm = compute_metrics(dfMenTest[nh.iBodyFatPct], dfMenTest['RFM'], dfMenTest[nh.iSampleWeight05_06])
    women_r2_rfm, women_rmse_rfm = compute_metrics(dfWomenTest[nh.iBodyFatPct], dfWomenTest['RFM'], dfWomenTest[nh.iSampleWeight05_06])
    overall_r2_rfm, overall_rmse_rfm = compute_metrics(pd.concat([dfMenTest, dfWomenTest])[nh.iBodyFatPct], pd.concat([dfMenTest, dfWomenTest])['RFM'], pd.concat([dfMenTest, dfWomenTest])[nh.iSampleWeight05_06])
    
    sns.scatterplot(x=dfMenTest['RFM'], y=dfMenTest[nh.iBodyFatPct], ax=ax2, color='blue', label=f"Men (R^2: {men_r2_rfm:.2f}; RMSE: {men_rmse_rfm:.2f}%)", alpha=0.5)
    sns.scatterplot(x=dfWomenTest['RFM'], y=dfWomenTest[nh.iBodyFatPct], ax=ax2, color='red', label=f"Women (R^2: {women_r2_rfm:.2f}; RMSE: {women_rmse_rfm:.2f}%)", alpha=0.5)
    sns.regplot(x=dfMenTest['RFM'], y=dfMenTest[nh.iBodyFatPct], ax=ax2, color='blue', scatter=False, line_kws={'label':'_nolegend_'})
    sns.regplot(x=dfWomenTest['RFM'], y=dfWomenTest[nh.iBodyFatPct], ax=ax2, color='red', scatter=False, line_kws={'label':'_nolegend_'})
    sns.regplot(x=pd.concat([dfMenTest, dfWomenTest])['RFM'], y=pd.concat([dfMenTest, dfWomenTest])[nh.iBodyFatPct], ax=ax2, color='gray', scatter=False, label=f"Overall Trend (R^2: {overall_r2_rfm:.2f}; RMSE: {overall_rmse_rfm:.2f}%)")

    ax2.set_title('Body Fat Percentage vs RFM')
    ax2.set_xlabel('RFM')
    ax2.set_ylabel('Body Fat Percentage')
    ax2.legend()
    ax2.set_xlim(0, 80)
    ax2.set_ylim(0, 80)
    ax2.set_xticks(range(0, 81, 20))
    ax2.set_yticks(range(0, 81, 20))

    fig.tight_layout(pad=5.0)
    fig.savefig('fig2.png', dpi=300, bbox_inches='tight')
