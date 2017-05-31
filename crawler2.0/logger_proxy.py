import logging.config

logging.config.fileConfig("logging.ini")


def get_logger():
	return logging.getLogger("proLogger")


# create logger
logger = get_logger()
