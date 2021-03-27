import pandas as pd
import pickle
import os

from definitions import *
from datamanager.processing import prepare_unloc, prepare_ccodes, check_ccode_loccode


rawdatainfo = pd.read_csv(joinpath(DATAMGR_PATH, 'overview_rawdata.csv'), sep=';')

# city codes
if not os.path.isfile(UNLOC_FILE_CLEAN_ABS):
    unloc = prepare_unloc(unloc_files=UNLOC_FILES_ABS)
    with open(UNLOC_FILE_CLEAN_ABS, 'wb') as f:
        pickle.dump(unloc, f)
else:
    with open(UNLOC_FILE_CLEAN_ABS, 'rb') as f:
        unloc = pickle.load(f)
    print(unloc.shape)

# ccodes
if not os.path.isfile(CCODE_FILE_CLEAN_ABS):
    ccodes = prepare_ccodes(ccode_file=CCODE_FILE_ABS)
    with open(CCODE_FILE_CLEAN_ABS, 'wb') as f:
        pickle.dump(ccodes, f)
else:
    with open(CCODE_FILE_CLEAN_ABS, 'rb') as f:
        ccodes = pickle.load(f)
    print(unloc.shape)


check_ccode_loccode(ccodes, unloc)
