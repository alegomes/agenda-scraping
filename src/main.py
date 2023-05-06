import ams_carre
import ams_dekleine
import ams_delamar
import ams_meervaart

from agenda_scraping_logging import AgendaScrapingLogging

from file_saver import FileSaver
from mysql_saver import MySQLSaver

logger = AgendaScrapingLogging.get_logger('main')

def main():
    # saver_ams_carre = FileSaver('ams-carre')
    # saver_ams_dekleine = FileSaver('ams-dekleine')
    # saver_ams_delamar = FileSaver('ams-delamar')
    # saver_ams_meervaart = FileSaver('ams-meervaart')

    # ams_carre.main(saver_ams_carre)
    # ams_dekleine.main(saver_ams_dekleine)
    # ams_delamar.main(saver_ams_delamar)
    # ams_meervaart.main(saver_ams_meervaart)

    ams_carre.main( MySQLSaver())
    ams_dekleine.main( MySQLSaver())
    ams_delamar.main( MySQLSaver())
    ams_meervaart.main( MySQLSaver())

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(f'Oops. Something went wrong: {e}')
