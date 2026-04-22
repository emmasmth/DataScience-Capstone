from src.plotter import *
from src.interface import *

import pandas as pd


def get_age(row):
    """
    Look up age for each respondent
    :param row: the row representing a respondent
    :return: the age of the respondent
    """
    w = row["retire_wave_num"]
    if pd.isna(w):
        return None
    age_col = f"r{int(w)}_age_yrs_mid"
    return row[age_col]

def get_nw(row):
    """
    Look up net worth for each respondent
    :param row: the row representing a respondent
    :return: the net worth of the respondent
    """
    w = row["retire_wave_num"]
    if pd.isna(w):
        return None
    nw_col = f"hh{int(w)}_wealth"
    return row[nw_col]


class Processor:
    def __init__(self, df):
        self.df = df
        self.new_df = pd.DataFrame()

        self.filtered_age_data = None
        self.filtered_worth_data = None
        self.sorted_wave_counts = None
        self.wave_counts = None

        self.derive_first_retirement_info()

        # print_dataframe("new_df", self.new_df)

    def derive_first_retirement_info(self):
        """
        r{w}_labor_status, originally LBRF, summarizes the labor force status for the Respondent at each wave as
        working full-time, working part-time, unemployed, partly retired, retired, disabled, or not in the
        labor force. (See page 1900 of reference document).

        r{w}_age_yrs_mid, originally RwAGEY_M, is the Age in years at the midpoint between the beginning and ending
        interview dates. This function finds the age of a person when they first retire. (See page 140 of
        reference document).
        """

        # --------------WAVE Derivation--------------

        # There are waves numbered 1 (1992) to 16 (2022)
        waves = [f"r{w}_labor_status" for w in range(1, 17)]  # there are waves numbered 1 to 16
        labor_df = self.df[waves].copy()  # waves is already a list so don't need to do double square brackets

        mapping = {
            "A": "Presumed retired",
            "Q": "Not asked",
            "T": "Worked last 2 years, not now",
            1: "Works FT",
            2: "Works PT",
            3: "Unemployed",
            4: "Partly retired",
            5: "Retired",
            6: "Disabled",
            7: "Not in LBRF"
        }

        # Switch LBRF variables to be categorical
        for wave in waves:
            labor_df[wave] = labor_df[wave].map(mapping).astype("category")

        # Make a boolean df: True where the person is retired (or presumed retired) in that wave
        retired_bool = labor_df.isin(["Retired", "Presumed retired"])

        # Get the first wave where retirement occurs
        first_retired_wave = retired_bool.idxmax(axis=1)

        # If a person was never retired, idxmax returns the first column, so fix that:
        first_retired_wave[~retired_bool.any(axis=1)] = None

        # Get how many people retired in each wave
        self.wave_counts = first_retired_wave.value_counts()
        self.sorted_wave_counts = self.wave_counts.sort_index(key=lambda idx: idx.str.extract(r"r(\d+)")[0].astype(int))

        # Get wave where person first becomes retired or presumed retired
        wave_num = first_retired_wave.str.extract(r"r(\d+)").astype(float)[0]

        # --------------AGE Derivation--------------

        # Get age during midpoint of each wave interview
        age_vars = [f"r{w}_age_yrs_mid" for w in range(1, 17)]
        age_df = self.df[age_vars].copy()

        # Add the wave num column temporarily
        age_df["retire_wave_num"] = wave_num

        # Compute ages
        self.df["age_at_first_retirement"] = age_df.apply(get_age, axis=1)

        # Show summary
        print_separator()
        print("Age at First Retirement Statistics")
        print(self.df["age_at_first_retirement"].describe())

        # Filter data for only those who are retired or presumed retired (for plotting)
        self.filtered_age_data = self.df["age_at_first_retirement"].dropna()

        # --------------NET WORTH Derivation--------------

        # Get net worth at each wave
        nw_vars = [f"hh{w}_wealth" for w in range(1, 17)]
        nw_df = self.df[nw_vars].copy()

        # Add the wave num column temporarily
        nw_df["retire_wave_num"] = wave_num

        # Compute wealth
        self.df["net_worth_at_first_retirement"] = nw_df.apply(get_nw, axis=1)

        # Show summary
        pd.set_option('display.float_format', '{:,.2f}'.format)
        print_separator()
        print("Net Worth Summary Statistics")
        print(self.df["net_worth_at_first_retirement"].describe())

        # Filter data for only those who are retired or presumed retired (for plotting)
        self.filtered_worth_data = self.df["net_worth_at_first_retirement"].dropna()

        # --------------New Dataframe--------------

        # Add column to new dataframe
        self.new_df = self.df.copy()
        self.new_df = self.new_df.assign(
            wave_of_first_retirement=age_df["retire_wave_num"].astype("Int64")
        )

    def get_df(self):
        """
        Getter function.
        """
        return self.df

    def get_new_df(self):
        """
        Getter function.
        """
        if self.new_df.empty:
            print("Warning! No new data. Please run processor to update.")
        return self.new_df

    def plot_age(self):
        """
        Plot age at retirement variable as a boxplot. Using filtered data that does not include respondents that
        have not yet retired.
        """
        title = "Distribution of Age at First Retirement"
        plot = confirm_print("Boxplot: " + title, "plot")
        if plot:
            print(self.filtered_age_data.describe())
            print(self.filtered_age_data.shape)
            boxplot(self.filtered_age_data, title,"Age at First Retirement (years)", "")

    def plot_waves(self):
        """
        Plot distribution of retirement waves as barplot. Using filtered data that does not include respondents that
        have not yet retired.
        """
        title = "Number of First-Time Retirements by Wave"
        plot = confirm_print("Barplot: " + title, "plot")
        if plot:
            barplot(self.sorted_wave_counts.index, self.sorted_wave_counts.values, title,
                    "Wave", "Number of people retiring")

    def plot_nw(self):
        """
        Plot distribution of net worth at retirement. Using filtered data that does not include respondents that
        have not yet retired.
        """
        title = "Distribution of Net Worth at First Retirement"
        plot = confirm_print("Boxplot: " + title, "plot")
        if plot:
            # print(self.filtered_worth_data.describe())
            # print(self.filtered_worth_data.shape)
            boxplot(self.filtered_worth_data, title, "Net Worth at First Retirement $","")