"""
    Script para generar random logs 
    
    Log level de python
    1. DEBUG
    2. INFO
    3. WARNING
    4. ERROR
    5. CRITICAL

"""
import logging
import random


def main():
    logging.basicConfig(filename='log_file.log',
                        filemode='w',
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s') 

    for i in range(1000):
        loop_time+= 1
        log_level = random.randint(1,5)
        if (log_level == 1):
            logging.debug('log debug')
        elif (log_level == 2):
            logging.info('log info')
        elif (log_level == 3):
            logging.warning('log warning')
        elif (log_level == 4):
            logging.error('log error')
        elif (log_level == 5):
            logging.critical('log critical')
        else:
            print( log_level )



if __name__ == '__main__':
    main()
