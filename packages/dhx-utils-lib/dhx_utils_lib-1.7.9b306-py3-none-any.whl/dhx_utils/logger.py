"""
Copyright (c) 2019-2020 RoZetta Technology Pty Ltd. All rights reserved.
"""
import logging
import os


# pylint:disable=too-few-public-methods
class DHXFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, 'aws_request_id'):
            # set aws_request_id to empty string if the logger is not used from AWS lambda
            record.aws_request_id = ''
        return True


def get_default_logger(name=None):
    """Returns a default logger for non AWS lambda environment.

    :param name: Name of the logger (defaults to None)
    :type name: str
    :return: The logger
    :rtype: Logger
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)-15s %(name)s %(levelname)-7s - %(message)s'))
        logger.addHandler(handler)
    return logger


def get_lambda_logger(name=None):
    """ Prepare a logger object that has a consistent logging
        format with the ability to overwrite the log level
        at run time (via the `LOG_LEVEL` environment variable) for aws lambda
    :param name: Name of the logger (defaults to None)
    :type name: str
    :return: The logger
    :rtype: Logger
    """
    logger = logging.getLogger(name)
    for h in logger.handlers:
        h.setFormatter(logging.Formatter(
            "[%(levelname)s]\t%(aws_request_id)s\t%(message)s\n"
        ))
    return logger


def _is_running_lambda():
    execution_env = os.environ.get('AWS_EXECUTION_ENV', '')
    if execution_env:
        return execution_env.startswith('AWS_Lambda_')
    return False


def get_logger(name=None):
    """ Prepare a logger object with the ability to overwrite the log level
        at run time (via the `LOG_LEVEL` environment variable)
    :param name: Name of the logger (defaults to None)
    :type name: str
    :return: The logger
    :rtype: Logger
    """
    if _is_running_lambda():
        logger = get_lambda_logger(name)
    else:
        logger = get_default_logger(name)
    level = logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO"))
    logger.setLevel(level)
    return logger
