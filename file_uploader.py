import config
from datetime import datetime
from flask import session
import logging
import os
# Validation adapted from:
# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

"""
This module is responsible for validating files uploaded by users.
Will check that files are of the right type, size and have a name.
A function also exists to rename files if the same file name and extension are
uploaded.
Also a function to clean up files within a directory to ensure independence of
results.
"""


def allowed_ext(file_name, allowed_extensions):
    """Checks that the file extension of the uploaded file(s) are permitted.
        Returns a Boolean to this effect.
        File name split from:
        https://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python

    Args:
        file_name (string): Name of uploaded file
        allowed_extensions (dict): Dictionary containing allowed file
        extensions

    Returns:
        True (Boolean): Indicates ext is within allowed_extensions dict
        False (Boolean): Indicates ext is not within allowed_extensions dict
    """
    if "." not in file_name:
        return False
    ext = file_name.rsplit(".", 1)[1]
    if ext.upper() in allowed_extensions:
        return True
    else:
        return False


def check_file_name_empty(file_name):
    """Checks that the file name isn't blank

    Args:
        file_name (string): Name of uploaded file

    Returns:
        True (Boolean): Indicates file name is null
        False (Boolean): Indicates file name is not null
    """
    checked_file_name, file_extension = os.path.splitext(file_name)
    if checked_file_name is None or file_extension is None or checked_file_name == "" or file_extension == "":
        return True
    else:
        return False


def check_file_length(file_length, max_file_size, min_file_size):
    """Checks that the file size is within the min and max params

    Args:
        file_length (int): Size of the file in bytes
        max_file_size (int): Maximum allowed file size in bytes
        min_file_size (int): Minimum allowed file size in bytes

    Returns:
        True (Boolean): Indicates the file length is within params.
        False (Boolean): Indicates the file length is not within params.
    """

    if max_file_size >= file_length >= min_file_size:
        return True
    else:
        return False


def check_existing_file_name(uploaded_file_name, upload_folder):
    """Checks if a file in the uploads directory already has this name
        If a file already exists with this name, splits the file name string
        and appends the current datetime to the file name
        Then, stitches the filename back together and returns it.
        Else, returns file name as was uploaded.
        File name split from:
        https://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python

    Args:
        uploaded_file_name (string): The name of the file that is being checked
        upload_folder (string): Path to the upload folder for this
        user's session

    Returns:
        file_name_return (string): The file name to return, either the original
        or the updated if file exists with original name.
        """
    file_names = os.listdir(
        upload_folder + str(session['public_user']))
    file_name_return = uploaded_file_name
    for file_name in file_names:
        if uploaded_file_name == file_name:
            new_file_name, file_extension = os.path.splitext(file_name)
            new_file_name = new_file_name + datetime.now().strftime(
                "%Y-%m-%d_%H_%M_%S")
            file_name_return = new_file_name + file_extension
        else:
            pass
    return file_name_return


def clean_up_directory(upload_folder):
    """Cleans out existing files in the directory, so each batch of
        files uploaded only parses those specific files.
        Try except as there is the possibility of the session management
        deleting the folder as this runs, don't want the system to crash.]

    Args:
        upload_folder (string): Path to the uploads folder
    """
    file_names = os.listdir(upload_folder)
    if len(file_names) >= 1:
        for file_name in file_names:
            try:
                logging.info("Deleting file: " + file_name)
                os.remove(upload_folder + "/" + file_name)
            except FileNotFoundError:
                logging.warning(file_name + " not found to delete.")
