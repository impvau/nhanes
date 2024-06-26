
from indices import *
from filters import *
from stats import *
from globals import *
from tabulate import tabulate

filename = f"{outRepDir}/SUP_TABLE1.md"
file = open(filename, 'w')

dfTrain = None
dfTest = None
dfWomen = None
dfMen = None
dfWomenNonImp = None
dfWomenImp = None
dfMenNonImp = None
dfMenImp = None

# Note age is shifted down slightly
paper_vals = [ 
    4829, 77.1, 1432, 22.9, 6261, 5065, 80.1, 1255, 19.9, 6320,
    1122, 80.2, 277, 19.8, 1399, 1208, 83.9, 231, 16.1, 1439,
    2432, 78.3, 675, 21.7, 3107, 2527, 79.1, 667, 20.9, 3194,
    865, 69.5, 379, 30.5, 1244, 922, 76.7, 280, 23.3, 1202,
    1600, 80.4, 389, 19.6, 1989, 1835, 86.2, 295, 13.8, 2130,
    1580, 79.1, 418, 20.9, 1998, 1595, 80.7, 381, 19.3, 1976,
    1649, 72.5, 625, 27.5, 2274, 1635, 73.8, 579, 26.2, 2214,
    102, 84.3, 19, 15.7, 121, 67, 80.7, 16, 19.3, 83,
    1643, 83.1, 333, 16.9, 1976, 1606, 85.2, 280, 14.8, 1886,
    1567, 81.8, 349, 18.2, 1916, 2244, 85.5, 380, 14.5, 2624,
    1517, 67.5, 731, 32.5, 2248, 1148, 66.5, 579, 33.5, 1727
]

headers = ["", "Non-imputed data (%)", "Imputed data (%)", "Total", "Non-imputed data (%)", "Imputed data (%)", "Total"]
    
def st1_samples():

    rows = [
        "",
        f"N={df_cnt(dfWomenNonImp)} ({pct(dfWomenNonImp,dfTrain,1)})",
        f"N={df_cnt(dfWomenImp)} ({pct(dfWomenImp,dfTrain,1)})",
        f"N={df_cnt(dfWomenNonImp)+df_cnt(dfWomenImp)}",
        f"N={df_cnt(dfMenNonImp)} ({pct(dfMenNonImp,dfTrain,1)})",
        f"N={df_cnt(dfMenImp)} ({pct(dfMenImp,dfTrain,1)})",
        f"N={df_cnt(dfMenNonImp)+df_cnt(dfMenImp)}"
    ]
    our_vals = [
        df_cnt(dfWomenNonImp),
        pct(dfWomenNonImp,dfWomen,1),
        df_cnt(dfWomenImp),
        pct(dfWomenImp,dfWomen,1),
        df_cnt(dfWomenNonImp)+df_cnt(dfWomenImp),

        df_cnt(dfMenNonImp),
        pct(dfMenNonImp,dfMen,1),
        df_cnt(dfMenImp),
        pct(dfMenImp,dfMen,1),
        df_cnt(dfMenNonImp)+df_cnt(dfMenImp)
    ]

    return rows, our_vals

