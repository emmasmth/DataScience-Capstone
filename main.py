from src.dataset import *
from src.interface import *
from src.processor import *

hello()

RAND_path = "./data/randhrs1992_2022v1.sas7bdat"
cleaned_path = "./data/cleaned_data.csv"

if check_file_exists(cleaned_path):
    file_path = check_file(cleaned_path)
    cleaned = True
else:
    file_path = check_file(RAND_path)
    cleaned = False

data = DataSet(file_path, cleaned)


"""
Need to work on processor functions now that we have changed the initial dataset handling.

Should still make the derived variables though
"""
# processor = Processor(data.df)
#
# processor.plot_waves()
# processor.plot_age()

while True:
    menu()