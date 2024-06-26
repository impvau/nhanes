
from download import *
from globals import *
from preproc import *

download(dataDir)
dfTrain, dfTest = preproc(dataDir)