def st1_race_pct():

    # Ethnicity data collection
    ethnicities = [
        ("Mexican-American", f_mex),
        ("European-American", f_eur),
        ("African-American", f_afr)  # Assuming this label is correct given the function name
    ]

    rows = []
    our_vals = []
    for ethnicity, func in ethnicities:

        dfWomenNonImpEth, dfWomenImpEth = func(dfWomenNonImp), func(dfWomenImp)
        dfMenNonImpEth, dfMenImpEth = func(dfMenNonImp), func(dfMenImp)

        rows.append([
            f"{ethnicity} %",
            f"{df_cnt(dfWomenNonImpEth)} ({rnd(100*df_cnt(dfWomenNonImpEth)/(df_cnt(dfWomenNonImpEth)+df_cnt(dfWomenImpEth)),1)})",
            f"{df_cnt(dfWomenImpEth)} ({rnd(100*df_cnt(dfWomenImpEth)/(df_cnt(dfWomenNonImpEth)+df_cnt(dfWomenImpEth)),1)})",
            f"{df_cnt(dfWomenNonImpEth)+df_cnt(dfWomenImpEth)}",
            f"{df_cnt(dfMenNonImpEth)} ({rnd(100*df_cnt(dfMenNonImpEth)/(df_cnt(dfMenNonImpEth)+df_cnt(dfMenImpEth)),1)})",
            f"{df_cnt(dfMenImpEth)} ({rnd(100*df_cnt(dfMenImpEth)/(df_cnt(dfMenNonImpEth)+df_cnt(dfMenImpEth)),1)})",
            f"{df_cnt(dfMenNonImpEth)+df_cnt(dfMenImpEth)}"
        ])
    
        our_vals.extend([
            df_cnt(dfWomenNonImpEth),
            rnd(100*df_cnt(dfWomenNonImpEth)/(df_cnt(dfWomenNonImpEth)+df_cnt(dfWomenImpEth)),1),
            df_cnt(dfWomenImpEth),
            rnd(100*df_cnt(dfWomenImpEth)/(df_cnt(dfWomenNonImpEth)+df_cnt(dfWomenImpEth)),1),
            df_cnt(dfWomenNonImpEth)+df_cnt(dfWomenImpEth),
            
            df_cnt(dfMenNonImpEth),
            rnd(100*df_cnt(dfMenNonImpEth)/(df_cnt(dfMenNonImpEth)+df_cnt(dfMenImpEth)),1),
            df_cnt(dfMenImpEth),
            rnd(100*df_cnt(dfMenImpEth)/(df_cnt(dfMenNonImpEth)+df_cnt(dfMenImpEth)),1),
            df_cnt(dfMenNonImpEth)+df_cnt(dfMenImpEth)
        ])

    return rows, our_vals

def st1_age_pct():

    rows = []
    our_vals = []

    # Age Category data collection
    age_categories = [
        ("20-39 years old", f_age_y),
        ("20-39 years old", f_age_m),  # This seems to be a duplicate label. Consider updating.
        (">=60 years old", f_age_a)
    ]

    for age_label, age_func in age_categories:

        dfWomenNonImpAge, dfWomenImpAge = age_func(dfWomenNonImp), age_func(dfWomenImp)
        dfMenNonImpAge, dfMenImpAge = age_func(dfMenNonImp), age_func(dfMenImp)

        rows.append([
            f"{age_label} %",
            f"{df_cnt(dfWomenNonImpAge)} ({rnd(100*df_cnt(dfWomenNonImpAge)/(df_cnt(dfWomenNonImpAge)+df_cnt(dfWomenImpAge)),1)})",
            f"{df_cnt(dfWomenImpAge)} ({rnd(100*df_cnt(dfWomenImpAge)/(df_cnt(dfWomenNonImpAge)+df_cnt(dfWomenImpAge)),1)})",
            f"{df_cnt(dfWomenNonImpAge)+df_cnt(dfWomenImpAge)}",
            f"{df_cnt(dfMenNonImpAge)} ({rnd(100*df_cnt(dfMenNonImpAge)/(df_cnt(dfMenNonImpAge)+df_cnt(dfMenImpAge)),1)})",
            f"{df_cnt(dfMenImpAge)} ({rnd(100*df_cnt(dfMenImpAge)/(df_cnt(dfMenNonImpAge)+df_cnt(dfMenImpAge)),1)})",
            f"{df_cnt(dfMenNonImpAge)+df_cnt(dfMenImpAge)}"
        ])
    
        our_vals.extend([
            df_cnt(dfWomenNonImpAge),
            rnd(100*df_cnt(dfWomenNonImpAge)/(df_cnt(dfWomenNonImpAge)+df_cnt(dfWomenImpAge)),1),
            df_cnt(dfWomenImpAge),
            rnd(100*df_cnt(dfWomenImpAge)/(df_cnt(dfWomenNonImpAge)+df_cnt(dfWomenImpAge)),1),
            df_cnt(dfWomenNonImpAge)+df_cnt(dfWomenImpAge),
            
            df_cnt(dfMenNonImpAge),
            rnd(100*df_cnt(dfMenNonImpAge)/(df_cnt(dfMenNonImpAge)+df_cnt(dfMenImpAge)),1),
            df_cnt(dfMenImpAge),
            rnd(100*df_cnt(dfMenImpAge)/(df_cnt(dfMenNonImpAge)+df_cnt(dfMenImpAge)),1),
            df_cnt(dfMenNonImpAge)+df_cnt(dfMenImpAge)
        ])       
        
    return rows, our_vals

