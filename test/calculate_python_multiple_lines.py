#%% --------------------  IMPORT MODULES                                      ---------------------------------------- #
from EESConnect.constants import ROOT_DIR
from EESConnect import EESConnector
import os


#%% --------------------  INIT CALCULATIONS                                   ---------------------------------------- #
base_folder = os.path.join(os.path.dirname(ROOT_DIR), "test")
input_dict = {

    "1": [0.45, 100, 0.8],
    "2": [0.50, 100, 0.8]

}


#%% --------------------  CALCULATE                                           ---------------------------------------- #
with EESConnector() as ees:

    ees.ees_file_path = os.path.join(base_folder, "EES HCT High Concentration_V3python.EES")
    result = ees.calculate(input_dict)

print(result)