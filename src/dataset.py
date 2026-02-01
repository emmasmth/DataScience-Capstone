import os
import time

import pyreadstat


class DataSet:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.load()

    def load(self):
        """
        Load Dataset from sas7bdat file.
        :return: self.df - dataset as type dataframe.
        """
        if os.path.exists(self.file_path):
            print(f"The file '{self.file_path}' exists.")
        else:
            print(f"The file '{self.file_path}' does not exist.")

        print("\nStarting to load file ... ")
        load_start_time = time.time()
        self.df, meta = pyreadstat.read_sas7bdat(self.file_path)
        load_end_time = time.time()
        print("File load complete! Took " + str(load_end_time - load_start_time) + " seconds")
        return self.df

