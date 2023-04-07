from datetime import datetime
import mysql.connector

from data_saver import DataSaver

from agenda_scraping_logging import AgendaScrapingLogging
logger = AgendaScrapingLogging.get_logger('mysql_saver')

NOW = datetime.now()

class MySQLSaver(DataSaver):

    def __init__(self):
        self.connection = mysql.connector.connect(
            host="db", # TODO: "localhost" when running local on the host machine
            user="scraper",
            password="brentmartens",
            database="agenda_scraping"
        )

    def save(self, productions):
        mycursor = self.connection.cursor()

        sql = "INSERT INTO productions (created_at, city, theater, id, showname, startdate, enddate, url) values (%s,%s,%s,%s,%s,%s,%s,%s)"

        values = []
        for p in productions:
            values.append((
                NOW.strftime("%Y-%m-%d %H:%M"),
                p['city'],
                p['theater'],
                p['id'],
                p['showName'],            
                p['startDate'], 
                p['endDate'],           
                p['linkToShow']
            ))
        
        # try:
        mycursor.executemany(sql, values)
        # except Exception as e:
        #     logger.error(f'Error:\n{e}\n...with data {p}')

        self.connection.commit()
        self.connection.close()

        logger.info(f'{mycursor.rowcount} productions saved.')
