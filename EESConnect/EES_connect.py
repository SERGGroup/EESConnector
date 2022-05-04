import EESConnect.constants as constants
from tkinter import filedialog
import tkinter as tk
import shutil, os


class EESConnector:

    def __init__(self, ees_file_path=None, keep_refprop=False):

        self.__clear_files()
        self.__with_initialization = False
        self.__keep_refprop = keep_refprop
        self.__ees_file_path = None

        if ees_file_path is not None:
            self.ees_file_path = ees_file_path

    def __enter__(self):

        self.__with_initialization = True
        self.__move_REFPROP_DIR(move_away=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.quit()

    def calculate(self, input_list):

        if self.is_ready:

            self.__prepare_input(input_list)

        try:

            system_comand = "{} {}".format(constants.EES_PATH, constants.EES_MACRO)
            os.chdir(constants.WORKSPACE_DIR)
            os.system(system_comand)

        except:

            return None

        else:

            return self.__collect_output()

    def quit(self):

        self.__move_REFPROP_DIR(move_away=False)
        if self.is_ready:
            # This part delete the file used for data IO
            self.__clear_files()

    def __prepare_input(self, input_list):

        if type(input_list) == list:

            self.__write_input_file(input_list, "default")
            last_file_path = os.path.join(constants.WORKSPACE_DIR, "default" + constants.IO_FILE_EXTENSION)

        elif type(input_list) == dict:

            key = "1"
            for key in input_list.keys():

                self.__write_input_file(input_list[key], key)

            last_file_path = os.path.join(constants.WORKSPACE_DIR, key + constants.IO_FILE_EXTENSION)

        else:
            return

        shutil.copy(last_file_path, os.path.join(constants.WORKSPACE_DIR, constants.EES_INPUT_FILENAME))

    def __collect_output(self):

        return_dict = dict()

        for file in os.listdir(constants.WORKSPACE_DIR):

            if file.endswith(constants.IO_FILE_EXTENSION):

                key = file.strip(constants.IO_FILE_EXTENSION)

                return_dict.update({

                    key: self.__read_output_file(key)

                })

        if "default" in return_dict.keys():

            return return_dict["default"]

        else:

            return return_dict

    def __move_REFPROP_DIR(self, move_away):

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

    @staticmethod
    def __write_input_file(input_list, filename):

        string_to_write = input_list[0]

        for element in input_list[1:]:
            string_to_write += "\t" + str(element)

        with open(os.path.join(constants.WORKSPACE_DIR, filename + constants.IO_FILE_EXTENSION), "w") as f:
            f.write(string_to_write)

    @staticmethod
    def __read_output_file(filename):

        with open(os.path.join(constants.WORKSPACE_DIR, filename + constants.IO_FILE_EXTENSION), "r") as f:

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
    def __clear_files():

        for file in os.listdir(constants.WORKSPACE_DIR):
            if file.endswith(constants.IO_FILE_EXTENSION) or file.endswith(".ees") or file.endswith(".dat") or file.endswith(".DAT"):
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


if __name__ == "__main__":

    with EESConnector() as connector:

        connector.select_file()
        # result = connector.calculate({
        #
        #     "1": ["air_ha", 300, 1013.25],
        #     "2": ["R22", 300, 1013.25],
        #     "3": ["R236fa", 300, 1013.25],
        #     "4": ["R134a", 300, 1013.25],
        #     "5": ["R236fa", 300, 1013.25],
        #     "6": ["R134a", 300, 1013.25],
        #     "7": ["R236fa", 300, 1013.25],
        #     "8": ["R134a", 300, 1013.25]
        #
        # })
        result = connector.calculate(["air_ha", 300, 1013.25])
        print(result)