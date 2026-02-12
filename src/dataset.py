import pandas as pd

from src.util import *

import os
import time

import pyreadstat


class DataSet:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.cleaned_data = pd.DataFrame()

        self.load()

    def clean(self):
        self.copy_vars()
        self.find_correlations()
        self.remove_vars()

    def col_in_df(self, col):
        if col in self.df.columns:
            return True
        else:
            return False

    def copy_vars(self):
        # copy over variables that are NOT wave specific
        set_vars = ["RAHHIDPN", "RABYEAR", "RAGENDER", "RARACEM", "RAEDYRS",
                "RAEDEGRM", "RAEDUC", "RAEVBRN", "RASSAGEM"]

        # copy over variables that ARE wave specific
        # Hw pre-fix (household)
        Hw_vars = ["ATOTB", "CPL", "ITOT", "ADEBT"]
        for var in Hw_vars:
            set_vars.extend([f"H{w}{var}" for w in range(1, 17)])

        # Rw pre-fix (respondent)
        Rw_vars = ["LBRF", "AGEY_M", "MPART", "URBRUR", "SHLT", "JCIND", "JCINDB", "JCINDC",
                   "JPHYS", "JSTRES", "JHOURS", "IEARN", "RETMON", "RETYR"]
        for var in Rw_vars:
            set_vars.extend([f"R{w}{var}" for w in range(1, 17)])

        set_vars = [var for var in set_vars if self.col_in_df(var)]
        self.cleaned_data = self.df[set_vars].copy()

        print(self.cleaned_data.shape[1])

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

    def find_correlations(self):
        # col1.corr(col2)
        pass

    def remove_vars(self):
        pass