from src.dataset import *
from src.interface import *
from src.processor import *

hello()

file_path = "./data/randhrs1992_2022v1.sas7bdat"
file_path = check_file(file_path)

data = DataSet(file_path)
data.clean()

processor = Processor(data.df)

processor.plot_waves()
processor.plot_age()

while True:
    menu()