from progress.utils import CURRENT_DATE, DATE_FORMAT, load_dataset, ONE_DAY_TIMEDELTA
from progress.logger import logging
from progress.main import main
from progress.utils import Config, pd




def get_yesterday_date() -> tuple[str, int, int]:
    '''
    Return the Yesterday Day, Month and Year.
    # Returns
    (Day, Month, Year)
    '''

    # Yesterday's Time Stamp
    yesterday = CURRENT_DATE - ONE_DAY_TIMEDELTA

    return (
        str(yesterday.day),
        yesterday.month,
        yesterday.year
        )

def UpdateValue(data, year:int, month:int, day:str, value=0):
    '''Updates Values in Data.'''

    year_mask = data['Date'].dt.year == year
    month_mask = data['Date'].dt.month == month
    mask = (year_mask & month_mask)
    # Updating the value in dataset
    data.loc[mask, day] = value

    return data

def Get_Year_Month_Filter(data: pd.DataFrame, year: int, month:int) -> pd.Series:
    '''Return a boolean series of the contains True where year_month matches with Date column in data.'''

    # formatted_date = data['Date'].dt.strftime(DATE_FORMAT)
    month_mask = data['Date'].dt.month == month
    year_mask = data['Date'].dt.year == month

    return (month_mask & year_mask)





if __name__ == '__main__':

    config = Config()
    dataset_file_path = config.get_dataset_path()
    visualization_path = config.get_visualization_path()
    
    # Loading Dataset
    data = load_dataset(dataset_file_path)

    day, year_month = get_yesterday_date()

    # Filter for Row
    # Matching the Year-Month with Date in data for which row need to update
    year_month_filter = Get_Year_Month_Filter(data, year_month)
    data = UpdateValue(data, year_month_filter, day)

    


    # Generating visuaization
    main(data, dataset_file_path, visualization_path)

    logging.info('Update Successfully')

