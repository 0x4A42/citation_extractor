import file_uploader
import flask
import logging
import os
from site_main import app
import shutil
import unittest


class FlaskTest(unittest.TestCase):

    allowed_extensions = [
        'TXT', 'PDF', 'DOCX', 'BIBTEXT', 'DBLP']
    max_file_size = (16 * 1000 * 1000)
    min_file_size = 1000
    upload_folder = 'uploads/'

    def setUp(self):
        app.config['TESTING'] = True
        logging.shutdown()

    def test_allowed_ext_true(self):
        """
        Asserts that the file extension is within the list of allowed
        extensions
        """
        test_file_name = "test_file.pdf"
        self.assertTrue(file_uploader.allowed_ext(
            test_file_name, FlaskTest.allowed_extensions))

    def test_allowed_ext_false(self):
        """
        Asserts that the file extension is not within the list of allowed
        extensions
        """
        test_file_name = "test_file.jpg"
        self.assertFalse(file_uploader.allowed_ext(
            test_file_name, FlaskTest.allowed_extensions))

    def test_check_file_name_empty_true(self):
        """
        Asserts True when file name is empty
        """
        test_empty_file_name = ""
        self.assertTrue(
            file_uploader.check_file_name_empty(test_empty_file_name))

    def test_check_file_name_empty_false(self):
        """
        Asserts False is file name is not empty
        """
        test_empty_file_name = "test_file.pdf"
        self.assertFalse(
            file_uploader.check_file_name_empty(test_empty_file_name))

    def test_check_file_length_true_lower_boundary(self):
        """
        Asserts True - shows that the file length is within the
        acceptable range. This test is checking the lower file
        length boundary
        """
        file_length = 1000
        self.assertTrue(file_uploader.check_file_length(
            file_length, FlaskTest.max_file_size, FlaskTest.min_file_size))

    def test_check_file_length_true_lower(self):
        """
        Asserts True - showing that the file length is within the
        acceptable range. This test is checking a lower file length
        """
        file_length = 1001
        self.assertTrue(file_uploader.check_file_length(
            file_length, FlaskTest.max_file_size, FlaskTest.min_file_size))

    def test_check_file_length_true_upper_boundary(self):
        """
        Asserts True - showing that the file length is within the
        acceptable range. This test is checking the upper file length
        boundary
        """
        file_length = 16 * 1000 * 1000
        self.assertTrue(file_uploader.check_file_length(
            file_length, FlaskTest.max_file_size, FlaskTest.min_file_size))

    def test_check_file_length_true_upper(self):
        """
        Asserts True - showing that the file length is within the
        acceptable range. This test is checking an upper file length
        """
        file_length = 15999999
        self.assertTrue(file_uploader.check_file_length(
            file_length, FlaskTest.max_file_size, FlaskTest.min_file_size))

    def test_check_file_length_true_middle(self):
        """
        Asserts True - showing that the file length is within the
        acceptable range. This test is checking a middle file length
        """
        file_length = 8 * 1000 * 1000
        self.assertTrue(file_uploader.check_file_length(
            file_length, FlaskTest.max_file_size, FlaskTest.min_file_size))

    def test_check_file_length_false_lower(self):
        """
        Asserts False - showing that that the file length is not within
        the acceptable range. This test is checking the lower file length
        boundary
        """
        file_length = 999
        self.assertFalse(file_uploader.check_file_length(
            file_length, FlaskTest.max_file_size, FlaskTest.min_file_size))

    def test_check_file_length_false_upper(self):
        """
        Asserts False - showing that that the file length is not within
        the acceptable range. This test is checking the upper file length
        boundary
        """
        file_length = 16000001
        self.assertFalse(file_uploader.check_file_length(
            file_length, FlaskTest.max_file_size, FlaskTest.min_file_size))

    def test_check_existing_file_name_true(self):
        """
        Asserts True - showing that the file name would be renamed as the
        original file already existed within the directory
        """
        with app.test_client() as test_client:
            test_client.get('/')
            shutil.copyfile('../test_documents/sample_citations_second.docx',
                            'uploads/' + flask.session['public_user']
                            + '/sample_citations_second.docx')
            test_file_name = "sample_citations_second.docx"
            new_file_name = file_uploader.check_existing_file_name(
                test_file_name, FlaskTest.upload_folder)
            self.assertTrue(new_file_name is not test_file_name)

    def test_check_existing_file_name_false(self):
        """
        Asserts True - showing that the file name would not be renamed as the original
        file name did not exist within the directory
        """
        with app.test_client() as test_client:
            test_client.get('/')
            shutil.copyfile('../test_documents/sample_citations_second.docx',
                            'uploads/' + flask.session['public_user']
                            + '/sample_citations_second.docx')
            test_file_name = "test_file_name.docx"

            new_file_name = file_uploader.check_existing_file_name(
                test_file_name, FlaskTest.upload_folder)
            self.assertTrue(new_file_name is test_file_name)

    def test_clean_up_directory(self):
        """
        Asserts that the number of files in a folder (which has 1 file
        moved into it) is 0 after the function call
        File counter from
        https://stackoverflow.com/questions/27694713/count-files-in-folder-by-python-programming
        """
        upload_folder = 'test_cleanup/'
        shutil.copyfile('../test_documents/sample_citations_second.docx',
                        'test_cleanup/sample_citations_second.docx')
        num_files = len([f for f in os.listdir(upload_folder)
                         if os.path.isfile(os.path.join(upload_folder, f))])
        file_uploader.clean_up_directory(upload_folder)
        num_files = len([f for f in os.listdir(upload_folder)
                         if os.path.isfile(os.path.join(upload_folder, f))])
        self.assertTrue(num_files == 0)


if __name__ == "__main__":
    unittest.main()
