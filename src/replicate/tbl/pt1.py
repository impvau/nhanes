

from indices import *
from filters import *
from stats import *
from globals import *
from tabulate import tabulate

filename = f"{outRepDir}/TABLE1.md"
file = open(filename, 'w')

dfTrain = None
dfTest = None
dfWomenTrain = None
dfWomenTest = None
dfMenTrain = None
dfMenTest = None

# Note age is shifted down slightly
paper_vals = [ 
        6261,6320,1700,1756,
        6.4,8,7.3,9.5,
        71.7,72.2,69.7,71.2,
        11.3,9.9,12.4,10.8,
        47.2,45,43.3,42.1,
        36.6,41.3,39.7,44.1,
        39.1,39.1,46.9,43.9,
        24.2,19.7,13.4,12.1,
        2.5,1.2,2.2,1.2,
        35.8,30,36.6,25.4,
        28.8,40.9,24.8,39.6,
        32.9,28,36.4,33.8,
        74.1,86.8,75.8,89.5,
        162.2,176.2,162.6,176.6,
        28.2,27.9,28.7,28.6,
        93.1,99.5,93.9,100.8,
        30.8,25.3,31.2,26,
        41.9,59.5,43.1,61.6,
        39.9,28,39.4,27.8,
        38.2,29.1,37.5,28.8 
    ]

headers = ["", "NHANES 1999-2004", "(Train data)", "NHANES 2005-2006", "(Test dataset)"]
    
def pt1_samples():

    rows = [
        "",
        f"N={df_cnt(dfWomenTrain)} ({pct_w(dfWomenTrain,dfTrain,0)})",
        f"N={df_cnt(dfMenTrain)} ({pct_w(dfMenTrain,dfTrain,0)})",
        f"N={df_cnt(dfWomenTest)} ({pct_w(dfWomenTest,dfTest,0)})",
        f"N={df_cnt(dfMenTest)} ({pct_w(dfMenTest,dfTest,0)})"
    ]
    our_vals = [
        df_cnt(dfWomenTrain),
        df_cnt(dfMenTrain),
        df_cnt(dfWomenTest),
        df_cnt(dfMenTest)
    ]

    return rows, our_vals

def pt1_race_pct():

    # Ethnicity data collection
    ethnicities = [
        ("Mexican-American", f_mex),
        ("European-American", f_eur),
        ("African-American", f_afr)  # Assuming this label is correct given the function name
    ]

    rows = []
    our_vals = []
    for ethnicity, func in ethnicities:

        dfWomenTrainEth, dfWomenTestEth = func(dfWomenTrain), func(dfWomenTest)
        dfMenTrainEth, dfMenTestEth = func(dfMenTrain), func(dfMenTest)

        rows.append([
            f"{ethnicity} %",
            f"{pct_w(dfWomenTrainEth, dfWomenTrain)}",
            f"{pct_w(dfMenTrainEth, dfMenTrain)}",
            f"{pct_w(dfWomenTestEth, dfWomenTest)}",
            f"{pct_w(dfMenTestEth, dfMenTest)}"
        ])
    
        our_vals.extend([pct_w(dfWomenTrainEth, dfWomenTrain),pct_w(dfMenTrainEth, dfMenTrain),pct_w(dfWomenTestEth, dfWomenTest),pct_w(dfMenTestEth, dfMenTest)])

    return rows, our_vals

def pt1_age_pct():

    rows = []
    our_vals = []

    # Age data
    rows.append([
        "Age Yr",
        f"{avg_w(dfWomenTrain, iAge)}",
        f"{avg_w(dfMenTrain, iAge)}",
        f"{avg_w(dfWomenTest, iAge)}",
        f"{avg_w(dfMenTest, iAge)}"
    ])
    our_vals.extend([avg_w(dfWomenTrain, iAge),avg_w(dfMenTrain, iAge),avg_w(dfWomenTest, iAge),avg_w(dfMenTest, iAge)])

    # Age Category data collection
    age_categories = [
        ("20-39 years old", f_age_y),
        ("40-59 years old", f_age_m),  # This seems to be a duplicate label. Consider updating.
        (">=60 years old", f_age_a)
    ]

    for age_label, age_func in age_categories:

        dfWomenTrainAge, dfWomenTestAge = age_func(dfWomenTrain), age_func(dfWomenTest)
        dfMenTrainAge, dfMenTestAge = age_func(dfMenTrain), age_func(dfMenTest)

        rows.append([
            f"{age_label} %",
            f"{pct_w(dfWomenTrainAge, dfWomenTrain)}",
            f"{pct_w(dfMenTrainAge, dfMenTrain)}",
            f"{pct_w(dfWomenTestAge, dfWomenTest)}",
            f"{pct_w(dfMenTestAge, dfMenTest)}"
        ])
        our_vals.extend([pct_w(dfWomenTrainAge, dfWomenTrain),pct_w(dfMenTrainAge, dfMenTrain),pct_w(dfWomenTestAge, dfWomenTest),pct_w(dfMenTestAge, dfMenTest)])
        
    return rows, our_vals

