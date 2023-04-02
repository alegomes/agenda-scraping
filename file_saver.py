from datetime import datetime
import csv

from data_saver import DataSaver

from agenda_scraping_logging import AgendaScrapingLogging
logger = AgendaScrapingLogging.get_logger('file_saver')

NOW = datetime.now()

class FileSaver(DataSaver):

    def __init__(self, prefix):
        self.FILENAME_PREFIX = prefix
    
    def save(self, productions):
    
        filename = f'data/{self.FILENAME_PREFIX}-productions-{NOW.strftime("%Y%m%d%H%M")}.csv'
        
        logger.info(f'Saving productions to {filename}')

        file = open(filename, 'a', newline='')
        writer = csv.writer(file)

        writer.writerow(["Timestamp", "City", "Theater Name", "ID",  "Show Name", "Start Date", "Link to Show"])

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

        logger.info(f'File {filename} saved')
