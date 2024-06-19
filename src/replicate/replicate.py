
# Replication imports
from .tbl.all import *      # Paper tables
from .fig.all import *      # Paper figures
from .sup_tbl.all import *  # Supplimentary tables

def replicate_all(dfTr, dfTe):

    pt_all(dfTr, dfTe)
    pf_all(dfTr, dfTe)
    st_all(dfTr, dfTe)
