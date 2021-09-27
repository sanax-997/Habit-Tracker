from bridge import app
import unittest


class TestViews(unittest.TestCase):

    def test_home(self):
        """
        Test that views.home is accessible without login
        """
        tester = app.test_client(self)
        response = tester.get('/')
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_register(self):
        """
        Test that views.register is accessible without login
        """
        tester = app.test_client(self)
        response = tester.get('/register')
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_login(self):
        """
        Test that views.login is accessible without login
        """
        tester = app.test_client(self)
        response = tester.get('/login')
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_analytics(self):
        """
        Test that views.analytics is inaccessible without login
        """
        tester = app.test_client(self)
        response = tester.get('/analytics')
        statuscode = response.status_code
        self.assertEqual(statuscode, 302)

    def test_habits(self):
        """
        Test that views.habits is inaccessible without login
        """
        tester = app.test_client(self)
        response = tester.get('/habits')
        statuscode = response.status_code
        self.assertEqual(statuscode, 302)

    def test_delete(self):
        """
        Test that views.delete.task is inaccessible without login
        """
        tester = app.test_client(self)
        response = tester.get('/delete/task')
        statuscode = response.status_code
        self.assertEqual(statuscode, 302)

    def test_check(self):
        """
        Test that views.check.task is inaccessible without login
        """
        tester = app.test_client(self)
        response = tester.get('/check/task')
        statuscode = response.status_code
        self.assertEqual(statuscode, 302)


if __name__ == "__main__":
    app.config['TESTING'] = True
    unittest.main()
