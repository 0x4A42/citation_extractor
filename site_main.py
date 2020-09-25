from apscheduler.schedulers.background import BackgroundScheduler
import config
import file_uploader
import file_processing
from flask import Flask, render_template, request, redirect, \
    send_from_directory, session
import logging
import log_management
import os
import session_management
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_pyfile('config.py')
# Dictionary that will track sessions. Key = session name, value = last request
active_sessions = {}


def check_recent_activity():
    """ Every two hours, this will run using APScheduler and will iterate
        through active_sessions.
        It will check when a request was last made by a session in the dict.
        If the last request was > 1 hour ago, it will delete the directory
        associated with the session, and remove it from the dict.
        The session has a lifespan of 1 hour and will have naturally expired.
    """
    # Makes function uses the global dict and not create a local one
    global active_sessions
    if len(active_sessions) >= 1:  # Checks there is at least 1 active session
        # Creates a copy of the dict, at there is the
        # possibility of dictionary changing as iteration occurs
        for session_token, last_request in active_sessions.copy().items():
            if session_management.compare_times(last_request) > \
                    config.MAX_SESSION_LENGTH_SECONDS:
                logging.info("Cleaning up session " + str(session_token))
                session_management.clean_up_sessions(
                    session_token,
                    config.UPLOAD_FOLDER,
                    active_sessions)
            else:
                continue
    else:
        logging.info("No sessions to check.")


def move_log_to_archive():
    """This is a function that when called will move the
    current_log file into the archive to ensure that the logs are consistently
    moved and that they only contain the data for a day's activity.
    """
    logging.warning("Current logging file being renamed and moved to archive.")
    logging.shutdown()
    try:
        new_log_file_name = log_management.rename_log(
            config.DEFAULT_LOG_NAME)
        log_management.move_log(new_log_file_name)
    except FileNotFoundError:
        print("Current log file not found")
    except PermissionError:
        logging.error("Permissions lacking to rename or move log.")


# Schedules tasks to be ran at specific intervals:
# check_recent_activity() to ran every two hours and clear up sessions
# move_log_daily() to be ran daily (at 23:59:59) to move the logging file
scheduler = BackgroundScheduler()
session_job = scheduler.add_job(check_recent_activity, 'interval', hours=2)
logging_job = scheduler.add_job(move_log_to_archive, 'cron', hour=23,
                                minute=59, second=59)
scheduler.start()


# This route will process how the index page is handled.
@app.route('/', methods=['POST', 'GET'])
def index_page():
    """ Default method for the index page. Initially will check if a session
        exists, if so it will update the key in the active_sessions dict.
        Else, will create a new session through calling generate_new_session()
        It will then call either index_post_request() or index_get_request
        depending on the request received.
    """
    # Makes function uses the global dict and not create a local one
    global active_sessions
    if session:  # If session exists, updates key with current datetime
        session_management.update_existing_session(
            active_sessions)
    else:  # Else, creates new session
        session_management.generate_new_session(
            active_sessions)
    upload_path = config.UPLOAD_FOLDER + \
        str(session['public_user'])

    if 'download_results' in request.form:
        return send_from_directory(config.UPLOAD_FOLDER
                                   + str(session['public_user']),
                                   config.RESULTS_ZIP,
                                   as_attachment=True)

    if request.method == "POST":
        file_uploader.clean_up_directory(upload_path)
        if index_post_request(upload_path) is True:
            return render_template('index.html', is_home='yes',
                                   has_results='yes')
        else:
            return render_template('index.html', is_home='yes')
    elif request.method == "GET":
        if index_get_request(upload_path) is True:
            return render_template('index.html', is_home='yes',
                                   has_results='yes')
        else:
            return render_template('index.html', is_home='yes')


