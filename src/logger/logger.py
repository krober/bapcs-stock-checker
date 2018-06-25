import logging


def get_logger(name: str, file: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(file)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter(f'%(asctime)s'
                                  f'-%(levelname)s'
                                  f'-%(name)s'
                                  f'-%(module)s'
                                  f'-%(lineno)s'
                                  f'-%(funcName)s'
                                  f'-%(message).50s')

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


