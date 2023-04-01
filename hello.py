import datetime
import logging

logging.basicConfig( level=logging.DEBUG, 
                    filename='log/app.log', 
                    filemode='a', 
                    datefmt='%y-%m-%d %H:%M:%S', 
                    format='%(asctime)s %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('hello')

f_handler = logging.FileHandler('log/app.log')
f_handler.setLevel(logging.DEBUG)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

def main():
    try:
        # Getting the current time upto seconds only.
        cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        msg = f'Current Time : {cur_time}'
        print(msg)
        logger.info(msg)
    except:
        # logging.error('Something Wrong in main function', exc_info=True)
        logger.exception('Something Wrong in main function')

if __name__=='__main__':
    main()