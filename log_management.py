import config
from datetime import datetime
import logging
import shutil
import os

"""This module deals with the log management of the system.
Functions rename and move log files.
"""


def check_log_on_startup(file_name):
    if os.path.exists(file_name):
        move_log(rename_log(file_name))


def move_log(file_name):
    """Moves the log fom the main directory into the log archive directory

    Args:
        file_name (string): File name of the log
    """
    src_location = file_name
    if os.path.exists(src_location):
        try:
            shutil.move(src_location, "logs")
        except FileExistsError:
            logging.error("Could not move " + file_name + ". File name \
                already present in archive")


def rename_log(current_file_name):
    """Renames the current log to log_ + current date for archiving purposes

    Args:
        current_file_name (string): Current file name, which will be
        'current_log.log'

    Returns:
        new_file_name (string): The new file name, which will be something
        such as 'log_2020-07-24'
    """
    new_file_name = "log_" + datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + \
        '.log'
    try:
        os.rename(current_file_name, new_file_name)
    except FileExistsError:
        logging.error("Could not rename " + current_file_name + ". New file \
            name '" + new_file_name + "' already exists")
    return new_file_name