def pt1_bmi_pct():

    rows = []
    our_vals = []

    # BMI Category data collection
    bmi_categories = [
        ("<18.5", f_bmi_u),
        ("18.5-24.9", f_bmi_n),
        ("25-29.9", f_bmi_o),
        ("≥30", f_bmi_ob)
    ]

    for bmi_label, bmi_func in bmi_categories:
        dfWomenTrainBMI, dfWomenTestBMI = bmi_func(dfWomenTrain), bmi_func(dfWomenTest)
        dfMenTrainBMI, dfMenTestBMI = bmi_func(dfMenTrain), bmi_func(dfMenTest)

        rows.append([
            f"{bmi_label} %",
            f"{pct_w(dfWomenTrainBMI, dfWomenTrain)}",
            f"{pct_w(dfMenTrainBMI, dfMenTrain)}",
            f"{pct_w(dfWomenTestBMI, dfWomenTest)}",
            f"{pct_w(dfMenTestBMI, dfMenTest)}"
        ])
        our_vals.extend([pct_w(dfWomenTrainBMI, dfWomenTrain),pct_w(dfMenTrainBMI, dfMenTrain),pct_w(dfWomenTestBMI, dfWomenTest),pct_w(dfMenTestBMI, dfMenTest)])

    return rows, our_vals

def pt1_avg_w():

    indices = [
        ("Weight kg", iWeight),
        ("Height", iHeight),
        ("BMI", iBMI),
        ("Waist Circumference", iWaist),
        ("Whole-body fat mass", iBodyFat),
        ("Whole-body fat free mass", iFatFreeMass),
        ("Whole-body fat percentage", iBodyFatPct),
        ("Trunk fat percentage", iTrunkFatPct)
    ]

    rows = []
    our_vals = []

    for desc, index in indices:
        calculated_vals = [
            avg_w(dfWomenTrain, index),
            avg_w(dfMenTrain, index),
            avg_w(dfWomenTest, index),
            avg_w(dfMenTest, index)
        ]
        
        row = [desc] + [f"{val}" for val in calculated_vals]
        rows.append(row)
        our_vals.extend(calculated_vals)

    return rows, our_vals

def pt1_tbl():

    # Replicate table
    rows = []
    rows.append(["", "Women", "Men", "Women", "Men"])
    rows.append(pt1_samples()[0])
    rows.extend(pt1_race_pct()[0])
    rows.extend(pt1_age_pct()[0])
    rows.extend(pt1_bmi_pct()[0])
    rows.extend(pt1_avg_w()[0])
    file.write(tabulate(rows, headers, tablefmt='github'))
    file.write("\n\n\n")

    vals = []   
    vals.extend(pt1_samples()[1])
    vals.extend(pt1_race_pct()[1])
    vals.extend(pt1_age_pct()[1])
    vals.extend(pt1_bmi_pct()[1])
    vals.extend(pt1_avg_w()[1])

    return vals

def pt1_tbl_from_vals(paper_vals, our_vals):

    # Determine diffs
    diff_vals = [paper - our for paper, our in zip(paper_vals, our_vals)]
    diff_vals = [round(value, 2) for value in diff_vals]

    # Generate diffs    
    rows = [
        ["", "Women", "Men", "Women", "Men"],
        ["", f"N={diff_vals[0]} ({rnd(diff_vals[0]/paper_vals[0]*100,1)})", f"N={diff_vals[1]}  ({rnd(diff_vals[1]/paper_vals[1]*100,1)})", f"N={diff_vals[2]}  ({rnd(diff_vals[2]/paper_vals[2]*100,1)})", f"N={diff_vals[3]} ({rnd(diff_vals[3]/paper_vals[3]*100,1)})"],
        ["Age Yr"] + diff_vals[4:8],
        ["Mexican-American %"] + diff_vals[8:12],
        ["European-American %"] + diff_vals[12:16],
        ["African-American %"] + diff_vals[16:20],
        ["20-39 years old %"] + diff_vals[20:24],
        ["40-59 years old %"] + diff_vals[24:28],
        [">=60 years old %"] + diff_vals[28:32],
        ["<18.5 %"] + diff_vals[32:36],
        ["18.5-24.9 %"] + diff_vals[36:40],
        ["25-29.9 %"] + diff_vals[40:44],
        [">=30 %"] + diff_vals[44:48],
        ["Weight kg"] + diff_vals[48:52],
        ["Height"] + diff_vals[52:56],
        ["BMI"] + diff_vals[56:60],
        ["Waist Circumference"] + diff_vals[60:64],
        ["Whole-body fat mass"] + diff_vals[64:68],
        ["Whole-body fat free mass"] + diff_vals[68:72],
        ["Whole-body fat percentage"] + diff_vals[72:76],
        ["Trunk fat percentage"] + diff_vals[76:80]
    ]

    file.write(tabulate(rows, headers, tablefmt="github"))    
    file.write("\n")

