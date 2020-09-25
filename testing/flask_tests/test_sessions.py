import unittest
import flask
import os
from datetime import datetime
from site_main import app
import session_management
import time


class FlaskTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True

    def test_generate_session_token(self):
        """
        Asserts that the session token is successfully created (10 chars long)
        """
        active_sessions = {}
        session_token = session_management.generate_session_token(
            active_sessions)
        self.assertEqual(len(session_token), 10)

    def test_generate_new_session(self):
        """
        Asserts a session with the key 'public_user' is created
        Test adapted from https://flask.palletsprojects.com/en/1.1.x/testing/]
        """
        with app.test_client() as test_client:
            test_client.get('/')
            self.assertIsNot(flask.session['public_user'], None)

    def test_update_existing_session(self):
        """
        Asserts that the value in active sessions gets updated
        Example dict is created with test data.txt, function is called to
        update the value
        Assert checks that the updated timestamp != the initial
        """
        with app.test_client() as test_client:
            test_client.get('/')
            time_stamp = datetime.now()
            active_sessions = {flask.session['public_user']: time_stamp}
            session_management.update_existing_session(active_sessions)
            self.assertTrue(active_sessions.get(
                flask.session['public_user']) is not time_stamp)

    def test_check_existing_sessions_false(self):
        """
        Asserts False is returned when session key is not within session
        dictionary
        """
        active_sessions = {'test_session': "test_value"}
        test_boolean = session_management.check_existing_sessions(
            "key_to_check", active_sessions)
        self.assertFalse(test_boolean)

    def test_check_existing_sessions_true(self):
        """
        Asserts True is returned when session key is within session
        dictionary
        """
        active_sessions = {'test_session': "test_value"}
        test_boolean = session_management.check_existing_sessions(
            "test_session", active_sessions)
        self.assertTrue(test_boolean)

    def test_compare_times(self):
        """
        Asserts that the difference in the timestamps is between
        5 - 6 seconds
        Unable to do exact time because of variation in milliseconds when
        tests run
        """
        test_time = datetime.now()
        time.sleep(5)
        difference = session_management.compare_times(test_time)
        print(difference)
        self.assertTrue(5 <= difference <= 6)

    def test_folder_is_created(self):
        """
        Checks that the session creation creates a folder
        """
        with app.test_client() as test_client:
            test_client.get('/')
            self.assertTrue(os.path.exists(
                'uploads/' + flask.session['public_user']))

    def test_clean_up_of_session_folder(self):
        """
        Asserts that the session clean up functionality works as expected
        with regard to folder deletion
        """
        active_sessions = {}
        with app.test_client() as test_client:
            test_client.get('/')
            active_sessions[flask.session['public_user']] = datetime.now()
            session_management.clean_up_sessions(
                flask.session['public_user'], 'uploads/', active_sessions)
            self.assertFalse(os.path.exists(
                'uploads/' + flask.session['public_user']))

    def test_removal_from_active_session(self):
        """
        Asserts that the session clean up functionality works as expected
        with regard to removing k,v pairs from the active_session dict
        """
        active_sessions = {}
        with app.test_client() as test_client:
            test_client.get('/')
            active_sessions[flask.session['public_user']] = datetime.now()
            session_management.clean_up_sessions(
                flask.session['public_user'], 'uploads/', active_sessions)
            self.assertTrue(
                flask.session['public_user'] not in active_sessions)

    def test_clean_uploads_on_start(self):
        """
        Asserts that the folder that is created within this test is deleted
        upon function call.
        """
        os.mkdir('uploads/test_clean_up_folder')
        session_management.clean_uploads_on_start('uploads/')
        self.assertFalse(os.path.exists('uploads/' + 'test_clean_up_folder'))
