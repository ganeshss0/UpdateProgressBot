from progress.logger import logging
from progress.utils import dt, pd
from progress.entity import ONE_MONTH_TIMEDELTA



def create(current_date: dt.datetime)->pd.DataFrame:
    '''Returns a template of dataset.'''

    # columns of dataset
    columns = ['Date'] + list(range(1, 32))
    # Next 12 months time stamps, starts from today
    next_12_months = pd.date_range(start=current_date - ONE_MONTH_TIMEDELTA, freq='ME', periods=12)
    logging.info('Creating Dataset Template')
    template = pd.DataFrame(
        data={
                'Date':next_12_months
            },
        columns=columns
    )
    template.columns = template.columns.astype(str)
    return template



def add_month_row(data: pd.DataFrame, current_date:object) -> pd.DataFrame:
    '''Adds a Empty month row to data.'''
    
    logging.info('Adding New Month Row to Data')
    # Day after current date
    next_day = current_date + dt.timedelta(days=1)

    logging.info('Creating Empty Row for Next Month')
    # Next Month Row [2024-01, NaN, ... , NaN]
    # new_month = [next_day.strftime(date_format)] + ([pd.NA] * 31)
    new_month = [next_day] + ([pd.NA] * 31)

    # Adding the Next Month Row at the end of data
    data.loc[data.index.size] = new_month
    logging.info('New Month Row Added Successfully')

    return data