def st1_bmi_pct():

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
        dfWomenNonImpBMI, dfWomenImpBMI = bmi_func(dfWomenNonImp), bmi_func(dfWomenImp)
        dfMenNonImpBMI, dfMenImpBMI = bmi_func(dfMenNonImp), bmi_func(dfMenImp)

        rows.append([
            f"{bmi_label} %",
            f"{df_cnt(dfWomenNonImpBMI)} ({rnd(100*df_cnt(dfWomenNonImpBMI)/(df_cnt(dfWomenNonImpBMI)+df_cnt(dfWomenImpBMI)),1)})",
            f"{df_cnt(dfWomenImpBMI)} ({rnd(100*df_cnt(dfWomenImpBMI)/(df_cnt(dfWomenNonImpBMI)+df_cnt(dfWomenImpBMI)),1)})",
            f"{df_cnt(dfWomenNonImpBMI)+df_cnt(dfWomenImpBMI)}",
            f"{df_cnt(dfMenNonImpBMI)} ({rnd(100*df_cnt(dfMenNonImpBMI)/(df_cnt(dfMenNonImpBMI)+df_cnt(dfMenImpBMI)),1)})",
            f"{df_cnt(dfMenImpBMI)} ({rnd(100*df_cnt(dfMenImpBMI)/(df_cnt(dfMenNonImpBMI)+df_cnt(dfMenImpBMI)),1)})",
            f"{df_cnt(dfMenNonImpBMI)+df_cnt(dfMenImpBMI)}"
        ])
    
        our_vals.extend([
            df_cnt(dfWomenNonImpBMI),
            rnd(100*df_cnt(dfWomenNonImpBMI)/(df_cnt(dfWomenNonImpBMI)+df_cnt(dfWomenImpBMI)),1),
            df_cnt(dfWomenImpBMI),
            rnd(100*df_cnt(dfWomenImpBMI)/(df_cnt(dfWomenNonImpBMI)+df_cnt(dfWomenImpBMI)),1),
            df_cnt(dfWomenNonImpBMI)+df_cnt(dfWomenImpBMI),
            
            df_cnt(dfMenNonImpBMI),
            rnd(100*df_cnt(dfMenNonImpBMI)/(df_cnt(dfMenNonImpBMI)+df_cnt(dfMenImpBMI)),1),
            df_cnt(dfMenImpBMI),
            rnd(100*df_cnt(dfMenImpBMI)/(df_cnt(dfMenNonImpBMI)+df_cnt(dfMenImpBMI)),1),
            df_cnt(dfMenNonImpBMI)+df_cnt(dfMenImpBMI)
        ])

    return rows, our_vals

def st1_tbl():

    # Replicate table
    rows = []
    rows.append(["", "Women", "Men", "Women", "Men"])
    rows.append(st1_samples()[0])
    rows.extend(st1_race_pct()[0])
    rows.extend(st1_age_pct()[0])
    rows.extend(st1_bmi_pct()[0])
    file.write(tabulate(rows, headers, tablefmt='github'))
    file.write("\n\n\n")

    vals = []   
    vals.extend(st1_samples()[1])
    vals.extend(st1_race_pct()[1])
    vals.extend(st1_age_pct()[1])
    vals.extend(st1_bmi_pct()[1])

    return vals

def st1_tbl_from_vals(paper_vals, our_vals):

    # Determine diffs
    diff_vals = [paper - our for paper, our in zip(paper_vals, our_vals)]
    diff_vals = [round(value, 2) for value in diff_vals]

    # Generate diffs    
    rows = [
        ["", "Women NImp", "%", "Women Imp", "%", "Total", "Men NImp", "%", "Men Imp", "%", "Total"],
            ["N", *diff_vals[0:10]],
            ["Mexican-American %", *diff_vals[10:20]],
            ["European-American %", *diff_vals[20:30]],
            ["African-American %", *diff_vals[30:40]],
            ["20-39 years old %", *diff_vals[40:50]],
            ["40-59 years old %", *diff_vals[50:60]],
            [">=60 years old %", *diff_vals[60:70]],
            ["<18.5 %", *diff_vals[70:80]],
            ["18.5-24.9 %", *diff_vals[80:90]],
            ["25-29.9 %", *diff_vals[90:100]],
            [">=30 %", *diff_vals[100:110]]
    ]

    headers = ["", "Non-imputed data", "%", "Imputed data", "%", "Total", "Non-imputed data","%", "Imputed data", "%", "Total"]

    file.write(tabulate(rows, headers, tablefmt="github"))    
    file.write("\n")

