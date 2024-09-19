import EESConnect.constants as constants
from tkinter import filedialog
from typing import Union, List
from copy import deepcopy
from tqdm import tqdm
import tkinter as tk
import subprocess
import shutil, os


class EESConnectorPlus:

    def __init__(

            self, ees_file_path: str = None, calculation_instruction: str = "solve",
            keep_refprop: bool = False, ees_decimal_separator: str = ",",
            display_progress_bar: bool = False, timeout: float = None,
            use_input_file: bool = False

    ):

        self.__clear_files()
        self.calculation_instruction = calculation_instruction

        self.__ees_file_path = None
        self.__with_initialization = False
        self.__keep_refprop = keep_refprop
        self.__decimal_separator = ees_decimal_separator
        self.__display_progress_bar = display_progress_bar
        self.__use_input_file = use_input_file
        self.__timeout = timeout

        if ees_file_path is not None:
            self.ees_file_path = ees_file_path

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

    def calculate(self, params: Union[List[dict], dict]) -> Union[List[dict], dict]:

        if self.is_ready:

            if self.__use_input_file:

                self.__define_base_macro(

                    input_params=params[0]["input"],
                    output_params=params[0]["output"]

                )

            if type(params) == dict:

                params = self.__calculate_dict(params)

            else:

                params = self.__calculate_list(params)

        return params

    def __calculate_dict(self, params: dict) -> dict:

        first_key = list(params["input"].keys())[0]
        if type(params["input"][first_key]) == list:

            n_points = len(params["input"][first_key])
            self.init_progress_bar(n_points)
            sub_params = deepcopy(params)

            for key in params["output"].keys():
                params["output"][key] = list()

            for i in range(n_points):

                for key in sub_params["input"].keys():
                    sub_params["input"][key] = params["input"][key][i]

                sub_params = self.__direct_calculation_passage(sub_params)

                for key in params["output"].keys():
                    params["output"][key].append(sub_params["output"][key])

                self.update_progress_bar()

            self.close_progress_bar()

        else:

            old_use_file = self.__use_input_file
            self.__use_input_file = False

            params = self.__direct_calculation_passage(params)

            self.__use_input_file = old_use_file

        return params

    def __calculate_list(self, params: List[dict]) -> List[dict]:

        return_list = list()

        self.init_progress_bar(len(params))

        for param in params:
            return_list.append(self.__direct_calculation_passage(param))

            self.update_progress_bar()

        self.close_progress_bar()

        return return_list

    def __direct_calculation_passage(self, params: dict) -> dict:

        filename = os.path.join(constants.WORKSPACE_DIR, "ees_input.dat")

        if self.__use_input_file:

            self.__write_input_file(params["input"], filename)

        else:

            self.__define_base_macro(input_params=params["input"], output_params=params["output"])

        try:

            subprocess.run(self.system_command, timeout=self.__timeout, cwd=constants.WORKSPACE_DIR)

        except:

            return params

        else:

            filename = os.path.join(constants.WORKSPACE_DIR, "ees_output.dat")
            return self.__read_output_file(params, filename)

    def __define_base_macro(self, input_params: dict, output_params: dict):

        output_filename = os.path.join(constants.WORKSPACE_DIR, "ees_output.dat")
        if os.path.isfile(output_filename):
            os.remove(output_filename)

        output_params_txt = ""
        for key in output_params.keys():
            output_params_txt += key + " "

        if self.__use_input_file:

            input_params_txt = "Import 'ees_input.dat' f$"
            for key in input_params.keys():
                input_params_txt += " " + key

        else:

            input_params_txt = "f$ = '{}'\n".format(output_filename)
            for key in input_params.keys():
                input_params_txt += key + " = " + str(input_params[key]).replace(".", self.__decimal_separator) + "\n"

        with open(constants.EES_MACRO, "w") as f:

            f.write(

                constants.BASE_MACRO_TXT.format(

                    input_params=input_params_txt,
                    output_params=output_params_txt,
                    calculation_instruction = self.calculation_instruction

                )

            )

    def __write_input_file(self, input_dict: dict, filename: str):

        output_filename = os.path.join(constants.WORKSPACE_DIR, "ees_output.dat")
        if os.path.isfile(output_filename):
            os.remove(output_filename)

        string_to_write = "'" + output_filename + "'"

        for key in input_dict.keys():
            string_to_write += "\t" + str(input_dict[key]).replace(".", self.__decimal_separator)

        with open(filename, "w") as f:
            f.write(string_to_write)

    @staticmethod
    def __read_output_file(params: dict, filename: str) -> dict:

        with open(filename, "r") as f:

            lines = f.readlines()

        keys = list(params["output"].keys())

        for line in lines:

            i = 0
            for element in line.strip("\n").split("\t"):

                try:

                    value = float(element.replace(",", "."))

                except:

                    value = element

                params["output"][keys[i]] = value
                i += 1

        return params

    @property
    def system_command(self) -> str:

        return "{} {} /hide".format(constants.EES_PATH, constants.EES_MACRO)

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

    @classmethod
    def modify_ees_executable_path(cls):

        constants.retrieve_EES_path()

    def update_progress_bar(self):
        if self.__display_progress_bar:
            self.__pbar.update(1)

    def init_progress_bar(self, length):
        if self.__display_progress_bar:
            self.__pbar = tqdm(desc="EES Calculation Ongoing", total=length)

    def close_progress_bar(self):
        if self.__display_progress_bar:
            self.__pbar.close()