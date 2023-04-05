import requests
from lxml import etree
import re
from datetime import datetime
import csv
import json

from file_saver import FileSaver
from mysql_saver import MySQLSaver

from agenda_scraping_logging import AgendaScrapingLogging
logger = AgendaScrapingLogging.get_logger('ams_delamar')

from date_converter import convert_date

NOW = datetime.now()

BASE_URL = 'https://delamar.nl/ajax/showsearch/'

# HEADERS = {
#     "host": "delamar.nl",
#     "connection": "keep-alive",
#     "sec-ch-ua": "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"macOS\"",
#     "upgrade-insecure-requests": "1",
#     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "sec-fetch-site": "none",
#     "sec-fetch-mode": "navigate",
#     "sec-fetch-user": "?1",
#     "sec-fetch-dest": "document",
#     "accept-encoding": "gzip, deflate, br",
#     "accept-language": "en-US,en;q=0.9"
# }

HEADERS = {
    "host": "delamar.nl",
    "connection": "keep-alive",
    "sec-ch-ua": "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
    "accept": "application/json, text/javascript, */*; q=0.01",
    "x-requested-with": "XMLHttpRequest",
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://delamar.nl/voorstellingen/",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "cookie": "ASP.NET_SessionId=aihu54sd5gbyujggvmkwgqbp"
}

def _save_response_content(data):
    global NOW

    filename = f'data/raw/ams-delamar-productions-raw-{NOW.strftime("%Y%m%d%H%M")}.json'

    logger.debug(f'Saving response raw content at {filename}')

    f = open(filename, 'w')
    f.write(data)
    f.close()

def get_production_list():
 
    logger.debug('Getting production list...')

    url = "https://delamar.nl/ajax/showsearch/"

    querystring = {
        "searchTerm": "",
        "date": "",
        "orderBy": "date",
        "currentNodeId": "1073",    # Que sera isso?
        "tags": ""
    }

    response = requests.get(url, headers=HEADERS, params=querystring)

    data = json.loads(response.text)

    _save_response_content(response.text)

    productions = []
    for show in data['Shows']:

        production_id = show['ShowId']
        production_title = show['Title']
        production_subtitle = show['Subtitle']
        production_url = f'https://delamar.n{show["Url"]}'

        # Covering cases like:
        # DateCompact: do 13 apr t/m zo 07 mei
        # DateCompact2: do 18 mei t/m zo 21 mei
        for date_key in ['DateCompact', 'DateCompact2']: 
            
            # Process DateCompact2 if:
            #   DateCompact: 'do 13 apr t/m zo 07 mei'
            #   DateCompact2: 'do 18 mei t/m zo 21 mei'
            # and not
            #   DateCompact: 'do 13 apr t/m zo 07 mei'
            #   DateCompact2: '' 
            if date_key in show and len(show[date_key].strip()) > 0: 

                production_date = show[date_key]   
                match = re.findall('\D{2} \d{2} \D{3}', production_date)
                if len(match) == 1 :
                    production_start_date = convert_date(match[0])
                    production_end_date = convert_date(match[0])
                elif len(match) > 1:  
                    production_start_date = convert_date(match[0])
                    production_end_date = convert_date(match[1])
                else:
                    production_start_date = NOW.strftime('%Y-%m-%d') # TODO: Reasonable?
                    production_end_date = NOW.strftime('%Y-%m-%d')
                
                production_time = '' # TODO: Where is it?


                # TODO: Refactor later
                # Not the best solution.
                # DateCompact: 'za 03 jun t/m vr 31 mrt'
                # DateCompact2: 'za 03 jun'
                if date_key == 'DateCompact2' and production_start_date == last_start_date:
                    break

                productions.append({
                    'city' : 'Amsterdan',
                    'theater' : 'De La Mar',
                    'id' : production_id,
                    'showName' : f'{production_title} - {production_subtitle}',
                    'startDate' : production_start_date,
                    'endDate' : production_end_date,
                    'time' : production_time,
                    'linkToShow' : production_url
                })

                last_start_date = production_start_date

        del production_id, production_title, production_date, production_start_date, production_end_date, production_time, production_url, last_start_date

    logger.debug(f'{len(productions)} found')
    return productions


# def save_productions(productions):
    
#     global NOW

#     filename = f'data/ams-delamar-productions-{NOW.strftime("%Y%m%d%H%M")}.csv'
    
#     logger.info(f'Saving productions at {filename}')
                 
#     file = open(filename, 'a', newline='')
#     writer = csv.writer(file)

#     writer.writerow(["Timestamp", "City", "Theater Name", "ID", "Show Name", "Start Date", "End Date", "Time", "Link to Show"])

#     for p in productions:
#         writer.writerow([
#             NOW.strftime("%Y-%m-%d %H:%M"),
#             p['city'],
#             p['theater'],
#             p['id'],            
#             p['showName'],
#             p['startDate'],
#             p['endDate'],
#             p['time'],
#             p['linkToShow']
#         ])

def main(data_saver):
    logger.info('Starting scraping Amsterdam Delamar')
    productions = get_production_list()
    # save_productions(productions)
    data_saver.save(productions)

if __name__ == '__main__':
    saver = FileSaver('ams-delamar')
    saver = MySQLSaver()

    main(saver)
