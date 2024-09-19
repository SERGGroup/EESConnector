# %% --------------------  IMPORT MODULES                                      ---------------------------------------- #
from EESConnect.constants import ROOT_DIR
from EESConnect import EESConnectorPlus
import numpy as np
import os


# %% --------------------  INIT CALCULATIONS                                   ---------------------------------------- #
base_folder = os.path.join(os.path.dirname(ROOT_DIR), "examples", "EES Connect Plus", "2 - Optimization")

b = np.linspace(10, 20, num=5)
c = np.array([3])
b, c = np.meshgrid(b, c, indexing='ij')

params = {

    "input": {

        "b": list(b.flatten()),
        "c": list(c.flatten())

    },

    "output": {

        "x_max": None,
        "y_max": None

    }

}


# %% --------------------  CALCULATE                                           ---------------------------------------- #
with EESConnectorPlus(timeout=10, display_progress_bar=True) as ees:

    ees.ees_file_path = os.path.join(base_folder, "optimization_trial.EES")
    ees.calculation_instruction = "Minimize y_max  x_max  /Method=Conjugate  /RelTol=1e-6  /MaxIt=500"

    params = ees.calculate(params)
