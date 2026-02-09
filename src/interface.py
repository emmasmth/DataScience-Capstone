import os

from src.util import *

def hello():
    print_separator()
    print("Welcome to Emma's Data Science Capstone project for Loyola University Maryland."
          "\n\tThis Python project examines retirement trends of Americans.")

def goodbye():
    print_separator()
    print("Thanks for visiting. Goodbye!")

def check_file(file_path):
    print_separator()
    acceptance = input("File name is " + str(file_path) + ". Confirm? (Y/N)\n")
    while acceptance.lower() not in ["y", "n", "yes", "no"]:
        acceptance = input("File name is " + str(file_path) + ". Confirm? (Y/N)\n")
    if acceptance == "n":
        exists = False
        while not exists:
            print("Current working directory is " + str(os.getcwd()))
            new_file_path = input("Please enter a new file name: \n")
            exists = check_file_exists(new_file_path)
            if exists:
                file_path = new_file_path
    return file_path

def confirm_print(name, print_or_plot="print"):
    print_separator()
    ans = input("Do you wish to " + print_or_plot + " " + name + "? (Y/N)\n")
    while ans.lower() not in ["y", "n", "yes", "no"]:
        ans = input("Do you wish to " + print_or_plot + " " + name + "? (Y/N)\n")
    if ans.lower() == "y":
        return True
    else:
        return False
