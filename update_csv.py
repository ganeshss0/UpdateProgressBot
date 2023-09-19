import pandas as pd
from time import localtime

def update(status: int, path: str):
    data = pd.read_csv(path)
    current_mon = localtime().tm_mon
    currnet_year = localtime().tm_year
    current_day = str(localtime().tm_mday)
    mask = (data.Month == current_mon) & (data.Year == currnet_year)
    data.loc[mask, current_day] = status
    data.to_csv(path, index=False)