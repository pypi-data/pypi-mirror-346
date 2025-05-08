from loguru import logger

logger: logger

def get_logger(name: str):
    return logger.bind(name=name)

