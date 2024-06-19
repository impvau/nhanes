
from indices import *
from filters import *
from stats import *
from globals import *
from tabulate import tabulate

from .st4_men import *
from .st4_wom import *

filename = f"{outRepDir}/SUP_TABLE4.md"
file = open(filename, 'w')

dfTrain = None
dfTest = None
dfWomen = None
dfMen = None

expected = [
    -0.8073, -0.8481,
    -0.8045, -0.8472,
    -0.8042, -0.8459,
    -0.8031, -0.8448,
    -0.8018,  0.8428,

    -0.7999,  0.8424,
    -0.7999, -0.841,
    -0.798,   0.8386,
    -0.798,   0.8384,
    -0.7976, -0.8377,

    -0.7969,  0.8292,
    -0.7955, -0.8278,
    -0.7951, -0.8274,
    -0.7949, -0.8252,
    -0.7945, -0.824,

    -0.7925, -0.8228,
    -0.7913,  0.8224,
    -0.7899, -0.8222,
    -0.7898, -0.8193,
    -0.7898, 0.8192
]

'''
    -0.7896,  0.8182,
    -0.7891, -0.8172,
    -0.789,  0.8167,
    -0.788, -0.8142,
    -0.7876,  0.8142,

    -0.7888,  0.8139,
    -0.7876,  0.8137,
    -0.7875,  0.8132
]
'''

def round_correlation_values(formulas, decimal_places=4):
    rounded_formulas = []
    for formula, correlation in formulas:
        if formula and correlation != "":
            rounded_correlation = round(correlation, decimal_places)
        else:
            rounded_correlation = correlation
        rounded_formulas.append((formula, rounded_correlation))
    return rounded_formulas

def st4_tbl(form_wom, form_men):

    rows = []
    for idx, (men_formula, women_formula) in enumerate(zip(form_men, form_wom)):
        rows.append([women_formula[0], women_formula[1], men_formula[0], men_formula[1]])

        # Append an empty row every 5 elements
        if (idx + 1) % 5 == 0:
            rows.append(['', '', '', ''])

    return rows

def st4_tbl_diff(form_wom, form_men, vals):

    rows = []
    idx = 0  # Counter for vals array
    for zip_idx, (men_formula, women_formula) in enumerate(zip(form_men, form_wom)):

        #print(f"{women_formula[0]}: {float(women_formula[1])}-{vals[idx]}, {men_formula[0]}: {float(men_formula[1])}-{vals[idx+1]}, ")
        # Subtracting the values from vals for the respective indices
        women_value = float(women_formula[1]) - vals[idx]
        men_value = float(men_formula[1]) - vals[idx + 1]

        rows.append([women_formula[0], rnd(women_value,4), men_formula[0], rnd(men_value,4)])

        # Append an empty row every 5 elements
        if (zip_idx + 1) % 5 == 0:
            rows.append(['', '', '', ''])

        idx += 2  # Increment the counter by 2 for the next pair of values

    #print(vals)
    return rows

