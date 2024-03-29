import requests
from lxml import etree
import re
from datetime import datetime

from file_saver import FileSaver
from mysql_saver import MySQLSaver

from agenda_scraping_logging import AgendaScrapingLogging
logger = AgendaScrapingLogging.get_logger('ams_dekleine')

from date_converter import convert_date

NOW = datetime.now()


BASE_URL = 'https://www.dekleinekomedie.nl/agenda'

HEADERS = {
        "host": "www.dekleinekomedie.nl",
        "connection": "keep-alive",
        "sec-ch-ua": "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "sec-fetch-site": "none",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9"
    }

def _save_response_content(data):
    global NOW

    filename = f'data/raw/ams-dekleine-productions-raw-{NOW.strftime("%Y%m%d%H%M")}.html'

    f = open(filename, 'w')
    f.write(data)
    f.close()

def _get_num_of_pages():
    
    logger.debug('Getting number of pages to iterate over')
    
    url = f"{BASE_URL}"

    # TODO: Overhead request just to get page numbers. Optmize it later.
    response = requests.get(url, headers=HEADERS)

    xpath_num_of_pages = '//*[@id="simplePagingForm"]/span'

    tree = etree.HTML(response.text)
    
    # TODO: What if there is one page only?

    pages_total  = tree.xpath(xpath_num_of_pages)[0].text
    num_of_pages = re.findall('van (\d+)', pages_total)[0]

    logger.debug(f'{num_of_pages} pages found')

    return int(num_of_pages)

    
def _get_productions_by_page(page=1):
    
    logger.debug(f'Getting productions of page {page}')

    url = f"{BASE_URL}?p={page}"

    response = requests.get(url, headers=HEADERS)
    _save_response_content(response.text)

    xpath_productions = '//*[@id="content"]/div[3]/div[2]/div/ul/li'

    xpath_title = 'div/div[2]/div[1]/a/h2'
    xpath_subtitle = 'div/div[2]/div[1]/a/div[@class="subtitle"]'
    xpath_start_date = 'div//div[@class="datetime"]/div[contains(@class, "date")]/div[@class="start"]'
    xpath_end_date = 'div//div[@class="datetime"]/div[contains(@class, "date")]/div[@class="end"]'
    xpath_time = 'div//div[@class="datetime"]/div[contains(@class, "time")]/*[@class="start"]'
    # xpath_url = 'div[@class="listItemWrapper"]/div[contains(@class,"thumb")]/a[@class="image"]'
    xpath_url = "./div[@class='listItemWrapper ']/div[@class='thumb ']/a/@href"

    # TODO: What if the production takes place more than one day?
    # xpath_subshows = '*[@id="show2148Dates"]'

    tree = etree.HTML(response.text)
    
    productions_in_the_page = tree.xpath(xpath_productions)

    productions = []
    for p in productions_in_the_page:
        production_id = p.get('data-entry-id')
        production_url = f"https://www.dekleinekomedie.nl{p.xpath(xpath_url)[0]}"
        production_title = p.xpath(xpath_title)[0].text
        production_subtitle = p.xpath(xpath_subtitle)[0].text
        production_start_date = convert_date(p.xpath(xpath_start_date)[0].text.strip())
        
        try:
            production_end_date = convert_date(p.xpath(xpath_end_date)[0].text.strip())
        except:
            production_end_date = production_start_date

        try:
            production_time = p.xpath(xpath_time)[0].text.strip()
        except:
            production_time = ''

        productions.append({
            'city' : 'Amsterdan',
            'theater' : 'De Kleine Komedie',
            'id' : production_id,
            'showName' : f'{production_title} - {production_subtitle}' ,
            'startDate' : production_start_date,
            'endDate' : production_end_date,
            'time' : production_time,
            'linkToShow' : production_url
        })

        production_time = ''

        del production_id, production_title, production_start_date, production_end_date, production_time, production_url

    return productions

def get_production_list():
 
    logger.debug('Getting production list...')

    productions = []
    num_of_pages = _get_num_of_pages()

    for p in range(1, num_of_pages+1):
        productions = productions + _get_productions_by_page(p)

    logger.debug(f'{len(productions)} productions found')

    return productions

# def save_productions(productions):
#     now = datetime.now()
#     filename = f'data/ams-dekleinekomedie-productions-{now.strftime("%Y%m%d%H%M")}.csv'
    
#     logger.info(f'Saving productions to {filename}')

#     file = open(filename, 'a', newline='')
#     writer = csv.writer(file)

#     writer.writerow(["Timestamp", "City", "Theater Name", "ID", "Show Name", "Start Date", "End Date", "Time", "Link to Show"])

#     for p in productions:
#         writer.writerow([
#             now.strftime("%Y-%m-%d %H:%M"),
#             p['city'],
#             p['theater'],
#             p['id'],            
#             p['showName'],
#             p['startDate'],
#             p['endDate'],
#             p['time'],
#             p['linkToShow']
#         ])

#     file.close()

def main(data_saver):
    logger.info('Starting scraping Amsterdam Dekleine')
    productions = get_production_list()
    # save_productions(productions)
    data_saver.save(productions)

if __name__ == '__main__':
    saver = FileSaver('ams-dekleine')
    saver = MySQLSaver()

    main(saver)
