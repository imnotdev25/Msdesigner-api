from logging import getLogger, StreamHandler, Formatter, DEBUG


def get_logger(name):
    logger_ = getLogger(name)
    logger_.setLevel(DEBUG)
    handler = StreamHandler()
    handler.setLevel(DEBUG)
    formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger_.addHandler(handler)
    return logger_


logger = get_logger(__name__)
