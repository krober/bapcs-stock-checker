import logging


def get_logger(name: str, file: str, level):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.FileHandler(file)
    handler.setLevel(level)

    formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger



