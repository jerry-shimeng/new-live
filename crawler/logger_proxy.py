import logging.config

from config import run_env

logging.config.fileConfig("logging.ini")


def get_logger():
    if run_env == "product" or run_env == "pro":
        return logging.getLogger("proLogger")
    else:
        return logging.getLogger("devLogger")


# create logger
logger = get_logger()
