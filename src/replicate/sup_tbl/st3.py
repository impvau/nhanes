
from indices import *
from filters import *
from stats import *
from globals import *
from tabulate import tabulate
import numpy as np

filename = f"{outRepDir}/SUP_TABLE3.md"
file = open(filename, 'w')

dfTrain = None
dfTest = None
dfWomen = None
dfMen = None

paper_vals_wom = np.array([
     0,      0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
     0.78,   0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
     0.76,   0.9,   0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
     0.73,   0.92,  0.83,  0,     0,     0,     0,     0,     0,     0,     0,     0,
     0.7,    0.93,  0.88,  0.9,   0,     0,     0,     0,     0,     0,     0,     0,
     0.65,   0.67,  0.58,  0.74,  0.66,  0,     0,     0,     0,     0,     0,     0,
     0.62,   0.84,  0.67,  0.82,  0.88,  0.65,  0,     0,     0,     0,     0,     0,
     0.59,   0.69,  0.63,  0.69,  0.65,  0.7,   0.56,  0,     0,     0,     0,     0,
     0.57,   0.8,   0.65,  0.78,  0.85,  0.58,  0.87,  0.5,   0,     0,     0,     0,
     0.25,   0.35,  0.41,  0.45,  0.55,  0.26,  0.43,  0.23,  0.44,  0,     0,     0,
    -0.11,  -0.02, -0.07,  0.11,  0.32,  0.07,  0.24,  0,     0.28,  0.61,  0,     0,
    -0.11,  -0.05, -0.06,  0.04,  0.18,  0.09,  0.3,   0.02,  0.24,  0.44,  0.63,  0
])

paper_vals_men = np.array([
    0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0,
    0.74, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0,
    0.83, 0.91, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0,
    0.53, 0.87, 0.74, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0,
    0.63, 0.91, 0.88, 0.88, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0,
    0.71, 0.69, 0.68, 0.62, 0.65, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0,
    0.45, 0.81, 0.65, 0.86, 0.86, 0.57, 0.00, 0.00, 0.00, 0.00, 0.00, 0,
    0.62, 0.69, 0.67, 0.59, 0.61, 0.65, 0.50, 0.00, 0.00, 0.00, 0.00, 0,
    0.47, 0.80, 0.68, 0.81, 0.86, 0.54, 0.87, 0.49, 0.00, 0.00, 0.00, 0,
    0.17, 0.28, 0.37, 0.40, 0.54, 0.24, 0.38, 0.19, 0.41, 0.00, 0.00, 0,
   -0.06, 0.05, 0.16, 0.26, 0.46, 0.10, 0.33, 0.02, 0.36, 0.69, 0.00, 0,
   -0.14, 0.01, 0.02, 0.20, 0.29, 0.06, 0.35, 0.02, 0.27, 0.50, 0.67, 0
])

rows = [
    ("Body mass index (BMI)", "kg/m2"),
    ("Waist circumference (WAIST)", "cm"),
    ("Arm circumference (ARMC)", "cm"),
    ("Body weight (BW)", "kg"),
    ("Triceps skinfold (TRI)", "mm"),
    ("Thigh circumference (THIGH)", "cm"),
    ("Subscapular skinfold (SUB)", "mm"),
    ("Calf circumference (CALF)", "cm"),
    ("Arm length (ARML)", "cm"),
    ("Height", "m"),
    ("Leg length", "cm")
]

headers = ["BFP*", "BMI", "WAIST", "ARMC", "BW", "TRI", "THIGH", "SUB", "CALF", "ARML", "Height", ""]

def st3_tbl_rows(matrix):

    new_rows = []  # Create a new list to store the updated rows
    for i, (desc, unit) in enumerate(rows):
        # Adjust the index for the vals DataFrame
        row_idx = i + 1
        if row_idx >= 0 and row_idx < len(matrix):
            # Replace NaN with empty string and format to 2 decimal places
            row_data = ['{:.2f}'.format(val) if not np.isnan(val) else '' for val in matrix.iloc[row_idx].tolist()]
            new_row = [desc, unit] + row_data
        else:
            new_row = [desc, unit] + [''] * (len(headers) - 2)  # Fill with empty strings if no data is available
        new_rows.append(new_row)

    return new_rows

