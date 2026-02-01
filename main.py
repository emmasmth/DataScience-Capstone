from src.dataset import *
from src.processor import *

file_path = "./data/randhrs1992_2022v1.sas7bdat"
data = DataSet(file_path)
processor = Processor(data.df)
processor.plot_waves()
processor.plot_age()