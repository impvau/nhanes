
from indices import *
import numpy as np
import pandas as pd

dfPbf = None 
dfW = None

def corr_w(df):

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

def corr(df):

    return df.corr(dfPbf)

def gen_wom_fs(df, dfWs, isCw = False):

    c = None
    if isCw:    c = corr_w
    else:       c = corr
    
    global dfPbf
    global dfW
    dfPbf = df[iBodyFatPct]
    dfW = dfWs.iloc[:,0].tolist()

    return [

        # Page 1
        (r"$$\dfrac{h^3}{ab\cdot w}$$",                 c(df[iHeight].pow(3)/(df[iWaist]*df[iWeight]))),
        (r"$$\dfrac{h^2}{ab\cdot \sqrt{w}}$$",          c(df[iHeight].pow(2)/(df[iWaist]*df[iWeight].pow(0.5)))),
        (r"$$\dfrac{h^{2.5}}{ab\cdot w}$$",             c(df[iHeight].pow(2.5)/(df[iWaist]*df[iWeight]))),
        (r"$$\dfrac{h^{2}}{\sqrt{ab}\cdot \sqrt{w}}$$", c(df[iHeight].pow(2)/(df[iWaist]*df[iWeight].pow(0.5)))),
        (r"$$\dfrac{h^{1.5}}{ab\cdot \sqrt{w}}$$",      c(df[iHeight].pow(1.5)/(df[iWaist]*df[iWeight].pow(0.5)))),

        (r"$$\dfrac{h^2}{\sqrt{ab}\cdot w}$$",          c(df[iHeight].pow(2)/(df[iWaist]*df[iWeight]))),
        (r"$$\dfrac{h^{2.5}}{ab\cdot \sqrt{w}}$$",      c(df[iHeight].pow(2.5)/(df[iWaist]*df[iWeight].pow(0.5)))),
        (r"$$\dfrac{h}{\sqrt{a}\cdot ab}$$",            c(df[iHeight]/(df[iArm].pow(0.5)*df[iWaist]))),
        (r"$$\dfrac{h^2}{{ab}^{1.5}\cdot \sqrt{w}}$$",  c(df[iHeight].pow(2)/(df[iWaist].pow(1.5)*df[iWeight].pow(0.5)))),
        (r"$$\dfrac{h^{1.5}}{a\cdot ab}$$",             c(df[iHeight].pow(1.5)/(df[iWaist]*df[iArm]))),

        (r"$$\dfrac{h^2}{ab\cdot w}$$",         c(df[iHeight].pow(2)/(df[iWaist]*df[iWeight]))),
        (r"$$\dfrac{h}{\sqrt{th}\cdot ab}$$",   c(df[iHeight]/(df[iThigh].pow(0.5)*df[iWaist]))),
        (r"$$\dfrac{h}{a\cdot ab}$$",           c(df[iHeight]/(df[iArm]*df[iWaist]))),
        (r"$$\dfrac{h^{2.5}}{w}$$",             c(df[iHeight].pow(2.5)/(df[iWeight]))),
        (r"$$\dfrac{h^{2}}{c\cdot ab}$$",       c(df[iHeight].pow(2)/(df[iArm]*df[iWaist]))),

        (r"$$\dfrac{h^3}{{ab}^2\cdot w}$$",             c(df[iHeight].pow(3)/(df[iWaist].pow(2)*df[iWeight]))),
        (r"$$\dfrac{h}{ab\cdot \sqrt{w}}$$",            c(df[iHeight]/(df[iWaist]*df[iWeight].pow(0.5)))),
        (r"$$\dfrac{h^2}{w}$$",                         c(df[iHeight].pow(2)/(df[iWeight]))),
        (r"$$\dfrac{h^2}{{ab}^2\cdot \sqrt{w}}$$",      c(df[iHeight].pow(2)/(df[iWaist].pow(2)*df[iWeight].pow(0.5)))),
        (r"$$\dfrac{h^2}{{ab}^{1.5}\cdot \sqrt{w}}$$",  c(df[iHeight].pow(2)/(df[iWaist].pow(1.5)*df[iWeight])))

    ]

    #(r"\dfrac{h^3}{\sqrt{ab}*\sqrt{w}}", (df[iHeight].pow(3)/(df[iWaist].pow(0.5)*df[iWeight].pow(0.5))).corr(df[iBodyFatPct])),
    #(r"\dfrac{h^3}{ab*\sqrt{w}}", (df[iHeight].pow(3)/(df[iWaist]*df[iWeight].pow(0.5))).corr(df[iBodyFatPct])),
    #(r"\dfrac{h^3}{w}", (df[iHeight].pow(3)/(df[iWeight])).corr(df[iBodyFatPct])),
    #(r"\dfrac{h}{w}", (df[iHeight]/(df[iWeight].pow(0.5))).corr(df[iBodyFatPct])),
    #(r"\dfrac{h}{a*\sqrt{ab}}", (df[iHeight]/(df[iArm]*df[iWaist].pow(0.5))).corr(df[iBodyFatPct])),
    