def st4(dfTr, dfTe):

    pd.options.display.float_format = '{:.2f}'.format
    decimal_places = 4

    global dfTrain
    global dfTest
    global dfWomen
    global dfMen
   
    dfTrain = f_all_paper(dfTr)
    #dfTrain = dfTrain.dropna(subset=iConsider, axis=0)
    dfWomen = f_wom(dfTrain)
    dfWomen, dfWomenWeights = f_vars(dfWomen)
    dfMen = f_men(dfTrain)
    dfMen, dfMenWeights = f_vars(dfMen)

    table_data = []
    table_headers = ["Formula (Women)", "Correlation (Women)", "Formula (Men)", "Correlation (Men)"]
    table_headers_diff = ["Formula (Women)", "Correlation Diff (Women)", "Formula (Men)", "Correlation Diff (Men)"]

    # Replication of table
    file.write("\n")
    file.write("# Supplimentary Table 4 Replacation\n")
    file.write( "We attempt to reproduce the 'Correlation matrix (unweighted Pearson’s r) between"
                " DXA-estimated whole-body fat percentage and more than 350 indices derived using"
                " common anthropometrics among adult individuals (≥20 years old) in the development"
                " dataset.' We are unable to reproduce this data, even though our correlation matrix"
                " near identical. In an attempt to replicate the values the authors have determined "
                " we have tried using the weighted correlation, remove the race categories incorrectly "
                " left in the datasets, and a number of other attempts but have been unsuccessful in "
                " replicating the published correlations. \n")
    
    file.write("\n\n")

    # Extract men correlations
    formulas_men = gen_men_fs(dfMen, dfMenWeights)
    max_len = len(formulas_men)
    formulas_men = round_correlation_values(formulas_men, decimal_places)
    formulas_men.extend([("", "")] * (max_len - len(formulas_men)))

    # Extract women correlations
    formulas_wom = gen_wom_fs(dfWomen, dfWomenWeights)
    formulas_wom = round_correlation_values(formulas_wom, decimal_places)
    formulas_wom.extend([("", "")] * (max_len - len(formulas_wom)))
    
    ### Reproduce table
    file.write(tabulate(st4_tbl(formulas_wom, formulas_men), headers=table_headers, tablefmt="pipe"))
    file.write("\n\n")

    # Diff reproduction to ours
    file.write("# Diff Supplimentary Table 4 Paper-Replicated\n")
    file.write(tabulate(st4_tbl_diff(formulas_wom, formulas_men, expected[:40]), headers=table_headers_diff, tablefmt="pipe"))
    file.write("\n\n")

    ### Reproduce by with weighted correlation
    # Extract men correlations
    formulas_men_w = gen_men_fs(dfMen, dfMenWeights, True)
    max_len = len(formulas_men_w)
    formulas_men_w = round_correlation_values(formulas_men_w, decimal_places)
    formulas_men_w.extend([("", "")] * (max_len - len(formulas_men_w)))
    # Extract women correlations
    formulas_wom_w = gen_wom_fs(dfWomen, dfWomenWeights, True)
    formulas_wom_w = round_correlation_values(formulas_wom_w, decimal_places)
    formulas_wom_w.extend([("", "")] * (max_len - len(formulas_wom_w)))
    # Weighted Table
    file.write("# Weighted Correlation Table\n")
    file.write(tabulate(st4_tbl(formulas_wom_w, formulas_men_w), headers=table_headers, tablefmt="pipe"))
    file.write("\n\n")
    # Diff Weighted Tabl
    file.write("# Diff Supplimentary Table 4 Paper-Replicated\n")
    file.write(tabulate(st4_tbl_diff(formulas_wom_w, formulas_men_w, expected[:40]), headers=table_headers_diff, tablefmt="pipe"))
    file.write("\n\n")

    ### Reproduce by with weighted correlation
    dfTrain = f_all_ours(dfTr)
    dfWomen = f_wom(dfTrain)
    dfWomen, dfWomenWeights = f_vars(dfWomen)
    dfMen = f_men(dfTrain)
    dfMen, dfMenWeights = f_vars(dfMen)
    # Extract men correlations
    formulas_men_w = gen_men_fs(dfMen, dfMenWeights, True)
    max_len = len(formulas_men_w)
    formulas_men_w = round_correlation_values(formulas_men_w, decimal_places)
    formulas_men_w.extend([("", "")] * (max_len - len(formulas_men_w)))
    # Extract women correlations
    formulas_wom_w = gen_wom_fs(dfWomen, dfWomenWeights, True)
    formulas_wom_w = round_correlation_values(formulas_wom_w, decimal_places)
    formulas_wom_w.extend([("", "")] * (max_len - len(formulas_wom_w)))
    # Weighted Table
    file.write("# Weighted Correlation Table With Our Data\n")
    file.write(tabulate(st4_tbl(formulas_wom_w, formulas_men_w), headers=table_headers, tablefmt="pipe"))
    file.write("\n\n")
    # Diff Weighted Tabl
    file.write("# Diff Supplimentary Table 4 Paper-Replicated\n")
    file.write(tabulate(st4_tbl_diff(formulas_wom_w, formulas_men_w, expected[:40]), headers=table_headers_diff, tablefmt="pipe"))
    file.write("\n\n")

    file.close()
