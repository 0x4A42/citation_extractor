import unittest
from site_main import app
import os
import log_management
import logging
import time


class FlaskTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        logging.shutdown()

    def test_logging_file_exists(self):
        """
        Checks that the logging file is successfully created
        """
        logging.info('Testing file exists')
        logging.shutdown()
        self.assertTrue(os.path.exists('current_log.log'))

    def test_logging_file_renamed(self):
        """
        Checks that the log is successfully renamed
        """
        log_name = 'current_log.log'
        with open(log_name, "w") as file:
            file.write("Log created for test")
        new_file_name = log_management.rename_log(log_name)
        self.assertTrue(os.path.exists(new_file_name))
        os.remove(new_file_name)

    def test_logging_file_moved(self):
        """
        Checks that the log is successfully moved into the /logs folder
        """
        logging.info('Testing file moving')
        logging.shutdown()
        time.sleep(1)
        new_file_name = log_management.rename_log('current_log.log')
        log_management.move_log(new_file_name)
        self.assertTrue(os.path.exists('logs/' + new_file_name))

    # Checks the check_log_on_startup function
    def test_check_file_on_startup(self):
        logging.info('Testing file on start up')
        logging.shutdown()
        log_management.check_log_on_startup('current_log.log')
        self.assertFalse(os.path.exists('current_log.log'))


if __name__ == "__main__":
    unittest.main()
