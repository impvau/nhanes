
from download import *
from preproc import *
from globals import *
from replicate.replicate import *

download(dataDir)
dfTrain, dfTest = preproc(dataDir)
replicate_all(dfTrain, dfTest)

# Filter according to the paper, generated the mean
dfTrainPaper = f_all_paper(dfTrain)
dfTrainOurs = f_all_ours(dfTrain)
dfTestPaper = f_all_paper(dfTest, False)
dfTestOurs = f_all_ours(dfTest, False)

# For speed, commented out here
dfTrainPaper.to_csv( f"{outDataDir}/train_paper.csv", index=False)
dfTestPaper.to_csv(f"{outDataDir}/test_paper.csv", index=False)
dfTrainOurs.to_csv(f"{outDataDir}/train_ours.csv", index=False)
dfTestOurs.to_csv(f"{outDataDir}/test_ours.csv", index=False)
