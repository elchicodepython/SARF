import logging

"""Utilities to bootstrap SARF listeners scripts"""


def setup_logging(name: str, filename: str, level: int=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    ch = logging.StreamHandler()
    fh = logging.FileHandler(filename)

    logger.addHandler(ch)
    logger.addHandler(fh)
