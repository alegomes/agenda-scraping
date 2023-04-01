import logging
import sys

LOGFILE='log/app.log'
LOGGING_FORMAT='%(asctime)s [%(name)s] %(funcName)s - %(levelname)s - %(message)s'

logging.basicConfig( level=logging.DEBUG, 
                    filename=LOGFILE, 
                    filemode='a', 
                    datefmt='%y-%m-%d %H:%M:%S', 
                    format=LOGGING_FORMAT)

# f_handler = logging.FileHandler(LOGFILE)
# f_handler.setLevel(logging.DEBUG)
# f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# f_handler.setFormatter(f_format)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))

logging.getLogger('urllib3.connectionpool').setLevel('INFO')

class AgendaScrapingLogging:

    def get_logger(logger_name):
        logger = logging.getLogger(logger_name)
        logger.addHandler(stdout_handler)

        return logger