def index_post_request(upload_path):
    """This function handles how the index.html page processes data.txt and
        serves the page when a post request is received.

        It will first check if there is a file request, and if so will iterate
        through each file validating them to ensure that they have a file name,
        are of the right extension and are between two file sizes.

        If they fail any validation, the file is disregarded.
        Else, file is saved into a directory unique for the user's session.
        Then, calls functions to extract and process the citations within the
        files that have been successfully saved, using a loader based on
        the file extension.

    Args:
        upload_path (string): The upload directory - a combination of /
        "upload/" + the session name

    Variables:
        files_processed (dictionary): Tracks the amount of files processed.
        If True (meaning a file has been successfully processed) >= 1,
        a zip is created and the download button is shown to the user]
    Returns:
        render_template: Serves the index.html page
        send_from_directory: Downloads the results zip for the client
    """
    if request.files:
        files_processed = {"True": 0, "False": 0}
        files = request.files.getlist("uploaded_file")

        # loop, as possibility of multiple file uploads
        for file_to_upload in files:
            # Gets the length of the file
            file_to_upload.seek(0, os.SEEK_END)
            file_length = file_to_upload.tell()
            # reset pointer to start of file, otherwise will be empty
            file_to_upload.seek(0)
            # Secures file name against user input
            file_name = secure_filename(file_to_upload.filename)
            # Checks the file name isn't blank
            if file_uploader.check_file_name_empty(file_name) is True:
                logging.info("Error uploading " + file_to_upload.filename
                             + "from " + str(session['public_user']) +
                             "- empty file name.")
                files_processed['False'] += 1
                continue
            # Checks the file has an allowed extension
            elif file_uploader.allowed_ext(file_to_upload.filename,
                                           config.
                                           ALLOWED_EXTENSIONS) is False:
                logging.info("Error uploading " + file_to_upload.filename
                             + "from " + str(session['public_user']) +
                             "- extension not supported.")
                files_processed['False'] += 1
                continue
            # Checks file size
            elif file_uploader.check_file_length(file_length,
                                                 config.MAX_FILE_SIZE,
                                                 config.MIN_FILE_SIZE
                                                 ) is False:
                logging.info("Error uploading " + file_to_upload.filename
                             + "from " + str(session['public_user']) +
                             file_to_upload.filename +
                             " invalid file size.")
                files_processed['False'] += 1
                continue
            else:  # Else, passes all validation and is saved.
                files_processed['True'] += 1
                file_name = file_uploader.check_existing_file_name(
                    file_name, "uploads/")
                file_path = upload_path + "/" + file_name
                file_to_upload.save(file_path)
                citations = file_processing.extract_citations(file_path)
                results = file_processing.start_citation_analysis(citations)
                file_processing.write_citations_to_file_json(
                    results, upload_path)

        # If files have been processed,
        #       return a render with the file download.
        if files_processed['True'] >= 1:
            # file_processing.generate_results_chart(
            # upload_path)
            file_processing.create_zip(upload_path,
                                       config.RESULTS_ZIP)
            return True
        else:  # Else, normal redirect.
            return False
        # If user clicked download results button
    else:  # If no files request, redirect to index.
        return redirect(request.url)


def index_get_request(upload_path):
    """ Processes how the page is served upon a GET request being received.
        If files have been processed and a results_file.zip exists in the
        directory for this session, returns a render with has_results
        var which will allow the user to download their results.

    Args:
        upload_path (string): The upload directory - a combination of /
        "upload/" + the session name

    Returns:
        True (Boolean): A results file exists in this session's upload
        directory, returns True to render a version of the webpage
        with a download button]
        False (Boolean): No results file exists. Returns False to render a
        normal render of the index page.
    """
    if os.path.isfile(upload_path + "/" + config.RESULTS_ZIP):
        return True
    else:
        return False


# This route will process how the About page is handled.
@ app.route('/about')
def about_page():
    """ Serves the about page.

    Returns:
        render_template: A normal render of the about page.
        is_about variable is used to control navigation bar colour.
    """
    return render_template('about.html', is_about='yes')


# This route will process how the Github links page is handled.
@ app.route('/github')
def download_links():
    """ Serves the github page.

    Returns:
        render_template: A normal render of the github page.
        is_github variable is used to control navigation bar colour.
    """
    return render_template('github.html', is_github='Yes')


if __name__ == "__main__":
    """Runs the webserver.

    Logs are checked to be moved into the archive both when the webserver
    starts, in case of any old log existing, and when the code hits
    the finally block.
    """
    try:
        move_log_to_archive()
        session_management.clean_uploads_on_start(config.UPLOAD_FOLDER)
        logging.info("Server has been started.")
        app.run(debug=False)
    finally:
        try:
            move_log_to_archive()
            session_management.clean_uploads_on_start(config.UPLOAD_FOLDER)
        except FileNotFoundError:
            print("Current log file not found")
        except PermissionError:
            print("Permissions lacking to rename or move file.")
