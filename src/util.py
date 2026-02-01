

def print_stats(var):
    print_type(var)
    print(var.head())
    print(var.describe())
    print(var.info())


def print_type(var):
    print("\nVariable 'df' is a " + str(type(var)))


def get_column_names(df):
    """
    :return: A list of the dataframe's columns.
    """
    return df.columns.tolist()


def to_csv(df, subset=None):
    """
    Save the dataframe as a csv
    :param: subset - An optional parameter that indicates that a csv should only include the first *subset* rows.
    """
    if subset is not None:
        sub_filename = "randHRS_first" + str(subset) + ".csv"
        df.head(subset).to_csv(sub_filename, index=False)
    else:
        sub_filename = "../data/randHRS.csv"
        df.to_csv(sub_filename, index=False)
    print("File saved: " + sub_filename)
