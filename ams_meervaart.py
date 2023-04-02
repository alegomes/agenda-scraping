import requests
from lxml import etree
import re
from datetime import datetime
import csv
import json

from file_saver import FileSaver

from agenda_scraping_logging import AgendaScrapingLogging
logger = AgendaScrapingLogging.get_logger('ams_meervaart')

NOW = datetime.now()
THEATER = 'meervaart'
BASE_URL = 'https://www.meervaart.nl/theater/programma'

HEADERS = {
        "host": "www.meervaart.nl",
        "connection": "keep-alive",
        "cache-control": "max-age=0",
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
        "accept-language": "en-US,en;q=0.9",
        "cookie": "CFID=86648576; CFTOKEN=d120d7f6d2df0bb9-70587140-5254-00B0-69B99C3CAD89EA2F; gs_v_GSN-074302-K=; _fbp=fb.1.1679091208115.273561518; _gid=GA1.2.1994754227.1679091208; _gat_UA-1578605-1=1; _hjFirstSeen=1; _hjIncludedInSessionSample_2149396=0; _hjSession_2149396=eyJpZCI6IjgwMzVlNWEyLWU1YzEtNGIwNi1iODc1LWIyY2RiZTc0NTcyNSIsImNyZWF0ZWQiOjE2NzkwOTEyMDg1NTksImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=1; _hjSessionUser_2149396=eyJpZCI6IjhhOGQ4NWNiLTY1Y2UtNTc2OS1hYTk5LTQ5NWQ3ZDgwZDE4ZiIsImNyZWF0ZWQiOjE2NzkwOTEyMDg1NTEsImV4aXN0aW5nIjp0cnVlfQ==; gs_u_GSN-074302-K=594dab4f6bad3d3d99302e3f3e44b7e2:3115:5379:1679091218217; _ga_570E8WDNJ1=GS1.1.1679091208.1.1.1679091218.0.0.0; _ga=GA1.1.149408999.1679091208; gs_p_GSN-074302-K=1"
    }

def _save_response_content(data):
    global NOW

    filename = f'data/raw/ams-{THEATER}-productions-raw-{NOW.strftime("%Y%m%d%H%M")}.html'

    logger.debug(f'Saving raw data at {filename}')

    f = open(filename, 'w')
    f.write(data)
    f.close()

def _get_production_id(url):

    r = '.*\/(\d{4,})\/*.*$'
    match = re.findall(r, url)

    return match[0] if match else 0

def _get_start_end_dates(fulldate):

    if type(fulldate) == list:  # "DI 21 MRT WO 22 MRT"
        match = fulldate
    else:                       # "DI 21 MRT" or "VR 27 MRT T/M ZO 26 MRT"     
        match = re.findall('\D{2} \d{2} \D{3}', fulldate)


    if len(match) == 1 :
        production_start_date = match[0]
        production_end_date = ''
    elif len(match) > 1:  
        #   do 13 apr t/m zo 07 mei 
        # or
        #   do 13 apr t/m zo 07 mei        # TODO: What to do in these cases? 
        #   do 18 mei t/m zo 21 mei
        # or
        #   vr 10 nov vr 17 nov            # TODO: It's an interval or two dates only?

        production_start_date = match[0]
        production_end_date = match[1]
    else:
        production_start_date = f'!!! {fulldate} !!!' # TODO: Translate to a date?
        production_end_date = ''

    return (production_start_date, production_end_date)

def _get_xpath(node, xpath):
    
    try:
        r = node.xpath(xpath)
        if len(r) == 1:
            return r[0]
        else:
            return r
    except:
        return '*Failed*'

def get_production_list():
 
    logger.debug('Getting productions list')

    response = requests.get(BASE_URL, headers=HEADERS)

    _save_response_content(response.text)

    xpath_productions = '//div[contains(@class, "show")]'

    xpath_title = './/div[@class="info"]/h3/text()'
    xpath_artist = './/div[@class="info"]/h4/text()'
    xpath_date = './/div[@class="info"]/div[contains(@class, "date")]/span/text()'
    xpath_url = './/a/@href'

    tree = etree.HTML(response.text)
    productions_html = tree.xpath(xpath_productions)

    productions = []
    for p in productions_html:

        # production_title = p.xpath(xpath_title)[0]
        production_title = _get_xpath(p, xpath_title)
        production_artist = _get_xpath(p, xpath_artist) # TODO: Relevant data?
        production_url = f'https://www.meervaart.nl{_get_xpath(p, xpath_url)}'
        production_date = _get_xpath(p, xpath_date)

        production_id = _get_production_id(production_url)
        production_start_date, production_end_date = _get_start_end_dates(production_date)

        production_genre = p.getparent().get('data-genre') # TODO: Relevant data?
        production_dates = p.getparent().get('data-date')

        production_time = ''

        productions.append({
            'city' : 'Amsterdan',
            'theater' : 'Meervaart',
            'id' : production_id,
            'showName' : production_title,
            'startDate' : production_start_date,
            'endDate' : production_end_date,
            'time' : production_time,
            'linkToShow' : production_url
        })

        del production_id, production_title, production_date, production_start_date, production_end_date, production_time, production_url

    logger.debug(f'{len(productions)} productions found')

    return productions


def save_productions(productions):
    
    global NOW

    filename = f'data/ams-{THEATER}-productions-{NOW.strftime("%Y%m%d%H%M")}.csv'
    
    logger.info(f'Saving productions at {filename}')

    file = open(filename, 'a', newline='')
    writer = csv.writer(file)

    writer.writerow(["Timestamp", "City", "Theater Name", "ID", "Show Name", "Start Date", "End Date", "Time", "Link to Show"])

    for p in productions:
        writer.writerow([
            NOW.strftime("%Y-%m-%d %H:%M"),
            p['city'],
            p['theater'],
            p['id'],            
            p['showName'],
            p['startDate'],
            p['endDate'],
            p['time'],
            p['linkToShow']
        ])

def main(data_saver):
    logger.info('Starting scraping Amsterdam Meervaart')
    productions = get_production_list()
    #save_productions(productions)
    data_saver.save(productions)

if __name__ == '__main__':
    main(FileSaver('ams-meervaart'))

