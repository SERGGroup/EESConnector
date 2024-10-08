from tkinter import filedialog
import tkinter as tk
import os


def retrieve_EES_path(failure_possible=True):
    root = tk.Tk()
    root.withdraw()
    __EES_PATH = filedialog.askopenfilename(

        title='select EES executable'

    )
    root.destroy()

    if os.path.isfile(__EES_PATH):

        with open(__EES_PATH_FILE, "w") as f:
            f.write(__EES_PATH)

        return __EES_PATH

    else:

        if not failure_possible:
            raise FileNotFoundError(
                "\n\nEES executable path must be provided!\n\n\t{} is not a suitable path\n\nExecution will stop!\n\n".format(
                    EES_PATH))

        return None


"""
In this module the path of the EES executable has to be retrieved. 
This can be done in two ways:

    If the "ees_path.dat" file exists, the code will read the path from there, otherwise the program will ask the user 
    to identify the path. In order to prevent the code from asking the user the path each import call, the selected path
    is written in the "ees_path.dat" file.
    
    the macro file is checked and generated as well 

"""

EES_PATH = None
ROOT_DIR = os.path.dirname(__file__)
__EES_PATH_FILE = os.path.join(ROOT_DIR, "ees_path.dat")

if os.path.isfile(__EES_PATH_FILE):

    with open(__EES_PATH_FILE) as f:
        lines = f.readlines()

    if os.path.isfile(str(lines[0])):
        EES_PATH = str(lines[0])

if EES_PATH is None:
    EES_PATH = retrieve_EES_path(failure_possible=False)

EES_DIR = os.path.dirname(EES_PATH)
EES_REFPROP_DIR = os.path.join(EES_DIR, "Userlib", "Userlib", "EES_REFPROP")
EES_REFPROP_TMP_DIR = os.path.join(EES_DIR, "EES_REFPROP")

"""
    
    MACRO FILE GENERATION:
    EES macro file should be saved in the workspace directory where the EES file will be stored too
    the name that the ees file must have is 

"""

WORKSPACE_DIR = os.path.join(ROOT_DIR, "workspace")

if not os.path.isdir(WORKSPACE_DIR):
    os.mkdir(WORKSPACE_DIR)

EES_MACRO = os.path.join(WORKSPACE_DIR, "ees_macro.EMF")
EES_DEFAULT_MACRO = os.path.join(WORKSPACE_DIR, "ees_run_macro.EMF")
EES_RUN_FILENAME = os.path.join(WORKSPACE_DIR, "ees_program.ees")
EES_INPUT_FILENAME = "ees_input.dat"
EES_OUTPUT_FILENAME = "ees_output.dat"
IO_FILE_EXTENSION = ".pyees"

BASE_MACRO_TXT = "ONERROR GOTO 10\n"
BASE_MACRO_TXT += "DIR$=GetDirectory$\n"
BASE_MACRO_TXT += "Open 'ees_program.ees'\n"
BASE_MACRO_TXT += "{input_params}\n"
BASE_MACRO_TXT += "{calculation_instruction}\n"
BASE_MACRO_TXT += "Export f$ {output_params}\n"
BASE_MACRO_TXT += "10:quit\n"
