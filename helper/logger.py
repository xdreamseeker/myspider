from logging import Logger
import logging,logging.config
from logging.handlers import RotatingFileHandler


#init log

def init_logger(logger_name):
    if logger_name not in Logger.manager.loggerDict:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)
        logger.addHandler(console)
    logger = logging.getLogger(logger_name)
    return logger

logger = init_logger("infolog")


if __name__ == '__main__':
    print("main")
    logger.info("logging init")