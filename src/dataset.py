from src.util import *

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
        print_separator()
        print("Starting to load file ... ")
        load_start_time = time.time()
        self.df, meta = pyreadstat.read_sas7bdat(self.file_path)
        load_end_time = time.time()
        print("File load complete! Took " + str(round(load_end_time - load_start_time, 2)) + " seconds")

        return self.df

