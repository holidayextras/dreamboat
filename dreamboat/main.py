import pycurl
import json
import time
import logging
import ConfigParser
import threading

CONFIG_FILE = 'config'

def make_logger(log_name, log_level):
    # setup logger
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    return logger

def give_life(source_url, data, DELAY, log_level):
    log_name = 'heartbeat_{0}'.format(source_url)
    logger = make_logger(log_name, log_level)
    while True:
        try:
            c = pycurl.Curl()
            c.setopt(pycurl.URL, source_url)
            c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json','X-22acaia-heartbeat: true'])
            c.setopt(pycurl.POST, 1)
            c.setopt(pycurl.POSTFIELDS, data)
            c.perform()
            rsp_code = c.getinfo(c.RESPONSE_CODE)
            if (rsp_code == 200):
                logger.info('Status from {0}: {1}'.format(source_url, rsp_code))
            else:
                logger.error('Status from {0}: {1}'.format(source_url, rsp_code))
            c.close()
            time.sleep(DELAY)
        except Exception as e:
            logger.error(e)
            time.sleep(5)

def main():
    # Load Configuration
    config = ConfigParser.ConfigParser()
    config.read(CONFIG_FILE)

    # ~~~ configure logger ~~~
    # Set log level
    LOG_LEVEL = config.get('override', 'log_level')
    logger = make_logger('heartbeat_main', LOG_LEVEL)
    logger.info('Using log_level: {0}'.format(LOG_LEVEL))

    # ~~~ configure url ~~~
    # get addresses to write to
    ADDR = config.get('override', 'endpoint')
    logger.info('Using addresses: {0}'.format(ADDR))
    # split addresses
    endpoints = ADDR.split(',')

    # ~~~ get # messages per second to write ~~~
    MSG_RATE = config.getfloat('override', 'msg_per_sec')
    logger.info('Using message rate: {0}'.format(MSG_RATE))
    # calculate delay between writes
    DELAY = 1/MSG_RATE

    # ~~~ configure json payload ~~~
    # get json field
    FIELD = config.get('override', 'field')
    logger.info('Using json field: {0}'.format(FIELD))
    # get json value
    VALUE = config.get('override', 'value')
    logger.info('Using json value: {0}'.format(VALUE))
    # create json
    data = json.dumps({FIELD: VALUE})

    # ~~~ create and spawn threads ~~~
    threads = []
    for ep in endpoints:
        logger.info('Creating pulse on {0}'.format(ep))
        t = threading.Thread(target=give_life, args=(ep, data, DELAY, LOG_LEVEL))
        t.daemon=True
        t.start()
        threads.append(t)

    allrunning = True
    while allrunning:
        for t in threads:
            t.join(5)
            if not t.isAlive():
                allrunning = False
                break

    logger.error('Opps one of the threads failed')

if __name__ == '__main__':
    main()
