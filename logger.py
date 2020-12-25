import logging

def create_default_logger(name, level=logging.DEBUG, to_file=False):
    handler = logging.StreamHandler()
    logger = logging.getLogger(name)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(message)s',
        datefmt='%d-%m-%Y %H:%S'
    )
    handler.setFormatter(formatter)

    if to_file:
        file_handler = logging.FileHandler('zacoby.log')
        logger.addHandler(file_handler)
        file_handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(level)

    return logger
    