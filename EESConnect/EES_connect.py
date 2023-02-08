import EESConnect.constants as constants
from tkinter import filedialog
import tkinter as tk
import shutil, os


class EESConnector:

    def __init__(self, ees_file_path=None, keep_refprop=False, solve_with_macro=False):

        self.__clear_files()

        self.__ees_file_path = None
        self.__with_initialization = False
        self.__keep_refprop = keep_refprop
        self.__solve_with_macro = solve_with_macro

        if ees_file_path is not None:
            self.ees_file_path = ees_file_path

    def __enter__(self):

        self.__with_initialization = True
        self.move_REFPROP_DIR(move_away=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.quit()

    def calculate(self, input_list):

        if self.is_ready:

            if self.__solve_with_macro:

                return self.__calculate_with_macro(input_list)

            else:

                return self.__calculate_directly(input_list)

    def quit(self):

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

    def __calculate_directly(self, input_list):

        if type(input_list) == list:

            return self.__direct_calculation_passage(input_list)

        elif type(input_list) == dict:

            return_dict = dict()

            for key in input_list.keys():

                return_dict.update({

                    key: self.__direct_calculation_passage(input_list[key])

                })

            return return_dict

        else:

            return None

    def __direct_calculation_passage(self, input_list):

        filename = os.path.join(constants.WORKSPACE_DIR, "ees_input.dat")
        self.__write_input_file(input_list, filename)

        try:

            system_comand = "{} {} /solve /hide".format(constants.EES_PATH, constants.EES_RUN_FILENAME)
            os.chdir(constants.WORKSPACE_DIR)
            os.system(system_comand)

        except:

            return None

        else:

            filename = os.path.join(constants.WORKSPACE_DIR, "ees_output.dat")
            return self.__read_output_file(filename)

    def __calculate_with_macro(self, input_list):

        if len(input_list) == 1:

            return self.__calculate_directly(input_list)

        else:

            self.__prepare_macro_input(input_list)

            try:

                system_comand = "{} {} /hide".format(constants.EES_PATH, constants.EES_MACRO)
                os.chdir(constants.WORKSPACE_DIR)
                os.system(system_comand)

            except:

                return None

            else:

                return self.__collect_macro_output()

    def __prepare_macro_input(self, input_list):

        if type(input_list) == list:

            filename = os.path.join(constants.WORKSPACE_DIR, "default" + constants.IO_FILE_EXTENSION)
            self.__write_input_file(input_list, filename)

        elif type(input_list) == dict:

            filename = os.path.join(constants.WORKSPACE_DIR, "1" + constants.IO_FILE_EXTENSION)
            for key in input_list.keys():
                filename = os.path.join(constants.WORKSPACE_DIR, key + constants.IO_FILE_EXTENSION)
                self.__write_input_file(input_list[key], filename)

        else:
            return

        shutil.copy(filename, os.path.join(constants.WORKSPACE_DIR, constants.EES_INPUT_FILENAME))

    def __collect_macro_output(self):

        return_dict = dict()

        for file in os.listdir(constants.WORKSPACE_DIR):

            if file.endswith(constants.IO_FILE_EXTENSION):

                filename = os.path.join(constants.WORKSPACE_DIR, file)
                key = file.strip(constants.IO_FILE_EXTENSION)

                return_dict.update({

                    key: self.__read_output_file(filename)

                })

        self.__clear_files(clear_only_input_files=True)

        if "default" in return_dict.keys():

            return return_dict["default"]

        else:

            return return_dict

    @staticmethod
    def __write_input_file(input_list, filename):

        output_filename = os.path.join(constants.WORKSPACE_DIR, "ees_output.dat")
        string_to_write = output_filename

        for element in input_list:
            string_to_write += "\t" + str(element)

        string_to_write = string_to_write.replace(".", ",")

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
    def ees_file_path(self):
        return self.__ees_file_path

    @property
    def is_ready(self):

        return self.__ees_file_path is not None

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

    @classmethod
    def modify_macro_delay(cls, delay_ms):

        constants.set_macro(delay_ms)


if __name__ == "__main__":

    import time

    n_calculations = 32
    calculate_with_macro = True
    input_dict = dict()

    T_amb = 15
    T_BHE_in = 30
    T_BHE_out = 100
    P_BHE_in = 8000
    P_BHE_out = 15000
    steam_production = 1
    P_steam = 1000
    P_SG_perc = 0.5
    dT_SG_pinch = 10

    for i in range(n_calculations):

        P_SG_perc = (float(i) / n_calculations) * (0.7 - 0.2) + 0.2

        input_dict.update({

            str(P_SG_perc): [

                "CarbonDioxide", T_amb,
                T_BHE_in, T_BHE_out, P_BHE_in, P_BHE_out,
                steam_production, P_steam, P_SG_perc, dT_SG_pinch

            ]

        })

    with EESConnector(solve_with_macro=calculate_with_macro) as connector:

        connector.select_file()
        start = time.time()
        result = connector.calculate(input_dict)
        print(result)

    print("\n\ttime elapsed = {} s\n".format(time.time() - start))