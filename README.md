# EES connector

__EES connector__ is a tools developed by the [SERG research group](https://www.dief.unifi.it/vp-177-serg-group-english-version.html) 
of the [University of Florence](https://www.unifi.it/changelang-eng.html) for launching [EES](https://fchartsoftware.com/ees/) 
calculation and retrieving results from python.

### Installing EES Connector
The beta version can be downloaded using __PIP__:

```
pip install EES_connector
```

### EES Connector +
From **version 1.0.0** a major improvement has been made to the code. For compatibility the previous version 
(_EESConnector_) is still usable (you can find the old documentation 
[here](https://github.com/SERGGroup/EESConnector/blob/master/examples/EES%20Connect/README.md)) but 
**it will not be maintained**

### Launching a calculation
Once the installation has been completed the user can import the tool and initialize the connector itself.
```python
from EESConnect import EESConnectorPlus

with EESConnectorPlus() as ees:

    # insert your code here

```
__Two important aspects to keep in mind for the initialization:__

  * Please use the __with statement__ during the initialization as shown above
    

  * A file-dialog will appear the first time that the connector is imported __asking the user to select the EES 
    executable path__ (usually it's _"C:\EES32\ees.exe"_). 
    Once the executable path has been selected, the program keep it in memory in order to avoid new appearance of the 
    file-dialog. The stored executable can be modified calling the following function:
    
```python
from EESConnect import EESConnectorPlus

EESConnectorPlus.modify_ees_executable_path()
```
    
<br/>   
Finally, you can ask the program to launch EES calculation using the following command:

```python
from EESConnect import EESConnectorPlus
from tkinter import filedialog
import tkinter as tk

#select the ees file path
root = tk.Tk()
root.withdraw()
ees_file_path = filedialog.askopenfilename()

with EESConnectorPlus() as ees:
    
    ees.ees_file_path = ees_file_path
    params = ees.calculate({
        
        "input": {"fluid$": "air_ha", "T": 300, "P": 1013.25}, 
        "output": {"h": None, "s": None}
    
    })
    print(params)

```

Calls with multiple parameters are possible as follows:
```python
from EESConnect import EESConnectorPlus
from tkinter import filedialog
import tkinter as tk

#select the ees file path
root = tk.Tk()
root.withdraw()
ees_file_path = filedialog.askopenfilename()

params = {
    
    "input": {
        
        "fluid$": ["air_ha", "R22", "R236fa", "R134a"], 
        "T": [300, 300, 300, 300], 
        "P": [1013.25, 1013.25, 1013.25, 1013.25]
    
    }, 
    "output": {"h": None, "s": None}

}

with EESConnectorPlus() as ees:
    
    ees.ees_file_path = ees_file_path
    params = ees.calculate(params)
    print(params)
```

### EES file configuration
Please notice that the EES file has to be configured properly in order to work.<br>
Here's an example, that works with the python code described above:
```
$UnitSystem SI K kPa kJ 
h=enthalpy(fluid$; T=T; P=P)
s=entropy(fluid$; T=T; P=P)
```
An explanation on how to set EES properly can be found [here](https://fchartsoftware.com/ees/eeshelp//hs605.htm). 
In addition here's some important things had to be noted:

 * The keys of the "input" and "output" dictionaries __must share the same name__, in the EES code, with the variable that they refer in
 * The values identified in the "input" dictionary **must not be defined in the code** (e.g. do not write "T=300" in the code above)
 * The code must work if the variable identified in the "input" dictionary are manually set in the code
 
### Calculation Options
Multiple options could be set in initializing the calculator:

```python
from EESConnect import EESConnectorPlus

with EESConnectorPlus(ees_decimal_separator=".", display_progress_bar=True, timeout=10) as ees:

    # insert your code here

```
* _"ees_decimal_separator"_ allows you to set the decimal separator in order to match the one required by your EES file. 
    The default is a comma (",")
* _"display_progress_bar"_ shows a bar describing the progress of the calculation
* _"timeout"_ set a timeout limit for the calculation (value to be set in seconds)


### Excel Exporter
You export the results of your calculation to excel using Pandas with the following code:

```python
with EESConnectorPlus(timeout=10, display_progress_bar=True) as ees:

    # Calculate
    params = ees.calculate(params)
    
    # Export results
    ees.export_to_excel(params=params, excel_path=os.path.join(base_folder, "results.xlsx"))
```

### EES Optimization and other Execution Personalization
EESConnectorPlus works by executing [EES Macros](https://fchartsoftware.com/ees/eeshelp/macro_commands.htm). 
The behaviour of the macro can be modified by the user to perform more complex operation (the most typical usage is to 
**perform optimization** in EES). This can be done by modifying the attribute "ees.calculation_instruction".
For example, for performing the optimization, you can use the [Minimize Macro instruction](https://fchartsoftware.com/ees/eeshelp/hs4165.htm) as shown below:

```python
from EESConnect import EESConnectorPlus

with EESConnectorPlus() as ees:

    ees.ees_file_path = os.path.join(base_folder, "optimization_trial.EES")
    
    # This code can be used to minimize y_max by changing x_max
    ees.calculation_instruction = "Minimize y_max  x_max  /Method=Conjugate  /RelTol=1e-6  /MaxIt=500"

    params = ees.calculate(params)

```
by default _ees.calculation_instruction = "[Solve](https://fchartsoftware.com/ees/eeshelp/hs4320.htm)"_. <br/>
In general the MACRO that will be run by EES will be the following:
```
ONERROR GOTO 10
DIR$=GetDirectory$
Open 'ees_program.ees'
Import 'ees_input.dat' f$ {{ Input Parameters }}

{{ calculation_instruction }}

Export f$ {{ Output Parameters }}
10:quit
```

### Example Code
You can find some example code in 
[this](https://github.com/SERGGroup/EESConnector/tree/master/examples/EES%20Connect%20Plus) folder
<br/><br/>

__-------------------------- !!! THIS IS A BETA VERSION !!! --------------------------__ 

please report any bug or problems in the installation to _pietro.ungar@unifi.it_<br/>
for further information visit: https://tinyurl.com/SERG-3ETool
