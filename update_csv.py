import pandas as pd

def update(status: int, path: str, date):
    data = pd.read_csv(path)
    mask = (data.Month == date.month) & (data.Year == date.year)
    data.loc[mask, str(date.day)] = status
    data.to_csv(path, index=False)