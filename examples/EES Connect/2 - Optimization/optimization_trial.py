# %% --------------------  IMPORT MODULES                                      ---------------------------------------- #
from EESConnect.constants import ROOT_DIR
from EESConnect import EESConnector
import numpy as np
import os


# %% --------------------  INIT CALCULATIONS                                   ---------------------------------------- #
base_folder = os.path.join(os.path.dirname(ROOT_DIR), "EES Connect", "examples", "2 - Optimization")
b_range = np.linspace(10, 20, num=5)

input_dict = {}

for b in b_range:

    input_dict.update({"{0:.2f}".format(b): [b, 3]})


# %% --------------------  CALCULATE                                           ---------------------------------------- #
with EESConnector(timeout=10, display_progress_bar=True) as ees:

    ees.ees_file_path = os.path.join(base_folder, "optimization_trial.EES")
    ees.macro_path = os.path.join(base_folder, "ees_optimize_macro.EMF")

    result = ees.calculate(input_dict)
