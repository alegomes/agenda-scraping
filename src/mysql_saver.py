import os
import sys
from datetime import datetime
import mysql.connector
from data_saver import DataSaver

from agenda_scraping_logging import AgendaScrapingLogging
logger = AgendaScrapingLogging.get_logger('mysql_saver')

NOW = datetime.now()

class MySQLSaver(DataSaver):

    def __init__(self):

        dbhost = os.getenv('MYSQL_HOST')
        dbuser = os.getenv('MYSQL_USER')
        dbpass = os.getenv('MYSQL_PASSWORD')

        if not dbhost:
            logger.debug('MYSQL_HOST not defined. Using default value "localhost"')
            dbhost="localhost"

        if not dbuser:
            msg = 'Environment variable MYSQL_USER required.'
            logger.error(msg)
            raise Exception(msg)

        if not dbpass:
            msg = 'Environment variable MYSQL_PASS required.'
            logger.error(msg)
            raise Exception(msg)

        logger.debug(f'Connecting to database with user={dbuser}...')

        try:
            self.connection = mysql.connector.connect(
                host=dbhost,
                port=3306,
                user=dbuser,
                password=dbpass,
                database="agenda_scraping"
            )
        except BaseException as e:
            logger.error(f'Failed to connect to the database host={dbhost} user={dbuser}: {e}')
            raise e

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
