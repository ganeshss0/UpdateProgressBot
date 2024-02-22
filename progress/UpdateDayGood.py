from utils import CURRENT_DATE, DATE_FORMAT, load_dataset, ONE_DAY_TIMEDELTA
from logger import logging
from main import main
from utils import Config, pd




def get_yesterday_date() -> tuple[str, str]:
    '''Return the Yesterday Day and Month-Year.'''

    # Yesterday's Time Stamp
    yesterday = CURRENT_DATE - ONE_DAY_TIMEDELTA

    return (
        str(yesterday.day), 
        yesterday.strftime(DATE_FORMAT)
        )

def UpdateValue(data, year_month_filter, day, value=0):
    '''Updates Values in Data.'''

    # Updating the value in dataset
    data.loc[year_month_filter, day] = value

    return data

def Get_Year_Month_Filter(data: pd.DataFrame, year_month:str) -> pd.Series:
    '''Return a boolean series of the contains True where year_month matches with Date column in data.'''

    formatted_date = data['Date'].dt.strftime(DATE_FORMAT)

    return (formatted_date == year_month)





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

