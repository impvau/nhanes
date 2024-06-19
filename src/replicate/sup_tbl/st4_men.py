
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

def gen_men_fs(df, dfWs, isCw = False):

    c = None
    if isCw:    c = corr
    else:       c = corr_w

    global dfPbf
    global dfW
    dfPbf = df[iBodyFatPct]
    dfW = dfWs.iloc[:,0].tolist()

    # Force a correlation of 1
    dfW = [1 for _ in dfW]

    return [

        # Page 1
        (   r"$$\dfrac{\sqrt{h}}{w}$$",             c(df[iHeight].pow(0.5)/df[iWaist])),
        (   r"$$\dfrac{h}{{ab}^{1.5}}$$",           c(df[iHeight]/df[iWaist].pow(1.5))),
        (   r"$$\dfrac{\sqrt{h}}{\sqrt{w}}$$",      c(df[iHeight].pow(0.5)/df[iWaist].pow(0.5))),
        (   r"$$\dfrac{h}{w}$$",                    c(df[iHeight]/df[iWaist])),
        (   r"$$\dfrac{\sqrt{w}}{\sqrt{h}}$$",      c(df[iWaist].pow(0.5)/(df[iHeight].pow(0.5)))),

        (   r"$$\dfrac{w}{\sqrt{h}}$$",             c(df[iWaist]/df[iHeight].pow(0.5))),
        (   r"$$\dfrac{h}{w^2}$$",                  c(df[iHeight]/df[iWaist].pow(2))),
        (   r"$$\dfrac{w}{h}$$",                    c(df[iWaist]/df[iHeight])),
        (   r"$$\dfrac{w^{1.5}}{h}$$",              c(df[iWaist].pow(1.5)/df[iHeight])),
        (   r"$$\dfrac{h^2}{w^2}$$",                c(df[iHeight].pow(2)/df[iWaist].pow(2))),

        (   r"$$\dfrac{{ab}^2}{h}$$",               c(df[iWaist].pow(2)/(df[iHeight]))),
        (   r"$$\dfrac{w}{{ab}^3}$$",               c(df[iWeight]/(df[iWaist].pow(3)))),
        (   r"$$\dfrac{w}{{ab}^4}$$",               c(df[iWeight]/(df[iWaist].pow(4)))),
        (   r"$$\dfrac{1}{\sqrt{ab}}$$",            c(1/(df[iWaist].pow(0.5)))),
        (   r"$$\dfrac{1}{ab}$$",                   c(1/(df[iWaist]))),

        (   r"$$\dfrac{h}{{ab}^3}$$",                   c(df[iHeight]/(df[iWaist].pow(3)))),
        (   r"$$\sqrt{ab}$$",                           c(df[iWaist].pow(0.5))),
        #(   r"$$\sqrt{ab}$$",                           c(df[iWaist].pow(0.5))),
        (   r"$$\dfrac{h^2}{{ab}^{1.5}*\sqrt{w}}$$",    c(df[iHeight].pow(2)/(df[iWaist].pow(1.5)*df[iWeight].pow(0.5)))),
        (   r"$$\dfrac{h^2}{{ab}^2 * \sqrt{w}}$$",      c(df[iHeight].pow(2)/(df[iWaist].pow(2)*df[iWeight].pow(0.5)))),
        (   r"$$\dfrac{ab^3}{we}$$",                    c(df[iWaist].pow(3)/df[iWeight]))

    ]

    #(   r"$$\dfrac{{ab}^3}{w}$$",                   c(df[iWaist].pow(3)/df[iWeight].pow(0.5))),
    
    #(r"\dfrac{h^{1.5}}{ab}", (df[iHeight].pow(1.5)/(df[iWaist]))),
    #(r"\dfrac{ab}{\sqrt{c}}", (df[iWaist]/(df[iCalf].pow(0.5)))),
    #(r"\dfrac{h^2}{ab * \sqrt{w}}", (df[iHeight].pow(2)/(df[iWaist]*df[iWeight].pow(0.5)))),
    #(r"\dfrac{1}{{ab}^2}", (1/(df[iWaist].pow(2)))),
    #(r"\dfrac{h^{1.5}}{{ab}*\sqrt{w}}", (df[iHeight].pow(1.5)/(df[iWaist]*df[iWeight].pow(0.5)))),
    #("",""),

    # Page 2
    #(r"\dfrac{ab}{h^{1.5}}", (df[iWaist] / df[iHeight].pow(1.5))),
    #(r"\dfrac{h \times c^{0.5} \times ab}{we}", (df[iHeight] * df[iCalf].pow(0.5) * df[iWaist] / df[iWeight])),
    #(r"h^{2.5} \times (ab \times we)^{0.5}", (df[iHeight].pow(2.5) * (df[iWaist] * df[iWeight]).pow(0.5))),
    #(r"ab^2 \times c", (df[iWaist].pow(2) * df[iCalf])),
    #(r"ab^{2} \times we^{0.5}", (df[iWaist].pow(2) * df[iWeight].pow(0.5))),s
    #("",""),
    # Missing 1
    #(r"ab^2", (df[iWaist].pow(2))),
    #(r"\dfrac{ab^2}{t^{0.5}}", (df[iWaist].pow(2) / df[iThigh].pow(0.5))),
    #(r"\dfrac{1}{ab^{3}}", (1 / df[iWaist].pow(3))),
    #(r"\dfrac{ab}{a^{0.5}}", (df[iWaist] / df[iArm].pow(0.5))),
    #("",""),
    #(r"\dfrac{h}{ab^4}", (df[iHeight] / df[iWaist].pow(4))),
    #(r"\dfrac{h \times (ab \times we)^{0.5}}{ab}", (df[iHeight] * (df[iWaist] * df[iWeight]).pow(0.5) / df[iWaist])),
    #(r"\dfrac{h \times (a^{0.5} \times ab)}{we}", (df[iHeight] * df[iArm].pow(0.5) * df[iWaist] / df[iWeight])),
    #(r"h \times t", (df[iHeight] * df[iThigh])),
    #(r"\dfrac{h \times (t^{0.5} \times ab)}{we}", (df[iHeight] * df[iThigh].pow(0.5) * df[iWaist] / df[iWeight])),
    #("",""),
    #(r"\dfrac{ab^{2.5}}{we}", (df[iWaist].pow(2.5) / df[iWeight])),
    #(r"h^3 \times (ab \times we)^{0.5}", (df[iHeight].pow(3) * (df[iWaist] * df[iWeight]).pow(0.5))),
    #(r"\dfrac{ab^3}{a}", (df[iWaist].pow(3) / df[iArm])),
    #(r"\dfrac{h^2 \times (c^{0.5} \times ab)}{we}", (df[iHeight].pow(2) * df[iCalf].pow(0.5) * df[iWaist] / df[iWeight])),
    #(r"\dfrac{h^2 \times (ab^{0.5} \times we^{0.5})}{ab}", (df[iHeight].pow(2) * df[iWaist].pow(0.5) * df[iWeight].pow(0.5) / df[iWaist])),
    #("",""),
    #(r"h^3 \times (ab \times we)", (df[iHeight].pow(3) * (df[iWaist] * df[iWeight]))),
    #(r"ab^3", (df[iWaist].pow(3))),
    #(r"\dfrac{h^2 \times (b \times ab)}{we}", (df[iHeight].pow(2) * df[iTricep] * df[iWaist] / df[iWeight])),
    #(r"ab^{1.5}", (df[iWaist].pow(1.5))),
    #(r"\dfrac{h^2 \times (a^{0.5} \times ab)}{we}", (df[iHeight].pow(2) * df[iArm].pow(0.5) * df[iWaist] / df[iWeight]))
    #("",""),