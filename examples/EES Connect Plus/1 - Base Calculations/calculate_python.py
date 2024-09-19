#%% --------------------  IMPORT MODULES                                      ---------------------------------------- #
from EESConnect.constants import ROOT_DIR
from EESConnect import EESConnectorPlus
import numpy as np
import os


#%% --------------------  INIT CALCULATIONS                                   ---------------------------------------- #
base_folder = os.path.join(os.path.dirname(ROOT_DIR), "examples", "EES Connect Plus", "1 - Base Calculations")
y_17 = np.linspace(0.45, 0.5, num=2)
m_dot = np.linspace(100, 300, num=1)
fr = np.linspace(0.8, 0.9, num=1)

y_17, m_dot, fr = np.meshgrid(y_17, m_dot, fr, indexing='ij')

params = {

    "input": {

        "y[17]": list(y_17.flatten()),
        "m_dot[8]": list(m_dot.flatten()),
        "FR_Recycle": list(fr.flatten()),

    },

    "output": {

        "Q_dot_dear": None,
        "Eta": None,
        "Eta_II": None

    }

}


#%% --------------------  CALCULATE                                           ---------------------------------------- #
with EESConnectorPlus(display_progress_bar=True) as ees:

    ees.ees_file_path = os.path.join(base_folder, "EES HCT High Concentration_V3python.EES")
    params = ees.calculate(params)
    ees.export_to_excel(params, os.path.join(base_folder, "results.xlsx"))
