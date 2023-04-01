import requests
import json
import csv
from datetime import datetime

from agenda_scraping_logging import AgendaScrapingLogging
logger = AgendaScrapingLogging.get_logger('ams_carre')

NOW = datetime.now()
PRODUCTIONS_KEY = 'nodes'

def _save_response_content(data):
    global NOW

    filename = f'data/raw/ams-carre-productions-raw-{NOW.strftime("%Y%m%d%H%M")}.json'

    logger.debug(f'Saving raw data at {filename}')

    f = open(filename, 'w')
    f.write(data)
    f.close()

def get_production_details(id, path):
    url = f"https://carre.nl/api/render{path}"

    headers = {}
    response = requests.get(url, headers=headers)

    _save_response_content(response.text)

    data = json.loads(response.text)

    venue_id = 0
    if 'productions' in data:
        events = data['productions'][id]['events']

        if len(events) == 0:
            raise Exception(f'No event found for production {id}')

        if len(events) > 1:
            raise Exception(f'Weird. More than one event found for production {id}')

        show_date = events[0]['start_date']
        venue_id = events[0]['venue_id']
    else:
        raise Exception(f'Production {id} not available anymore')

    if 'venues' in data:
        city = data['venues'][venue_id]['data']['city']
    else:
        city = 'Unknown'


    return {
        'show_date' : show_date,
        'city' : city
    }

def save_productions(productions):
    
    filename = f'data/ams-carre-productions-{NOW.strftime("%Y%m%d%H%M")}.csv'
    
    logger.info(f'Saving productions to {filename}')

    file = open(filename, 'a', newline='')
    writer = csv.writer(file)

    writer.writerow(["Timestamp", "City", "Theater Name", "ID",  "Show Name", "Date", "Link to Show"])

    for p in productions:
        writer.writerow([
            NOW.strftime("%Y-%m-%d %H:%M"),
            p['city'],
            p['theaterName'],
            p['id'],
            p['showName'],            
            p['date'],            
            p['linkToShow']
        ])

    file.close()

def summarize_productions(productions):
    logger.debug('Summarizing productions...')
    summary = []

    for k in productions:
        kind = productions[k]['kind']
        # logger.debug(f'Processing production of type {kind}')
        if kind == 'production-page':
            id = productions[k]['production_id']
            show_name = productions[k]['data']['title']
            theater_name = productions[k]['data']['siteTitle']
            path  = productions[k]['data']['url']
            
            logger.debug(f'Enriching production {id} at {path}...')

            try:
                details = get_production_details(id, path)
                summary.append({
                    'id': id,
                    'city' : details['city'],
                    'showName' : show_name,
                    'date' : details['show_date'][:10],
                    'theaterName' : theater_name,
                    'linkToShow' : f'https://carre.nl{path}',
                })

            except Exception as e:
                logger.debug(e)
                # Ignore
    
    return summary

def get_production_list():
    logger.debug('Getting production list...')

    url = "https://carre.nl/api/render/production-page-list-nl"

    headers = {}

    response = requests.get(url, headers=headers)

    data = json.loads(response.text)

    productions = data[PRODUCTIONS_KEY]

    logger.debug(f'{len(productions)} productions found')
    return productions
            
def main():
    logger.info('Starting scraping Amsterdam Carre')
    productions = get_production_list()
    productions = summarize_productions(productions)
    save_productions(productions)

if __name__ == '__main__':
    main()

