import EESConnect.constants as constants
from tkinter import filedialog
import tkinter as tk
import shutil, os


class EESConnector:

    def __init__(self, ees_file_path=None, keep_refprop=False):

        self.__with_initialization = False
        self.__keep_refprop = keep_refprop

        self.__ees_file_path = None
        self.__ees_file_directory = None
        self.__ees_input_file = None
        self.__ees_output_file = None

        if ees_file_path is not None:
            self.ees_file_path = ees_file_path

    def __enter__(self):

        self.__with_initialization = True

        if os.path.isdir(constants.EES_REFPROP_DIR) and not self.__keep_refprop:
            # This part of the code moves the EES-REFPROP plugin folder away from its correct location in order to
            # prevent the plugin from asking the user the position of the Refprop folder on each iteration.
            #
            # If refprop is needed for the calculation the
            shutil.move(constants.EES_REFPROP_DIR, constants.EES_REFPROP_TMP_DIR)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        if os.path.isdir(constants.EES_REFPROP_TMP_DIR):
            # This part of the code moves the EES-REFPROP plugin folder back in its correct location in order to
            # restore the plugin functionality

            shutil.move(constants.EES_REFPROP_TMP_DIR, constants.EES_REFPROP_DIR)

        if self.is_ready:

            # This part delete the file used for data IO

            for file in [self.__ees_input_file, self.__ees_output_file]:
                if os.path.exists(file):
                    os.remove(file)

    def calculate(self, input_list):

        if self.is_ready:

            string_to_write = input_list[0]

            for element in input_list[1:]:
                string_to_write += "\t" + str(element)

            with open(self.__ees_input_file, "w") as f:

                f.write(string_to_write)

            with open(self.__ees_output_file, "w") as f:

                f.write("")

        try:

            system_comand = "{} {} /solve".format(constants.EES_PATH, self.__ees_file_path)
            os.system(system_comand)

        except:

            return None

        else:

            with open(self.__ees_output_file, "r") as f:

                lines = f.readlines()

            return_list = list()

            for line in lines:

                sublist = list()

                for element in line.strip("\n").split("\t"):

                    try:

                        sublist.append(float(element.replace(",", ".")))

                    except:

                        sublist.append(element)

                return_list.append(sublist)

            return return_list

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
            self.__ees_file_directory = os.path.dirname(ees_file_path)
            self.__ees_input_file = os.path.join(self.__ees_file_directory, "ees_input.dat")
            self.__ees_output_file = os.path.join(self.__ees_file_directory, "ees_output.dat")

    @classmethod
    def modify_ees_executable_path(cls):

        constants.retrieve_EES_path()


if __name__ == "__main__":

    with EESConnector() as connector:

        connector.select_file()
        result = connector.calculate(["air_ha", 150, 1013.25])
        print(result)
