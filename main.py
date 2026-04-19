from src.model import *
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

processor = Processor(data.df)
processor.plot_waves()
processor.plot_age()
processor.plot_nw()
new_df = processor.get_new_df()

model = Model(new_df)

# while True:
#     menu()