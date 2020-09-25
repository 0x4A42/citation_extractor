import unittest
from site_main import app


class FlaskTest(unittest.TestCase):

    """
    Test adapted from: https://www.youtube.com/watch?v=UZyZw4tYJMI
    """
    def setUp(self):
        app.config['TESTING'] = True

    def test_index_route(self):
        """
        Check for response 200 on the index page
        """
        tester = app.test_client()
        response = tester.get('/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_index_route_post(self):
        """
        Check for response 200 on the index page
        """
        tester = app.test_client()
        response = tester.post('/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_index_loads(self):
        """
        Checks that the page loads properly by checking for the title
        in response data
        """
        tester = app.test_client()
        response = tester.get('/')
        self.assertTrue(b'Citation Extractor' in response.data)

    def test_about_route(self):
        """
        Check for response 200 on the about page
        """
        tester = app.test_client()
        response = tester.get('/about')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_about_loads(self):
        """
        Checks that the about page loads by checking if the title
        is in the response data
        """
        tester = app.test_client()
        response = tester.get('/about')
        self.assertTrue(b'Under the Hood' in response.data)

    def test_github_route(self):
        """
        Check for response 200 on the GitHub page
        """
        tester = app.test_client()
        response = tester.get('/github')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_github_loads(self):
        """
        Checks that the GitHub page loads by checking if the title is
        in the response data
        """
        tester = app.test_client()
        response = tester.get('/github')
        self.assertTrue(b'GitHub Repos' in response.data)

    def test_false_route(self):
        """
        Checks for response 404 on route that does not exist
        """
        tester = app.test_client()
        response = tester.get('/test')
        status_code = response.status_code
        self.assertEqual(status_code, 404)


if __name__ == "__main__":
    unittest.main()
