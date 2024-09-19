import EESConnect.constants as constants
from tkinter import filedialog
from tqdm import tqdm
import tkinter as tk
import subprocess
import shutil, os


class EESConnector:

    def __init__(

            self, ees_file_path=None, macro_path=None,
            keep_refprop=False, ees_decimal_separator=",",
            display_progress_bar=False, timeout=None

    ):

        self.__clear_files()

        self.__ees_file_path = None
        self.__macro_path = None
        self.__with_initialization = False
        self.__keep_refprop = keep_refprop
        self.__decimal_separator = ees_decimal_separator
        self.__display_progress_bar = display_progress_bar
        self.__timeout = timeout

        if ees_file_path is not None:
            self.ees_file_path = ees_file_path

        if macro_path is not None:
            self.macro_path = macro_path

    def __enter__(self):

        self.__with_initialization = True
        self.move_REFPROP_DIR(move_away=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.move_REFPROP_DIR(move_away=False)
        if self.is_ready:
            # This part delete the file used for data IO
            self.__clear_files()

    def move_REFPROP_DIR(self, move_away=True):

        if move_away:

            if os.path.isdir(constants.EES_REFPROP_DIR) and not self.__keep_refprop:
                # This part of the code moves the EES-REFPROP plugin folder away from its correct location in order to
                # prevent the plugin from asking the user the position of the Refprop folder on each iteration.
                shutil.move(constants.EES_REFPROP_DIR, constants.EES_REFPROP_TMP_DIR)

        else:

            if os.path.isdir(constants.EES_REFPROP_TMP_DIR):
                # This part of the code moves the EES-REFPROP plugin folder back to its correct location in order to
                # restore the plugin functionality
                shutil.move(constants.EES_REFPROP_TMP_DIR, constants.EES_REFPROP_DIR)

    def calculate(self, input_list):

        if type(input_list) == list:

            return self.__direct_calculation_passage(input_list)

        elif type(input_list) == dict:

            return_dict = dict()

            if self.__display_progress_bar:
                pbar = tqdm(desc="EES Calculation Ongoing", total=len(input_list.keys()))

            for key in input_list.keys():

                return_dict.update({

                    key: self.__direct_calculation_passage(input_list[key])

                })

                if self.__display_progress_bar:
                    pbar.update(1)

            if self.__display_progress_bar:
                pbar.close()

            return return_dict

        else:

            return None

    def __direct_calculation_passage(self, input_list):

        filename = os.path.join(constants.WORKSPACE_DIR, "ees_input.dat")
        self.__write_input_file(input_list, filename)

        try:

            subprocess.run(self.system_command, timeout=self.__timeout, cwd=constants.WORKSPACE_DIR)

        except:

            return None

        else:

            filename = os.path.join(constants.WORKSPACE_DIR, "ees_output.dat")
            return self.__read_output_file(filename)

    def __write_input_file(self, input_list, filename):

        output_filename = os.path.join(constants.WORKSPACE_DIR, "ees_output.dat")
        if os.path.isfile(output_filename):
            os.remove(output_filename)

        string_to_write = "'" + output_filename + "'"

        for element in input_list:
            string_to_write += "\t" + str(element).replace(".", self.__decimal_separator)

        with open(filename, "w") as f:
            f.write(string_to_write)

    @staticmethod
    def __read_output_file(filename):

        with open(filename, "r") as f:

            lines = f.readlines()

        return_list = list()

        for line in lines:

            for element in line.strip("\n").split("\t"):

                try:

                    return_list.append(float(element.replace(",", ".")))

                except:

                    return_list.append(element)

        return return_list

    @property
    def system_command(self):

        if self.__solve_with_macro:

            return "{} {} /hide".format(constants.EES_PATH, constants.EES_MACRO)

        else:

            return "{} {} /solve /hide".format(constants.EES_PATH, constants.EES_RUN_FILENAME)

    @staticmethod
    def __clear_files(clear_only_input_files=False):

        for file in os.listdir(constants.WORKSPACE_DIR):

            if file.endswith(constants.IO_FILE_EXTENSION) or file.endswith(".dat") or file.endswith(".DAT"):
                os.remove(os.path.join(constants.WORKSPACE_DIR, file))

            if file.endswith(".ees") and (not clear_only_input_files):
                os.remove(os.path.join(constants.WORKSPACE_DIR, file))

    def select_file(self):

        root = tk.Tk()
        root.withdraw()

        self.ees_file_path = filedialog.askopenfilename(title='select EES file')

        root.destroy()

    @property
    def is_ready(self):

        return self.__ees_file_path is not None

    @property
    def ees_file_path(self):
        return self.__ees_file_path

    @ees_file_path.setter
    def ees_file_path(self, ees_file_path):

        if os.path.isfile(ees_file_path):

            self.__ees_file_path = ees_file_path

            if os.path.isfile(constants.EES_RUN_FILENAME):
                os.remove(constants.EES_RUN_FILENAME)

            shutil.copy(ees_file_path, constants.EES_RUN_FILENAME)

    @property
    def macro_path(self):
        return self.__macro_path

    @macro_path.setter
    def macro_path(self, macro_path):

        if os.path.isfile(macro_path):

            self.__macro_path = macro_path
            self.__solve_with_macro = True

            if os.path.isfile(constants.EES_MACRO):
                os.remove(constants.EES_MACRO)

            shutil.copy(macro_path, constants.EES_MACRO)

        else:

            self.__macro_path = None

    @property
    def solve_with_macro(self):

        return self.__macro_path is not None

    @classmethod
    def modify_ees_executable_path(cls):

        constants.retrieve_EES_path()
