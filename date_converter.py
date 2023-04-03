import re
from datetime import datetime

NOW = datetime.now()

def convert_date(dutch_date):

    regex = '\D\D +(\d+) +(\D+)'
    match = re.findall(regex, dutch_date)

    day = match[0][0]
    month = match[0][1]
    year = NOW.year
    
    show_date = datetime.strptime(f'{year}-{month}-{day}', '%Y-%b-%d')

    year = NOW.year if show_date.month >= NOW.month else NOW.year + 1

    show_date = datetime.strptime(f'{year}-{month}-{day}', '%Y-%b-%d').strftime('%Y-%m-%d')

    return show_date