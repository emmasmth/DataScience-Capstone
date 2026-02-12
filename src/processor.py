from interface import *
from src.plotter import *
from src.util import *

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
    age_col = f"R{int(w)}AGEY_M"
    return row[age_col]


class Processor:
    def __init__(self, df):
        self.df = df
        self.cleaned_df = pd.DataFrame()

        self.filtered_data = None
        self.first_retired_wave = None
        self.sorted_wave_counts = None
        self.wave_counts = None

        self.add_wave_of_first_retirement()
        self.add_age_of_first_retirement()

        # print_dataframe("cleaned_df", self.cleaned_df)

    def add_age_of_first_retirement(self):
        """
        RwAGEY_M is the Age in years at the midpoint between the beginning and ending interview dates.
        This function finds the age of a person when they first retire. (See page 140 of reference document).
        """
        # Get age during midpoint of each wave interview
        age_vars = [f"R{w}AGEY_M" for w in range(1, 17)]
        age_df = self.df[age_vars].copy()

        # Get wave where person first becomes retired or presumed retired
        wave_num = self.first_retired_wave.str.extract(r"R(\d+)").astype(float)[0]

        # Add the wave num column temporarily
        age_df["retire_wave_num"] = wave_num

        # Compute ages
        self.df["age_at_first_retirement"] = age_df.apply(get_age, axis=1)

        # Show summary
        # print(self.df["age_at_first_retirement"].describe())

        # Filter data for only those who are retired or presumed retired (for plotting)
        self.filtered_data = self.df["age_at_first_retirement"].dropna()

        # Add columns to cleaned dataframe
        self.cleaned_df["wave_of_first_retirement"] = age_df["retire_wave_num"].astype('Int64')
        self.cleaned_df["age_at_first_retirement"] = self.df["age_at_first_retirement"]


    def add_wave_of_first_retirement(self):
        """
        RwLBRF summarizes the labor force status for the Respondent at each wave as working full-time,
        working part-time, unemployed, partly retired, retired, disabled, or not in the labor force.
        (See page 1900 of reference document).
        """
        # There are waves numbered 1 (1992) to 16 (2022)
        waves = [f"R{w}LBRF" for w in range(1, 17)]  # there are waves numbered 1 to 16
        LBRF_waves = self.df[waves].copy()  # waves is already a list so don't need to do double square brackets

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
            LBRF_waves[wave] = LBRF_waves[wave].map(mapping).astype("category")

        # Make a boolean df: True where the person is retired (or presumed retired) in that wave
        retired_bool = LBRF_waves.isin(["Retired", "Presumed retired"])

        # Get the first wave where retirement occurs
        self.first_retired_wave = retired_bool.idxmax(axis=1)

        # If a person was never retired, idxmax returns the first column, so fix that:
        self.first_retired_wave[~retired_bool.any(axis=1)] = None

        # Get how many people retired in each wave
        self.wave_counts = self.first_retired_wave.value_counts()
        self.sorted_wave_counts = self.wave_counts.sort_index(key=lambda idx: idx.str.extract(r"R(\d+)")[0].astype(int))


    def plot_waves(self):
        title = "Number of First-Time Retirements by Wave"
        plot = confirm_print("Barplot: " + title, "plot")
        if plot:
            barplot(self.sorted_wave_counts.index, self.sorted_wave_counts.values, title,
                    "Wave", "Number of people retiring")

    def plot_age(self):
        title = "Distribution of Age at First Retirement"
        plot = confirm_print("Boxplot: " + title, "plot")
        if plot:
            boxplot(self.filtered_data, title,"Age at First Retirement (years)")