def pt1(dfTr, dfTe):
        
    global dfTrain
    global dfTest
    global dfWomenTrain
    global dfWomenTest
    global dfMenTrain
    global dfMenTest

    # Heading
    file.write("\n")
    file.write("# Table 1 Replacation\n")
    file.write("The figure provides charateristics of adult individuals (≥20 years old) included in the study"
               " using pooled weighted mean estimates (or percentages). The authors warn 'percentages may not "
               "total 100 due to rounding'.\n\n")

    # Replication table; Filter according to the paper
    file.write("## Replication\n")
    file.write("Our attempts to exactly replicate the first table in Woolcots paper. We could only achieve the precise totals by including the race demographics that are excluded from the work (r=2, r=5, r=. missing). \n\n")
    dfTrain = f_all_paper(dfTr)
    dfTest = f_all_paper(dfTe, False)
    dfWomenTrain, dfWomenTest = f_wom(dfTrain), f_wom(dfTest)
    dfMenTrain, dfMenTest = f_men(dfTrain), f_men(dfTest)
    vals = pt1_tbl()
    file.write("\n")

    # Diff table
    file.write("## Diff: Paper-Replication Table\n")
    file.write( "We see no difference in replication, although we incorrecly include certain race types. "
                "There are no weights and simply total the values. The case that we are in error would require "
                "our preliminary fitlering to be incorrect, and those errors still result it the precise decifit we observe "
                "when including r=2, r=5 and r=. missing \n\n")
    pt1_tbl_from_vals(paper_vals, vals)
    file.write("\n")

    # Removing Other Races
    file.write("## Table 1 Limiting to r=1, r=3, r=5\n")
    file.write("We now consider the totals when only the Mex-Am (r=1), Eur-Am (r=3) and Afr-Am (r=4) are included. We believe this is what the authors meant to based their work on, and it is uncertain if the incorrect dataset was used throughout their work. \n\n")
    dfTrain = f_all_paper(dfTr)
    dfTrain = f_race(dfTrain)
    dfTest = f_all_paper(dfTe, False)
    dfTest = f_race(dfTest)
    dfWomenTrain, dfWomenTest = f_wom(dfTrain), f_wom(dfTest)
    dfMenTrain, dfMenTest = f_men(dfTrain), f_men(dfTest)
    vals_race = pt1_tbl()

    # Diff table
    file.write("## Diff: Paper-Race Limited Table\n")
    file.write("We observe an average percentage reduction of around 18% of the data when we limit race to the expected categories: r=2, r=5 and r=. missing \n\n")
    pt1_tbl_from_vals(paper_vals, vals_race)
    file.write("\n")

    # Removing NAs
    file.write("## Table 1 Removing NaNs\n")
    file.write(f"We remove NaNs from the columns {','.join(iConsider)}. We do this to avoid any potential issues in correlation from missing values. \n\n")
    dfTrain = f_all_paper(dfTr)
    dfTest = f_all_paper(dfTe, False)
    dfTrain = dfTrain.dropna(subset=iConsider, axis=0)
    dfTest = dfTest.dropna(subset=iConsider, axis=0)
    dfWomenTrain, dfWomenTest = f_wom(dfTrain), f_wom(dfTest)
    dfMenTrain, dfMenTest = f_men(dfTrain), f_men(dfTest)
    nas_race = pt1_tbl()

    # Diff table
    file.write("## Diff: Paper-NaNs Table\n")
    file.write(f"We have a loss of around 25% when we remove NaNs from the mentioned columns \n\n")
    pt1_tbl_from_vals(paper_vals, nas_race)
    file.write("\n")

    # Our Data
    file.write("# Our Data\n")
    file.write("We correctly limits race codes and removes NaNs, resulting in the following data \n\n")
    dfTrain = f_all_ours(dfTr)
    dfTest = f_all_ours(dfTe, False)
    dfWomenTrain, dfWomenTest = f_wom(dfTrain), f_wom(dfTest)
    dfMenTrain, dfMenTest = f_men(dfTrain), f_men(dfTest)
    vals_ours = pt1_tbl()
    file.write("\n")

    # Diff table
    file.write("## Diff: Paper-Our Table\n")
    file.write("We observe an average reduction percent of around 31-32% across the categories in comparison original paper. We see a large reduction in ther percentage of Mex-Am race category. Within the BMI ranges our precentages decrease for smaller weight categories while the percentage obese significantly increases. This may suggest that measurements of obese  patients is far more common than in other weight categories. The average values for the whole-body fat increase naturally with the higher percentage of obsese samples. \n\n")
    pt1_tbl_from_vals(paper_vals, vals_ours)
    file.write("\n")

    file.close()
