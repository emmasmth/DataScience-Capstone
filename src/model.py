from os import remove

from util import *

class Model:
    def __init__(self, df):
        self.df = df
        # self.df.to_csv("./data/model_df.csv", index=False)

        self.omit_variables()


    def omit_variables(self):
        """
        Drop variables that were used to create the derivative variables. Also drop variables that are related to
        post-retirement (i.e., retire_mon and retire_yr) and "unmeaningful" variables (i.e., r_ID)
        """
        drop_vars = ["r_ID"]
        drop_vars.extend([f"r{w}_labor_status" for w in range(1, 17)])
        drop_vars.extend([f"r{w}_age_yrs_mid" for w in range(1, 17)])
        drop_vars.extend([f"r{w}_retire_mon" for w in range(1, 17)])
        drop_vars.extend([f"r{w}_retire_yr" for w in range(1, 17)])
        self.df = self.df.drop(columns=drop_vars, errors="ignore")