def st3_tbl(df, dfW = None, isSp = False):

    matrix = None
    if dfW is not None:
        if isSp:
            matrix = scorr_w_mat(df, dfW)
        else:
            matrix = corr_w_mat(df, dfW)
    else:
        matrix = df.corr()
        # Default ~ to the pearson piecewise approach on i.e.
        # matrix = df.corr(method='pearson', min_periods=1)

    mask = np.triu(np.ones_like(matrix, dtype=bool))
    matrix[mask] = np.nan

    new_rows = st3_tbl_rows(matrix)

    # Initialize a NumPy array with 12 zeros
    float_data_rows = np.zeros(12)
    for new_row in new_rows:
        # Take the slice from the 3rd element onwards and convert to float
        # Replace empty strings with 0 (since np.nan will be converted to 0 later)
        float_row = [float(value) if value else 0 for value in new_row[2:]]
        # Use numpy.concatenate to add to the NumPy array
        float_data_rows = np.concatenate((float_data_rows, float_row))

    # Convert NaNs to 0, in this case, it might be redundant since you've already replaced empty strings with 0
    float_array = np.nan_to_num(float_data_rows)

    return new_rows, float_array

def st3(dfTr, dfTe):
    
    pd.options.display.float_format = '{:.2f}'.format

    global dfTrain
    global dfTest
    global dfWomen
    global dfMen

    # Heading
    file.write("\n")
    file.write("# Supplimentary Table 3 Replacation\n")
    file.write( "Correlation matrix (unweighted Pearson’s r) between DXA-estimated whole-body fat percentage "
                "and common anthropometrics among adult individuals (≥20 years old) in the training dataset .\n\n")

    # Replication table; Filter according to the paper
    file.write("## Replication\n")
    file.write( "Our attempts to exactly replicate the third table in the suppimentary material. "
                " We could only achieve the precise totals by including the race demographics that "
                " are excluded from the work (r=2, r=5, r=. missing). \n\n"
    )
    
    # Get data based on paper
    dfTrain = f_all_paper(dfTr)
    dfWomen = f_wom(dfTrain)
    dfWomen, dfWomenWeights = f_vars(dfWomen)
    dfMen = f_men(dfTrain)
    dfMen, dfMenWeights = f_vars(dfMen)

    rows_wom, vals_wom  = st3_tbl(dfWomen)
    file.write(tabulate(rows_wom, headers, tablefmt="pipe")+"\n\n")

    rows_men, vals_men  = st3_tbl(dfMen)
    file.write(tabulate(rows_men, headers, tablefmt="pipe")+"\n\n")

    # Diffs to paper 
    file.write("## Diff: Paper-Replication Table")
    file.write( "We observe an error of 0.14 on a value of 0.07, for which we believe there is a "
                " typo in the sign of the correlation. "
                "\n\n"
    )

    wom_diff = paper_vals_wom - vals_wom
    wom_diff = pd.DataFrame(wom_diff.reshape(-1, 12))
    rows_wom_diff = st3_tbl_rows(wom_diff)
    file.write(tabulate(pd.DataFrame(rows_wom_diff), headers, tablefmt="pipe")+"\n\n")

    men_diff = paper_vals_men - vals_men
    men_diff = pd.DataFrame(men_diff.reshape(-1, 12))
    rows_men_diff = st3_tbl_rows(men_diff)
    file.write(tabulate(pd.DataFrame(rows_men_diff), headers, tablefmt="pipe")+"\n\n")
    
    # Replication using the correct data

    file.write("## Replication With Correct demongraphics\n")
    file.write( "Our correlations after excluding (r=2, r=5, r=. missing) "
                "\n\n"
    )
    # Get data based on paper
    dfTrain = f_all_paper(dfTr)
    dfTrain = f_race(dfTrain)
    dfWomen = f_wom(dfTrain)
    dfWomen, dfWomenWeights = f_vars(dfWomen)
    dfMen = f_men(dfTrain)
    dfMen, dfMenWeights = f_vars(dfMen)

    rows_wom, vals_wom  = st3_tbl(dfWomen)
    file.write(tabulate(rows_wom, headers, tablefmt="pipe")+"\n\n")

    rows_men, vals_men  = st3_tbl(dfMen)
    file.write(tabulate(rows_men, headers, tablefmt="pipe")+"\n\n")

    # Diffs to paper 
    file.write("## Diff: Paper-Replication Table")
    file.write( "We observe the correlations are still very close, but there is many more correlations that no longer have zero error "
                "and one observation exceeds the 0.01 uncertainty"
                "\n\n"
    )

    wom_diff = paper_vals_wom - vals_wom
    wom_diff = pd.DataFrame(wom_diff.reshape(-1, 12))
    rows_wom_diff = st3_tbl_rows(wom_diff)
    file.write(tabulate(pd.DataFrame(rows_wom_diff), headers, tablefmt="pipe")+"\n\n")

    men_diff = paper_vals_men - vals_men
    men_diff = pd.DataFrame(men_diff.reshape(-1, 12))
    rows_men_diff = st3_tbl_rows(men_diff)
    file.write(tabulate(pd.DataFrame(rows_men_diff), headers, tablefmt="pipe")+"\n\n")

    # Our Data
    file.write("# Our Data")
    file.write( "We compute wil missing samples filtered "
                "\n\n"
    )

    # Get data based on paper
    dfTrain = f_all_ours(dfTr)
    dfWomen = f_wom(dfTrain)
    dfWomen, dfWomenWeights = f_vars(dfWomen)
    dfMen = f_men(dfTrain)
    dfMen, dfMenWeights = f_vars(dfMen)

    rows_wom, vals_ours_wom  = st3_tbl(dfWomen)
    file.write(tabulate(rows_wom, headers, tablefmt="pipe")+"\n\n")

    rows_men, vals_ours_men  = st3_tbl(dfMen)
    file.write(tabulate(rows_men, headers, tablefmt="pipe")+"\n\n")

    # Diffs to paper 
    file.write("## Diff: Paper-Replication Table")
    file.write( "The difference suggests that there is minor difference to the pairwise approach and simply removing these samples, but it is non-zero (~12% in some cases)"
                "\n\n"
    )

    wom_diff = paper_vals_wom - vals_ours_wom
    wom_diff = pd.DataFrame(wom_diff.reshape(-1, 12))
    rows_wom_diff = st3_tbl_rows(wom_diff)
    file.write(tabulate(pd.DataFrame(rows_wom_diff), headers, tablefmt="pipe")+"\n\n")

    men_diff = paper_vals_men - vals_ours_men
    men_diff = pd.DataFrame(men_diff.reshape(-1, 12))
    rows_men_diff = st3_tbl_rows(men_diff)
    file.write(tabulate(pd.DataFrame(rows_men_diff), headers, tablefmt="pipe")+"\n\n")

    # Using weighted correlations
    file.write("## Weighted correlations Table")
    file.write( ""
                "\n\n"
    )

    # Get data based on paper
    dfTrain = f_all_ours(dfTr)
    dfWomen = f_wom(dfTrain)
    dfWomen, dfWomenWeights = f_vars(dfWomen)
    dfMen = f_men(dfTrain)
    dfMen, dfMenWeights = f_vars(dfMen)

    rows_wom, vals_pcorr_w_wom  = st3_tbl(dfWomen, dfWomenWeights)
    file.write(tabulate(rows_wom, headers, tablefmt="pipe")+"\n\n")

    rows_men, vals_pcorr_w_men  = st3_tbl(dfMen, dfMenWeights)
    file.write(tabulate(rows_men, headers, tablefmt="pipe")+"\n\n")

    # Using weighted correlations
    file.write("## Diff Our Data Unweighted Correlation to Weighted correlations Table")
    file.write( "We observe a further difference within the data when considering weighting of 7%"
                "\n\n"
    )

    wom_diff = vals_ours_wom - vals_pcorr_w_wom
    wom_diff = pd.DataFrame(wom_diff.reshape(-1, 12))
    rows_wom_diff = st3_tbl_rows(wom_diff)
    file.write(tabulate(pd.DataFrame(rows_wom_diff), headers, tablefmt="pipe")+"\n\n")

    men_diff = vals_ours_men - vals_pcorr_w_men
    men_diff = pd.DataFrame(men_diff.reshape(-1, 12))
    rows_men_diff = st3_tbl_rows(men_diff)
    file.write(tabulate(pd.DataFrame(rows_men_diff), headers, tablefmt="pipe")+"\n\n")

    # Using weighted correlations
    file.write("## Spearman correlations Table")
    file.write( ""
                "\n\n"
    )

    # Get data based on paper
    dfTrain = f_all_ours(dfTr)
    dfWomen = f_wom(dfTrain)
    dfWomen, dfWomenWeights = f_vars(dfWomen)
    dfMen = f_men(dfTrain)
    dfMen, dfMenWeights = f_vars(dfMen)

    rows_wom, vals_wom  = st3_tbl(dfWomen, dfWomenWeights, True)
    file.write(tabulate(rows_wom, headers, tablefmt="pipe")+"\n\n")

    rows_men, vals_men  = st3_tbl(dfMen, dfMenWeights, True)
    file.write(tabulate(rows_men, headers, tablefmt="pipe")+"\n\n")

    # Using weighted correlations
    file.write("## Diff Our Weighted Pearson to Our Weighted Spearman \n\n")
    file.write( "Minor differences ~2% observed"
                "\n\n"
    )

    wom_diff = vals_pcorr_w_wom - vals_wom
    wom_diff = pd.DataFrame(wom_diff.reshape(-1, 12))
    rows_wom_diff = st3_tbl_rows(wom_diff)
    file.write(tabulate(pd.DataFrame(rows_wom_diff), headers, tablefmt="pipe")+"\n\n")

    men_diff = vals_pcorr_w_men - vals_men
    men_diff = pd.DataFrame(men_diff.reshape(-1, 12))
    rows_men_diff = st3_tbl_rows(men_diff)
    file.write(tabulate(pd.DataFrame(rows_men_diff), headers, tablefmt="pipe")+"\n\n")

    file.close()

