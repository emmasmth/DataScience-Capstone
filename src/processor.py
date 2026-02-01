from src.plotter import *

import pandas as pd


def get_age(row):
    """
    Look up age for each respondent
    :param row:
    :return:
    """
    w = row["retire_wave_num"]
    if pd.isna(w):
        return None
    age_col = f"R{int(w)}AGEM_M"
    return row[age_col]


class Processor:
    def __init__(self, df):
        self.df = df

        self.filtered_data = None
        self.first_retired_wave = None
        self.sorted_wave_counts = None
        self.wave_counts = None

        self.add_wave_of_first_retirement()
        self.add_age_of_first_retirement()

    def add_age_of_first_retirement(self):
        age_vars = [f"R{w}AGEM_M" for w in range(1, 17)]
        age_df = self.df[age_vars].copy()

        wave_num = self.first_retired_wave.str.extract(r"R(\d+)").astype(float)[0]

        # Add the wave-number column temporarily
        age_df["retire_wave_num"] = wave_num

        # Compute ages
        self.df["age_at_first_retirement"] = age_df.apply(get_age, axis=1)
        self.df["age_at_first_retirement"] = self.df["age_at_first_retirement"] / 12  # in months so convert to years

        # Show summary
        print(self.df["age_at_first_retirement"].describe())

        self.filtered_data = self.df["age_at_first_retirement"].dropna()

    def add_wave_of_first_retirement(self):
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

        # Make a boolean df: True where the person is retired in that wave
        retired_bool = LBRF_waves.eq("Retired")

        # Get the first wave where retirement occurs
        self.first_retired_wave = retired_bool.idxmax(axis=1)

        # If a person was never retired, idxmax returns the first column, so fix that:
        self.first_retired_wave[~retired_bool.any(axis=1)] = None

        self.wave_counts = self.first_retired_wave.value_counts()
        self.sorted_wave_counts = self.wave_counts.sort_index(key=lambda idx: idx.str.extract(r"R(\d+)")[0].astype(int))

    def plot_waves(self):
        barplot(self.sorted_wave_counts.index, self.sorted_wave_counts.values,
                "Number of First-Time Retirements by Wave", "Wave", "Number of people retiring")

    def plot_age(self):
        boxplot(self.filtered_data, "Distribution of Age at First Retirement", "Age at First Retirement (years)")

