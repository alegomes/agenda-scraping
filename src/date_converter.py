import re
from datetime import datetime
import locale

# To avoid errors like 
# ValueError: time data '2023-mei-1' does not match format '%Y-%b-%d'  
# locale.setlocale(locale.LC_TIME, 'nl_NL')
locale.setlocale(locale.LC_TIME, "nl_NL.UTF-8")


NOW = datetime.now()

from agenda_scraping_logging import AgendaScrapingLogging
logger = AgendaScrapingLogging.get_logger('date_converter')

def convert_date(dutch_date):

    regex = '\D\D +(\d+) +(\D+)'
    match = re.findall(regex, dutch_date)

    day = match[0][0]
    month = match[0][1]
    year = NOW.year
    
    show_date = None

    # Dutch expected abbreviations:
    # januari jan
    # februari feb
    # maart maa
    # april apr
    # mei mei
    # juni jun
    # juli jul
    # augustus aug
    # september sep
    # oktober okt
    # november nov
    # december dec
    month = 'maa' if month == 'mrt' else month

    try:
        show_date = datetime.strptime(f'{year}-{month}-{day}', '%Y-%b-%d')
    except Exception as e:
        logger.error(f'Could not convert "{year}-{month}-{day}": {e}' )
        raise e

    year = NOW.year if show_date.month >= NOW.month else NOW.year + 1

    show_date = datetime.strptime(f'{year}-{month}-{day}', '%Y-%b-%d').strftime('%Y-%m-%d')

    return show_date