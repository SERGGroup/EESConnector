#%% --------------------  IMPORT MODULES                                      ---------------------------------------- #
from EESConnect.constants import ROOT_DIR
from EESConnect import EESConnector
import pandas as pd
import numpy as np
import os


#%% --------------------  INIT CALCULATIONS                                   ---------------------------------------- #
base_folder = os.path.join(os.path.dirname(ROOT_DIR), "examples", "EES Connect", "1 - Base Calculations")
y_range = np.linspace(0.45, 0.5, num=2)
m_range = np.linspace(100, 300, num=1)
fr_range = np.linspace(0.8, 0.9, num=1)

df = {

    "y[17]": list(),
    "m_dot": list(),
    "fr": list(),
    "Q_dot_dear": list(),
    "Eta": list(),
    "Eta_ex": list()

}


#%% --------------------  CALCULATE                                           ---------------------------------------- #
with EESConnector(timeout=10) as ees:

    ees.ees_file_path = os.path.join(base_folder, "EES HCT High Concentration_V3python.EES")
    
    for y in y_range:

        for m in m_range:

            for fr in fr_range:

                try:

                    result = ees.calculate([y, m, fr])
                
                    df["y[17]"].append(y)
                    df["m_dot"].append(m)
                    df["fr"].append(fr)
                    df["Q_dot_dear"].append(result[0])
                    df["Eta"].append(result[1])
                    df["Eta_ex"].append(result[2])

                    print(df)

                except Exception as error:

                    print(error)


#%% --------------------  EXPORT TO EXCEL                                     ---------------------------------------- #
df = pd.DataFrame(df)
excel_path = os.path.join(base_folder, 'result.csv')
df.to_csv(excel_path, index=False)

print(excel_path)
