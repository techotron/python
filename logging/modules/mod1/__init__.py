from utils import Logger


LOGGER = Logger(__file__)
LOG = LOGGER.get_logger()


def function_from_mod1():
    LOG.info("Hello from mod1!")
