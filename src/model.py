from os import remove

import numpy as np
import pandas as pd
import sklearn.linear_model, sklearn.metrics, sklearn.model_selection

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
        self.model_age_linear()
        self.model_age_forest()

        self.model_worth_linear()
        self.model_worth_forest()

    def add_variables(self):
        """
        Add basic variables to the working df
        """
        vars_to_add = ["age_at_first_retirement", "net_worth_at_first_retirement", "wave_of_first_retirement",
                       "r_age_ss_payments", "r_birth_yr", "r_child_born"]
        self.working_df = self.df[vars_to_add].copy()

    def clean_nonwave(self, col_name):
        if col_name not in self.df.columns:
            return

        temp_df = self.df[[col_name]].copy()
        temp_df[col_name] = temp_df[col_name].replace({"M": np.nan})

        # Create dummies
        temp_df = pd.get_dummies(
            temp_df,
            columns=[col_name],
            drop_first=True
        )

        self.working_df = self.working_df.assign(**temp_df)


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
        if not wave_cols:
            return

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
        print_separator()

        if high_corr[high_corr > threshold].empty:
            print("There are no highly correlated variables!")

        else:
            print("There are highly correlated variables :(")
        # print(high_corr[high_corr > threshold])

    def model_age_forest(self):
        pd.set_option('display.float_format', '{:.6f}'.format)

        age_df = self.working_df.copy()
        # print(age_df.shape)

        # drop respondents that have not yet retired
        age_df = age_df.dropna(subset=["age_at_first_retirement"])
        # print(age_df.shape)

        print_separator()
        print("Random Forest Regression: Age")
        print(f"Run #1")

        y = age_df["age_at_first_retirement"]
        x = age_df.drop(columns=["age_at_first_retirement", "net_worth_at_first_retirement",
                                 "wave_of_first_retirement"])

        x = x.drop(columns=["r_age_ss_payments"])

        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(
            x, y, test_size=0.2, random_state=42
        )

        x_train = x_train.fillna(x_train.mean())
        x_test = x_test.fillna(x_train.mean())

        rf = sklearn.ensemble.RandomForestRegressor(n_estimators=200, random_state=42)
        rf.fit(x_train, y_train)

        rf.fit(x_train, y_train)
        preds = rf.predict(x_test)

        r2 = sklearn.metrics.r2_score(y_test, preds)
        mae = sklearn.metrics.mean_absolute_error(y_test, preds)

        print("Random Forest Results")
        print("---------------------")
        print(f"R²: {r2:.4f}")
        print(f"MAE: {mae:.4f}")

        importance = pd.Series(
            rf.feature_importances_,
            index=x_train.columns
        ).sort_values(ascending=False)

        print("\nTop 10 Important Features:")
        print(importance.head(10))

    def model_age_linear(self):
        pd.set_option('display.float_format', '{:.6f}'.format)

        age_df = self.working_df.copy()
        # print(age_df.shape)

        # drop respondents that have not yet retired
        age_df = age_df.dropna(subset=["age_at_first_retirement"])
        # print(age_df.shape)

        print_separator()
        print("Linear Regression: Age")
        print(f"Run #1")
        print("Variable overview")
        for col, dtype in age_df.dtypes.items():
            print(f"Column: {col}, Type: {dtype}")

        y = age_df["age_at_first_retirement"]
        x = age_df.drop(columns=["age_at_first_retirement", "net_worth_at_first_retirement",
                                 "wave_of_first_retirement"])

        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(
            x, y, test_size=0.2, random_state=42
        )

        x_train = x_train.fillna(x_train.mean())
        x_test = x_test.fillna(x_train.mean())

        model = sklearn.linear_model.LinearRegression()
        model.fit(x_train, y_train)

        preds = model.predict(x_test)

        r2 = sklearn.metrics.r2_score(y_test, preds)
        mae = sklearn.metrics.mean_absolute_error(y_test, preds)

        print()
        print("\tR²:", r2)
        print("\tMAE:", mae)

        # coefficients
        coef_df = pd.Series(model.coef_, index=x_train.columns).sort_values()
        print("\nCoefficients:")
        print(coef_df)

        lasso = sklearn.linear_model.Lasso(alpha=0.1)
        lasso.fit(x_train, y_train)

        lasso_coef = pd.Series(lasso.coef_, index=x_train.columns)
        print("\nLasso coefficients:")
        print(lasso_coef.sort_values())

        to_drop = lasso_coef[abs(lasso_coef) < 1e-5].index
        print("\nVariables to drop next round: " + str(len(to_drop)))
        print(to_drop)

        x_train_reduced = x_train.drop(columns=to_drop)
        x_test_reduced = x_test.drop(columns=to_drop)

        model_reduced = sklearn.linear_model.LinearRegression()
        model_reduced.fit(x_train_reduced, y_train)

        preds_reduced = model_reduced.predict(x_test_reduced)

        print_separator()
        print("Run #2 (Reduced Model)")

        r2_reduced = sklearn.metrics.r2_score(y_test, preds_reduced)
        mae_reduced = sklearn.metrics.mean_absolute_error(y_test, preds_reduced)

        print("\n\tR²:", r2_reduced)
        print("\tMAE:", mae_reduced)

        coef_reduced = pd.Series(model_reduced.coef_, index=x_train_reduced.columns).sort_values()
        print("\nCoefficients:")
        print(coef_reduced)

    def model_worth_forest(self):
        pd.set_option('display.float_format', '{:.6f}'.format)

        worth_df = self.working_df.copy()

        worth_df = worth_df.dropna(subset=["net_worth_at_first_retirement"])
        worth_df = worth_df[worth_df["net_worth_at_first_retirement"] > -1]

        print_separator()
        print("Random Forest Regression: Net Worth")

        y = np.log1p(worth_df["net_worth_at_first_retirement"])

        x = worth_df.drop(columns=["age_at_first_retirement",
                                   "net_worth_at_first_retirement",
                                   "wave_of_first_retirement",
                                   "hh_wealth_avg",
                                   "hh_wealth_growth",
                                   "hh_income_to_wealth"])

        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(
            x, y, test_size=0.2, random_state=42
        )

        x_train = x_train.fillna(x_train.mean())
        x_test = x_test.fillna(x_train.mean())

        rf = sklearn.ensemble.RandomForestRegressor(n_estimators=200,
                                                    max_depth=None,
                                                    min_samples_split=2,
                                                    random_state=42,
                                                    n_jobs=-1)

        rf.fit(x_train, y_train)
        preds = rf.predict(x_test)

        y_test_actual = np.expm1(y_test)
        preds_actual = np.expm1(preds)

        r2 = sklearn.metrics.r2_score(y_test, preds)
        mae = sklearn.metrics.mean_absolute_error(y_test_actual, preds_actual)

        print("Random Forest Results")
        print("---------------------")
        print(f"R²: {r2:.4f}")
        print(f"MAE: {mae:.4f}")

        importance = pd.Series(
            rf.feature_importances_,
            index=x_train.columns
        ).sort_values(ascending=False)

        print("\nTop 10 Important Features:")
        print(importance.head(10))

    def model_worth_linear(self):
        pd.set_option('display.float_format', '{:.6f}'.format)

        worth_df = self.working_df.copy()

        # drop respondents that have not yet retired
        worth_df = worth_df.dropna(subset=["net_worth_at_first_retirement"])

        print_separator()
        print("Linear Regression: Net Worth")
        print(f"Run #1")

        worth_df = worth_df[worth_df["net_worth_at_first_retirement"] > -1]
        y = np.log1p(worth_df["net_worth_at_first_retirement"]) # log transform bc skewed
        x = worth_df.drop(columns=["age_at_first_retirement", "net_worth_at_first_retirement",
                                 "wave_of_first_retirement", "hh_wealth_avg", "hh_wealth_growth",
                                 "hh_income_to_wealth"])

        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(
            x, y, test_size=0.2, random_state=42
        )

        x_train = x_train.fillna(x_train.mean())
        x_test = x_test.fillna(x_train.mean())

        model = sklearn.linear_model.LinearRegression()
        model.fit(x_train, y_train)

        preds = model.predict(x_test)

        # change back to actual $
        y_test_actual = np.expm1(y_test)
        preds_actual = np.expm1(preds)

        r2 = sklearn.metrics.r2_score(y_test, preds)
        mae = sklearn.metrics.mean_absolute_error(y_test_actual, preds_actual)

        print()
        print("\tR²:", r2)
        print("\tMAE:", mae)

        # coefficients
        coef_df = pd.Series(model.coef_, index=x_train.columns).sort_values()
        print("\nCoefficients:")
        print(coef_df)

        lasso = sklearn.linear_model.Lasso(alpha=0.1)
        lasso.fit(x_train, y_train)

        lasso_coef = pd.Series(lasso.coef_, index=x_train.columns)
        print("\nLasso coefficients:")
        print(lasso_coef.sort_values())

        to_drop = lasso_coef[abs(lasso_coef) < 1e-5].index
        print("\nVariables to drop next round: " + str(len(to_drop)))
        print(to_drop)

        x_train_reduced = x_train.drop(columns=to_drop)
        x_test_reduced = x_test.drop(columns=to_drop)

        model_reduced = sklearn.linear_model.LinearRegression()
        model_reduced.fit(x_train_reduced, y_train)

        preds_reduced = model_reduced.predict(x_test_reduced)

        y_test_reduced_actual = np.expm1(y_test)
        preds_reduced_actual = np.expm1(preds_reduced)

        print_separator()
        print("Run #2 (Reduced Model)")

        r2_reduced = sklearn.metrics.r2_score(y_test, preds_reduced)
        mae_reduced = sklearn.metrics.mean_absolute_error(y_test_reduced_actual, preds_reduced_actual)

        print("\n\tR²:", r2_reduced)
        print("\tMAE:", mae_reduced)

        coef_reduced = pd.Series(model_reduced.coef_, index=x_train_reduced.columns).sort_values()
        print("\nCoefficients:")
        print(coef_reduced)

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
        nonwave_cols = ["r_edu_high_deg", "r_gender", "r_race"]
        for col in nonwave_cols:
            self.clean_nonwave(col)

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