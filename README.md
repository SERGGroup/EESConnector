# EES connector

__EES connector__ is a tools developed by the [SERG research group](https://www.dief.unifi.it/vp-177-serg-group-english-version.html) 
of the [University of Florence](https://www.unifi.it/changelang-eng.html) for launching [EES](https://fchartsoftware.com/ees/) 
calculation and retrieving results from python.

The beta version can be downloaded using __PIP__:

```
pip install EES_connector
```
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
    print(result[0][1])

```
please notice that the EES file has to be configured properly in order to work.<br>
Here an example, that works with the python code described above:
```
$UnitSystem SI K kPa kJ 
$Import 'ees_input.dat' F$ T P

h=enthalpy(F$; T=T; P=P)
s=entropy(F$; T=T; P=P)

$Export 'ees_output.dat' h s
```
An explaination on how to set EES properly can be found [here](https://fchartsoftware.com/ees/eeshelp//hs605.htm).
Please notice two important things:

 * The input defined in the EES file __must be consistent with the list provided to the calculation function__ as an input


 * The files input and output file for EES __must be called__ _"ees_input.dat"_ and _"ees_output.dat"_ respectively!
   
<br/><br/>
__-------------------------- !!! THIS IS A BETA VERSION !!! --------------------------__ 

please report any bug or problems in the installation to _pietro.ungar@unifi.it_<br/>
for further information visit: https://tinyurl.com/SERG-3ETool
