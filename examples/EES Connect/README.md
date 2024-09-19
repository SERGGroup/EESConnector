# EES connector

__EES connector__ is a tools developed by the [SERG research group](https://www.dief.unifi.it/vp-177-serg-group-english-version.html) 
of the [University of Florence](https://www.unifi.it/changelang-eng.html) for launching [EES](https://fchartsoftware.com/ees/) 
calculation and retrieving results from python.

### Installing EES Connector
The beta version can be downloaded using __PIP__:

```
pip install EES_connector
```

### Launching a calculation
Once the installation has been completed the user can import the tool and initialize the connector itself.
```python
from EESConnect import EESConnector

with EESConnector() as ees:

    # insert your code here

```
__Two important aspects to keep in mind for the initialization:__

  * Please use the __with statement__ during the initialization as shown above
    

  * A file-dialog will appear the first time that the connector is imported __asking the user to select the EES 
    executable path__ (usually it's _"C:\EES32\ees.exe"_). 
    Once the executable path has been selected, the program keep it in memory in order to avoid new appearance of the 
    file-dialog. The stored executable can be modified calling the following function:
    
```python
from EESConnect import EESConnector

EESConnector.modify_ees_executable_path()
```
    
<br/>   
Finally, you can ask the program to launch EES calculation using the following command:

```python
from EESConnect import EESConnector
from tkinter import filedialog
import tkinter as tk

#select the ees file path
root = tk.Tk()
root.withdraw()
ees_file_path = filedialog.askopenfilename()

with EESConnector() as ees:
    
    ees.ees_file_path = ees_file_path
    result = ees.calculate(["air_ha", 110, 1013.25])
    print(result[1])

```
Multiple call are possible passing a dictionaty in the ees.calculate() function in order to speed up the calculation 
process (the program is loaded on the RAM only once):

```python
from EESConnect import EESConnector
from tkinter import filedialog
import tkinter as tk

#select the ees file path
root = tk.Tk()
root.withdraw()
ees_file_path = filedialog.askopenfilename()

with EESConnector() as ees:
    
    ees.ees_file_path = ees_file_path
    result = ees.calculate({

            "air_ha":   ["air_ha", 300, 1013.25],
            "R22":      ["R22", 300, 1013.25],
            "R236fa":   ["R236fa", 300, 1013.25],
            "R134a":    ["R134a", 300, 1013.25]

        })
    
    print(result["R22"][1])
    print(result["R236fa"][1])
```

### EES file configuration
Please notice that the EES file has to be configured properly in order to work.<br>
Here's an example, that works with the python code described above:
```
$UnitSystem SI K kPa kJ 
$Import 'ees_input.dat' file$ F$ T P

h=enthalpy(F$; T=T; P=P)
s=entropy(F$; T=T; P=P)

$Export file$ h s
```
An explanation on how to set EES properly can be found [here](https://fchartsoftware.com/ees/eeshelp//hs605.htm). 
Two important things had to be noted:

 * The input defined in the EES file __must be consistent with the list provided to the calculation function__ as an input
 * The input and output file in the EES code __must be called__ _"ees_input.dat"_ and _"ees_output.dat"_ respectively!
 
### Calculation Options
Multiple options could be set in initializing the calculator:

```python
from EESConnect import EESConnector

with EESConnector(ees_decimal_separator=".", display_progress_bar=True, timeout=10) as ees:

    # insert your code here

```
* _"ees_decimal_separator"_ allows you to set the decimal separator in order to match the one required by your EES file. 
    The default is a comma (",")
* _"display_progress_bar"_ shows a bar describing the progress of the calculation
* _"timeout"_ set a timeout limit for the calculation (value to be set in seconds)

<br/><br/>

__-------------------------- !!! THIS IS A BETA VERSION !!! --------------------------__ 

please report any bug or problems in the installation to _pietro.ungar@unifi.it_<br/>
for further information visit: https://tinyurl.com/SERG-3ETool
