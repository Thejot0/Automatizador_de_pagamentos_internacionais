import logging

logging.basicConfig(
    level=logging.INFO,
    format= "%(asctime)s[%(levelname)s]: %(message)s",
    datefmt= "%d/%m/%Y - [%H:%M:%S]",
    filename='pasta_log.log',
    encoding='utf-8',
    force = True

)

logger = logging.getLogger()

if __name__ == "__main__":
    logger.info('sss')