def st1(dfTr, dfTe):
        
    global dfTrain
    global dfTest
    global dfWomen
    global dfMen
    global dfWomenNonImp
    global dfWomenImp
    global dfMenNonImp
    global dfMenImp

    # Heading
    file.write("\n")
    file.write("# Supplimentary Table 1 Replacation\n")
    file.write( "Frequency of DXA multiply imputed data in among adult participants (≥20 years old) in the"
                " training dataset .\n\n")

    # Replication table; Filter according to the paper
    file.write("## Replication\n")
    file.write( "Our attempts to exactly replicate the second table in the suppimentary material. We could only"
                " achieve the precise totals by including the race demographics that are excluded from the work "
                "(r=2, r=5, r=. missing). \n\n")
    dfTrain = f_all_paper(dfTr)
    dfWomen = f_wom(dfTrain)
    dfMen = f_men(dfTrain)
    dfWomenNonImp, dfWomenImp = f_nimp(dfWomen, True), f_imp(dfWomen, True)
    dfMenNonImp, dfMenImp = f_nimp(dfMen, True), f_imp(dfMen, True)
    vals = st1_tbl()
    file.write("\n")

    # Diff table
    file.write("## Diff: Paper-Replication Table\n")
    file.write("We see complete replication when including all race categories \n\n")
    st1_tbl_from_vals(paper_vals, vals)
    file.write("\n")

    # Removing Other Races
    file.write("## Table 1 Limiting to r=1, r=3, r=5\n")
    file.write( "We now consider the totals when only the Mex-Am (r=1), Eur-Am (r=3) and Afr-Am (r=4) are included. "
                "We believe this is what the authors meant to based their work on, and it is uncertain if the incorrect dataset "
                "was used throughout their work. When we consider thta the age and BMI totals are impacted, but the race categories are not "
                "it suggests that there is strict filtering on the race catgories but all data is considered in the other categories \n\n")
    dfTrain = f_all_paper(dfTr)
    dfTrain = f_race(dfTrain)
    dfWomen = f_wom(dfTrain)
    dfMen = f_men(dfTrain)
    dfWomenNonImp, dfWomenImp = f_nimp(dfWomen, True), f_imp(dfWomen, True)
    dfMenNonImp, dfMenImp = f_nimp(dfMen, True), f_imp(dfMen, True)
    vals_race = st1_tbl()

    # Diff table
    file.write("## Diff: Paper-Race Limited Table\n")
    file.write( "We observe a reduction in around 8% of the data when we limit race to the expected categories: r=2, r=5 and r=. "
                "missing. The most heavily impacted is the Non-imputed datasets.  \n\n")
    st1_tbl_from_vals(paper_vals, vals_race)
    file.write("\n")

    # Removing NAs
    file.write("## Table 1 Removing NaNs\n")
    file.write(f"We remove NaNs from the columns {','.join(iConsider)}. We do this to avoid any potential issues in correlation from missing values. \n\n")
    dfTrain = f_all_paper(dfTr)
    dfTrain = dfTrain.dropna(subset=iConsider, axis=0)
    dfWomen = f_wom(dfTrain)
    dfMen = f_men(dfTrain)
    dfWomenNonImp, dfWomenImp = f_nimp(dfWomen, True), f_imp(dfWomen, True)
    dfMenNonImp, dfMenImp = f_nimp(dfMen, True), f_imp(dfMen, True)
    nas_race = st1_tbl()

    # Diff table
    file.write("## Diff: Paper-NaNs Table\n")
    file.write(f"We have a loss of around 24% when we remove NaNs from the mentioned columns \n\n")
    st1_tbl_from_vals(paper_vals, nas_race)
    file.write("\n")

    # Our Data
    file.write("# Our Data\n")
    file.write("We correctly limits race codes and removes NaNs, resulting in the following data \n\n")
    dfTrain = f_all_ours(dfTr)
    dfWomen = f_wom(dfTrain)
    dfMen = f_men(dfTrain)
    dfTrain.to_csv(f"{outDataDir}/andy_test.csv", index=False)

    dfWomenNonImp, dfWomenImp = f_nimp(dfWomen, True), f_imp(dfWomen, True)
    dfMenNonImp, dfMenImp = f_nimp(dfMen, True), f_imp(dfMen, True)
    vals_ours = st1_tbl()
    file.write("\n")

    # Diff table
    file.write("## Diff: Paper-Our Table\n")
    file.write( "We observe no further reduction in size when both Nans and unexpected races are excluded. This suggests that there are only Nans in the "
                "in the r=2, r=5, r=. missing races. \n\n")
    st1_tbl_from_vals(paper_vals, vals_ours)
    file.write("\n")

    file.close()
