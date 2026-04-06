import numpy as np
import pandas as pd
import pyreadstat

from src.util import *

import time


class DataSet:
    def __init__(self, file_path, cleaned):
        self.file_path = file_path
        self.df = None
        self.RAND_data = pd.DataFrame()

        if cleaned:
            self.load()
        else:
            self.load_sas7bdat()
            self.copy_vars()
            self.find_correlations()
            self.remove_vars()

        self.df.to_csv("./data/cleaned_data.csv", index=False)

    def copy_vars(self):
        """
        Copy and rename all relevant variables to a working df.
        """
        # copy over variables that are NOT wave specific
        set_vars = ["RAHHIDPN", "RABYEAR", "RAGENDER", "RARACEM", "RAEDYRS",
                "RAEDEGRM", "RAEDUC", "RAEVBRN", "RASSAGEM"]

        col_dict = {
            "RASSAGEM": "r_age_ss_payments",
            "RABYEAR": "r_birth_yr",
            "RAEVBRN": "r_child_born",
            "RAEDEGRM": "r_edu_high_deg",
            "RAEDUC": "r_edu_sum",
            "RAEDYRS": "r_edu_yrs",
            "RAGENDER": "r_gender",
            "RAHHIDPN": "r_ID",
            "RARACEM": "r_race"
        }

        wave_vars = {
            "AGEY_M": "age_yrs_mid",
            "MPART": "has_partner",
            "SHLT": "health_self_reported",
            "IEARN": "income",
            "JHOURS": "job_hours",
            "JCIND": "job_industry_1980",
            "JCINDB": "job_industry_2002",
            "JCINDC": "job_industry_2007",
            "JPHYS": "job_physical",
            "JSTRES": "job_stress",
            "LBRF": "labor_status",
            "RETMON": "retire_mon",
            "RETYR": "retire_yr",
            "URBRUR": "urbanicity",
            "ADEBT": "debt",
            "ATOTB": "wealth",
            "CPL": "single_or_couple",
            "ITOT": "total_income"
        }

        # copy over variables that ARE wave specific
        # Hw pre-fix (household)
        Hw_vars = ["ATOTB", "CPL", "ITOT", "ADEBT"]
        for var in Hw_vars:
            set_vars.extend([f"H{w}{var}" for w in range(1, 17)])
            for w in range(1, 17):
                col_dict[f"H{w}{var}"] = f"hh{w}_{wave_vars[var]}"

        # Rw pre-fix (respondent)
        Rw_vars = ["LBRF", "AGEY_M", "MPART", "URBRUR", "SHLT", "JCIND", "JCINDB", "JCINDC",
                   "JPHYS", "JSTRES", "JHOURS", "IEARN", "RETMON", "RETYR"]
        for var in Rw_vars:
            set_vars.extend([f"R{w}{var}" for w in range(1, 17)])
            for w in range(1, 17):
                col_dict[f"R{w}{var}"] = f"r{w}_{wave_vars[var]}"

        set_vars = [var for var in set_vars if col_in_df(self.RAND_data, var)]
        self.df = self.RAND_data[set_vars].copy()
        self.df.rename(columns=col_dict, inplace=True)

    def copy_vars_limited(self):
        """
        Creating a limited-variable dataframe. Only including non-wave variables, in addition
        to RwLBRF and Rw_AGEY_M, which are variables that directly inform us of retirement success
        and timing.

        Note that this function does NOT save to self.df. It only creates a csv file for now.
        """
        col_dict = {
            "RASSAGEM": "r_age_ss_payments",
            "RABYEAR": "r_birth_yr",
            "RAEVBRN": "r_child_born",
            "RAEDEGRM": "r_edu_high_deg",
            "RAEDUC": "r_edu_sum",
            "RAEDYRS": "r_edu_yrs",
            "RAGENDER": "r_gender",
            "RAHHIDPN": "r_ID",
            "RARACEM": "r_race"
        }

        wave_vars = {
            "LBRF": "labor_status",
            "_AGEY_M": "age_yrs_mid",
        }

        # copy over variables that are NOT wave specific
        set_vars = ["RAHHIDPN", "RABYEAR", "RAGENDER", "RARACEM", "RAEDYRS",
                "RAEDEGRM", "RAEDUC", "RAEVBRN", "RASSAGEM"]

        # Rw pre-fix (respondent)
        Rw_vars = ["LBRF", "_AGEY_M"]
        for var in Rw_vars:
            set_vars.extend([f"R{w}{var}" for w in range(1, 17)])
            for w in range(1, 17):
                col_dict[f"R{w}{var}"] = f"r{w}_{wave_vars[var]}"

        set_vars = [var for var in set_vars if col_in_df(self.RAND_data, var)]
        limited_df = self.RAND_data[set_vars].copy()
        limited_df.rename(columns=col_dict, inplace=True)
        save_as_csv(limited_df, filename="limited_data.csv")

    def find_correlations(self):
        """
        Find high correlations (defined as correlation coefficient > 0.90) among respondent (non-wave) variables
        """
        threshold = 0.90

        cols = ["r_age_ss_payments", "r_birth_yr", "r_child_born", "r_edu_high_deg",
            "r_gender", "r_ID", "r_race", "r_edu_sum", "r_edu_yrs"]
        corr_matrix = self.df[cols].corr()
        # corr_matrix.to_csv("./data/corr_matrix_respondent_vars.csv")

        high_corr_pairs = (
            corr_matrix
            .where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
            .stack()
            .loc[lambda x: x > threshold]
            .sort_values(ascending=False)
        )

        # Print highly correlated pairs
        print_separator()
        print("Finding highly correlated variables...\n")
        for (var1, var2), corr in high_corr_pairs.items():
            _, _, substr1 = var1.partition("_")
            _, _, substr2 = var2.partition("_")
            if substr1 != substr2:
                print("\t", var1, var2, corr)

    def get_dataframe(self):
        """
        Getter function.
        """
        return self.df

    def load(self):
        """
        If using cleaned dataset, read in csv.
        """
        self.df = pd.read_csv(self.file_path)

    def load_sas7bdat(self):
        """
        Load Dataset from sas7bdat file.
        :return: self.RAND_data - dataset as type dataframe.
        """
        print_separator()
        print("Starting to load file ... ")
        load_start_time = time.time()
        self.RAND_data, meta = pyreadstat.read_sas7bdat(self.file_path)
        load_end_time = time.time()
        print("File load complete! Took " + str(round(load_end_time - load_start_time, 2)) + " seconds")

    def remove_vars(self):
        """
        Remove variables that are highly correlated. We want to keep the r_edu_high_deg variable since it has the
        most categories. This function removes the r_edu_sum and r_edu_yrs variables.
        """
        self.df = self.df.drop(columns=["r_edu_sum", "r_edu_yrs"], errors="ignore")
