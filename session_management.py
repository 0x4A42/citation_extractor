import config
from datetime import datetime
from flask import session
import logging
import random
import os
import string
import shutil


def generate_session_token(active_sessions, string_length=10):
    """Generates a random session token for a user without an existing
        session.
        Will check against other existing sessions to ensure the generated
        string isn't currently used by an existing session.
        String generator:
        https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits

    Args:
        active_sessions (dictionary): Contains all active sessions, as there
        exists the possibility of generating the same token.
        string_length (int, optional): The length of the token. Defaults to 10.

    Returns:
        token (string): The generated token which will be used for the
                         session name.
    """
    continue_loop = True
    while continue_loop is True:
        session_token_charset = string.ascii_letters + string.digits
        token = ''.join((random.choice(session_token_charset)
                         for i in range(string_length)))
        if check_existing_sessions(token, active_sessions) is True:
            continue
        else:
            continue_loop = False
    return token


def generate_new_session(active_sessions):
    """Generates a new session if one does not exist.
        Creates a new directory to store the files of this session.
        Stores session and timestamp in dict as k,v respectively in order to
        manage sessions.

    Args:
        active_sessions (dictionary): Contains all active sessions, as there
        exists the possibility of generating the same token.

    Returns:
        active_sessions (dictionary): Updated dictionary of active sessions.
        Key = session token, value = last request timestamp.
    """
    session_token = generate_session_token(active_sessions)
    logging.info("New session generated: " + session_token)
    session['public_user'] = session_token
    active_sessions[session_token] = datetime.now()
    os.mkdir('uploads/'+session['public_user'])


def update_existing_session(active_sessions):
    """Updates the value of the session in the management dictionary with
    a current timestamp.

    Args:
        active_sessions (dictionary): Dictionary containing session info.
        key = session token, value = last request timestamp.

    Returns:
        active_sessions (dictionary): Updated dictionary of active sessions.
        Key = session token, value = last request timestamp.
    """
    session_name = session.get('public_user')
    logging.info("New request from " + str(session_name))
    active_sessions[session_name] = datetime.now()


def check_existing_sessions(session_key, active_sessions):
    """Checks the existing sessions to see if token is in use.

    Args:
        session_key (string): The proposed session name.
        active_sessions (dictionary): Dictionary containing session info.
        key = session token, value = last request timestamp.

    Returns:
        True (Boolean): Indicates the session name is already in use.
        False (Boolean): Indicates the session name is not in use.
    """
    if session_key in active_sessions:
        return True
    else:
        return False


def compare_times(session_time):
    """This function generates the difference (in seconds) between
    a current datetime.now() and the last request time of the session
    (the arg).

    Args:
        session_time (datetime): The last access time from the session.

    Variables:
        current_time (datetime): the current time when this is called.

    Returns:
        in_seconds (int): The difference in seconds between the current
        timestamp and arg.
    """
    current_time = datetime.now()
    difference = current_time - session_time
    in_seconds = difference.total_seconds()
    return in_seconds


def clean_up_sessions(session_to_clean, upload_folder, active_sessions):
    """This function cleans up an existing session when it has not had
    activity for a certain period of time.
    First, deletes the directory created for the session.
    Then, removes the session from the active_sessions dict.

    Args:
        session_to_clean (string): The session name which is to be cleaned
        up.
        upload_folder (string): Path to the uploads folder.
        active_sessions (dictionary): A dictionary of active sessions.
        Key = session token, value = last request timestamp.

    Returns:
        active_sessions (dictionary): Updated dictionary of active sessions.
        Key = session token, value = last request timestamp.
    """
    shutil.rmtree(upload_folder + session_to_clean)
    logging.info("Cleaning up expired session: " + session_to_clean)
    del active_sessions[session_to_clean]


def clean_uploads_on_start(upload_folder):
    """Cleans the uploads directory by deleting all existing folders in there
        upon server start up.

        Args:
        upload_folder (string): The path to the uploads folder.
    """
    file_names = os.listdir(upload_folder)
    if len(file_names) >= 1:
        for file_name in file_names:
            try:
                logging.info("Deleting folder for session: " + file_name)
                shutil.rmtree(upload_folder + file_name)
            except FileNotFoundError:
                logging.error(file_name + " not available to delete")
            except PermissionError:
                logging.error(file_name + " could not be deleted due to lack\
                                of permissions. A file or folder may be open.")