''' Check the manual calculation of the weighted correlation
x = (dfWomen[iHeight].pow(3)/(dfWomen[iWaist]*dfWomen[iWeight])).tolist()
y = (dfWomen[iBodyFatPct]).tolist()
w = (dfWomenWeights).iloc[:, 0].tolist()

# Convert lists to a DataFrame
data = {
    'X': x,
    'Y': y,
    'Weights': w
}
df_to_save = pd.DataFrame(data)

# Write DataFrame to CSV
df_to_save.to_csv('andy_test_comb.csv', index=False)
# Also tried in excel from the raw data
# D1 = SUMPRODUCT(A2:A6263, C2:C6263) / SUM(C2:C6263)
# E1 = SUMPRODUCT(B2:B6263, C2:C6263) / SUM(C2:C6263)
# F1 = SUMPRODUCT(C2:C6263, (A2:A6263-D1), (B2:B6263-E1)) / SUM(C2:C6263)
# G1 = SQRT(SUMPRODUCT(C2:C6263, (A2:A6263-D1)^2) / SUM(C2:C6263))
# H1 = SQRT(SUMPRODUCT(C2:C6263, (B2:B6263-E1)^2) / SUM(C2:C6263))
# I1 = F1 / (G1 * H1)
# Result is -0.852808805
'''

'''
# Calculate weighted means
x_weighted_mean = sum([w_i * x_i for w_i, x_i in zip(w, x)]) / sum(w)
y_weighted_mean = sum([w_i * y_i for w_i, y_i in zip(w, y)]) / sum(w)

# Calculate weighted covariance and variances
cov_weighted = sum([w_i * (x_i - x_weighted_mean) * (y_i - y_weighted_mean) for w_i, x_i, y_i in zip(w, x, y)])
var_x_weighted = sum([w_i * (x_i - x_weighted_mean)**2 for w_i, x_i in zip(w, x)])
var_y_weighted = sum([w_i * (y_i - y_weighted_mean)**2 for w_i, y_i in zip(w, y)])

# Calculate weighted correlation
Rw = cov_weighted / (var_x_weighted * var_y_weighted)**0.5
#print(Rw)  -0.8528088051103047
'''