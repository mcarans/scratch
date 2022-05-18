import logging

from hdx.utilities.easy_logging import setup_logging
from loguru import logger

setup_logging(error_file=True)
standard_logger = logging.getLogger(__name__)

text = "This is an error!"
standard_logger.error(text)

text = "Division by zero!"


def divide(a, b):
    return a / b


try:
    divide(1, 0)
except ZeroDivisionError:
    standard_logger.exception(text)

text = "Another zero error!"
try:
    divide(2, 0)
except ZeroDivisionError:
    logger.exception(text)
