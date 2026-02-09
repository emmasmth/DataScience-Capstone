import os

from interface import confirm_print


def check_file_exists(file_path):
    if os.path.exists(file_path):
        print(f"The file '{file_path}' exists.")
        return True
    else:
        print(f"The file '{file_path}' does not exist.")
        return False

def print_dataframe(name, df):
    ans = confirm_print("the cleaned dataframe")
    if ans:
        print_separator()
        print("Showing " + name + "...")
        print(df)


def print_separator():
    print("\n---------------------------------------------------------------------------------\n")

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


def save_as_csv(df, subset=None, filename="randHRS.csv"):
    """
    Save the dataframe as a csv
    :param: subset - An optional parameter that indicates that a csv should only include the first *subset* rows.
    """
    sub_filename = "../data/" + filename
    if subset is not None:
        df.head(subset).to_csv(sub_filename, index=False)
    else:
        df.to_csv(sub_filename, index=False)
    print("File saved: " + sub_filename)
