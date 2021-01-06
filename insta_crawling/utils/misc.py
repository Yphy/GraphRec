def get_logger(name=__file__):
    import logging
    import logging.handlers
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('./crawling.log')
    fh.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)-8s] %(asctime)s [%(filename)s] [%(funcName)s:%(lineno)d] %(message)s', '%Y-%m-%d %H:%M:%S')
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger
