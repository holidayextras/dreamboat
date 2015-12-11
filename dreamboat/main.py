import pycurl
import json
import time
import logging
import ConfigParser

CONFIG_FILE = 'config'

# setup logger
logger = logging.getLogger('heartbeat_logger')
logger.setLevel('ERROR')
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

def main():
    # Load Configuration
    config = ConfigParser.ConfigParser()
    config.read(CONFIG_FILE)
    
    # ~~~ configure logger ~~~
    # Set log level
    LOG_LEVEL = config.get('override', 'log_level')
    logger.setLevel(LOG_LEVEL)
    logger.info('Using address: {0}'.format(LOG_LEVEL))
    
    # ~~~ configure url ~~~
    # get address to write to
    ADDR = config.get('override', 'address')
    logger.info('Using address: {0}'.format(ADDR))
    # get port
    PORT = config.get('override', 'port')
    logger.info('Using port: {0}'.format(PORT))
    # get post route
    POST = config.get('override', 'post_route')
    logger.info('Using post route: {0}'.format(POST))
    # create url
    source_url = '{0}:{1}{2}'.format(ADDR,PORT,POST)
    
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
    
    while True:
        try:
            c = pycurl.Curl()
            c.setopt(pycurl.URL, source_url)
            c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json'])
            c.setopt(pycurl.POST, 1)
            c.setopt(pycurl.POSTFIELDS, data)
            c.perform()
            rsp_code = c.getinfo(c.RESPONSE_CODE)
            if (rsp_code == 200):
                logger.info('Status: %d' % rsp_code)
            else:
                logger.error('Status: %d' % rsp_code)
            c.close()
            time.sleep(DELAY)
        except Exception as e:
            logger.error(e)
            time.sleep(5)

if __name__ == '__main__':
    main()
