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
