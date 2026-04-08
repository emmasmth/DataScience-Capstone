from os import remove

import numpy as np
import pandas as pd

import util
from util import *

class Model:
    def __init__(self, df):
        self.df = df
        self.working_df = pd.DataFrame()
        # self.omit_variables()
        # self.df.to_csv("./data/model_df.csv", index=False)

        self.add_variables()
        self.prep()
        self.working_df.to_csv("./data/model_df.csv", index=False)

        # for col in self.working_df.columns:
        #     print(col)

        self.eval_corr()
        self.model_age()

    def add_variables(self):
        """
        Add basic variables to the working df
        """
        vars_to_add = ["age_at_first_retirement", "net_worth_at_first_retirement", "wave_of_first_retirement",
                       "r_age_ss_payments", "r_birth_yr", "r_child_born", "r_edu_high_deg", "r_gender", "r_race"]
        self.working_df = self.df[vars_to_add].copy()

    def clean_hhcol(self, col_name):
        """
        Using hh wave variables, get an average variable and a growth (last occurrence - first occurrence)
        Then add to working df
        """
        wave_cols = [f"hh{w}_{col_name}" for w in range(1, 17)]
        wave_cols = [col for col in wave_cols if col in self.df.columns]

        if not wave_cols:
            return

        temp_df = self.df[wave_cols].copy()
        temp_df = temp_df.apply(pd.to_numeric, errors="coerce")

        avg = temp_df.mean(axis=1)
        first = temp_df.bfill(axis=1).iloc[:, 0]
        last = temp_df.ffill(axis=1).iloc[:, -1]
        growth = last - first

        avg_col_name = f"hh_{col_name}_avg"
        growth_col_name = f"hh_{col_name}_growth"
        self.working_df = self.working_df.assign(**{
            avg_col_name: avg,
            growth_col_name: growth
        })

    def clean_rcol(self, col_name):
        """
        For respondent wave variables, make non-numeric answers NaNs, then get a numerical average
        across all waves to use for model
        """
        wave_cols = [f"r{w}_{col_name}" for w in range(1, 17)]
        wave_cols = [col for col in wave_cols if col in self.df.columns]

        temp_df = self.df[wave_cols].copy()
        temp_df = temp_df.replace({
            "B": np.nan,
            "D": np.nan,
            "J": np.nan,
            "M": np.nan,
            "N": np.nan,
            "P": np.nan,
            "Q": np.nan,
            "R": np.nan,
            "S": np.nan,
            "W": np.nan
        })
        temp_df = temp_df.apply(pd.to_numeric, errors="coerce")
        avg = temp_df.mean(axis=1)

        new_col = f"r_{col_name}_avg"
        self.working_df = self.working_df.assign(**{new_col: avg})

    def eval_corr(self):
        corr = self.working_df.corr().abs()
        threshold = 0.9

        # Get upper triangle only (avoid duplicates)
        upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))

        # Find high correlations
        high_corr = upper.stack().sort_values(ascending=False)

        if high_corr[high_corr > threshold].empty:
            print_separator()
            print("There are no highly correlated variables!")

        else:
            print_separator()
            print("There are highly correlated variables :(")
        # print(high_corr[high_corr > threshold])

    def model_age(self):
        age_df = self.working_df.copy()
        print(age_df.shape)
        age_df = age_df.dropna(subset=["age_at_first_retirement"])
        print(age_df.shape)

    def omit_variables(self):
        """
        Not going to use
        But would remove unused variables from self.df

        Drop "unmeaningful" variables (i.e., r_ID).
        Drop derivative variables.
        Drop variables that were used to create the derivative variables.
        Drop post-retirement variables(i.e., retire_mon and retire_yr).
        """
        drop_vars = ["r_ID"]
        drop_vars.extend(["age_at_first_retirement", "net_worth_at_first_retirement", "wave_of_first_retirement"])
        drop_vars.extend([f"r{w}_labor_status" for w in range(1, 17)])
        drop_vars.extend([f"r{w}_age_yrs_mid" for w in range(1, 17)])
        drop_vars.extend([f"r{w}_retire_mon" for w in range(1, 17)])
        drop_vars.extend([f"r{w}_retire_yr" for w in range(1, 17)])
        self.df = self.df.drop(columns=drop_vars, errors="ignore")

    def prep(self):
        """
        Prep variables into a single working_df to use for modeling
        """
        rcols_to_convert = ["health_self_reported", "job_physical", "job_stress", "urbanicity",
                           "has_partner", "job_hours"] # ", income"
        for col in rcols_to_convert:
            self.clean_rcol(col)

        # for col in cols_to_convert:
        #     new_col = f"{col}_avg"
        #     print(new_col + " " + str(self.df[new_col].dtype))
        #     print(self.df[new_col].describe())
        #     print()

        hhcols_to_convert = ["debt", "wealth", "total_income"]
        for col in hhcols_to_convert:
            self.clean_hhcol(col)

        # relationship = [f"hh{w}_single_or_couple" for w in range(1, 17)]
        # temp_df = self.df[relationship].copy()
        # temp_df = temp_df.apply(pd.to_numeric, errors="coerce")
        # avg = temp_df.mean(axis=1)
        # self.working_df = self.working_df.assign(**{"hh_single_or_couple_avg": avg})

        # calc ratios
        self.working_df["hh_debt_to_wealth"] = self.working_df["hh_debt_avg"] / (self.working_df["hh_wealth_avg"] + 1)
        self.working_df["hh_income_to_wealth"] = self.working_df["hh_total_income_avg"] / (self.working_df["hh_wealth_avg"] + 1)