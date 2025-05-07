import pandas as pd
import numpy as np
from functools import partial

class ClimateHandler:
    def __init__(self, wx_file, start_day, start_month, start_year, sep = "\t"):
        self.df = pd.read_csv(wx_file, sep=sep)
        self.start_index = self.get_start_index(start_day, start_month, start_year)
        for col in self.df.columns:
            setattr(self, col, partial(self.climate, variable=col))

    def get_start_index(self, start_day, start_month, start_year):
        try:
            index = self.df[(self.df.DA == start_day) & (self.df.MO == start_month) & (self.df.YEAR == start_year)].index[0]
        except:
            IndexError(f"Date {start_day}-{start_month}-{start_year} not found in weather file.")
        return index
    
    def climate(self, T, variable):
        index = int(np.floor(T) + self.start_index)
        return self.df.iloc[index][variable]
    
C = ClimateHandler("pbdm/sample_weather.csv", 14, 2, 2007)

print(C.TMAX(14), C.DA(14))