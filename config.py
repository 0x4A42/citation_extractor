from datetime import timedelta
from flask import app, Flask
import logging


"""This module is a config file.

Logging config from:
https://www.youtube.com/watch?v=-ARI4Cz-awo
"""

logging.basicConfig(filename='current_log.log', level=logging.INFO,
                    filemode='a',
                    format='%(asctime)s:%(levelname)s:%(message)s')

UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = [
    'TXT', 'PDF', 'DOCX']
DEFAULT_LOG_NAME = 'current_log.log'
MIN_FILE_SIZE = 1000   # 1KB minimum file size
MAX_FILE_SIZE = 16 * 1000 * 1000  # 16MB max file size
GRAPH_FILE = "results_graph.png"
JSON_FILE_NAME = 'output.txt'
RESULTS_ZIP = "results_files.zip"
MAX_SESSION_LENGTH_SECONDS = 3600
SECRET_KEY = "8Z!dNgVcP]Rk.A[@V$"
PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
