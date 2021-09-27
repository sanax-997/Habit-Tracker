import unittest
import os

from datetime import date, timedelta
from flask import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestBase(unittest.TestCase):

    def setUp(self):
        """
        setUp is defined by the unittest framework
        This function is called every time a test starts
        and is the set up for the tests
        """
        # Creates an instance of the webdriver wiht the Chrom webdriver located in the program directory
        self.driver = webdriver.Chrome(
            "chromedriver.exe")
        # The domain of the localhost server is retrieved
        self.driver.get("http://127.0.0.1:5000/")

        # Click register button on the nav bar
        self.driver.find_element_by_id("register").click()

        # Waits for the registration elements to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
        except:
            self.driver.close()

        # Fill in the registration Form
        self.driver.find_element_by_id("email").send_keys("test@hotmail.com")
        self.driver.find_element_by_id("username").send_keys("Test")
        self.driver.find_element_by_id("password1").send_keys("password")
        self.driver.find_element_by_id("password2").send_keys("password")
        self.driver.find_element_by_id("submit").click()

    def tearDown(self):
        """
        tearDown is defined by the unittest framework
        This function is called every time a test end
        and is the clean up of tests to reset everything
        """

        # Waits for the logout element to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "logout"))
            )
        except:
            self.driver.close()

        # Logs out of the application
        self.driver.find_element_by_id("logout").click()

        # Removes the Test file created in the setUp
        os.remove('./Data/Test.json')

        # Quits the webdriver
        self.driver.quit()


class TestRegistration(TestBase):

    def test_server_is_running(self):
        """
        The basic test function, which checks if the server is running
        """

        # Asserts if the domain string is in the current url of the driver
        assert 'http://127.0.0.1:5000/' == self.driver.current_url

    def test_register(self):
        """
        Test that a user can create an account using the registration form
        if all fields are filled out correctly, and that they will be
        redirected to the home page. If the registration form is filled out
        incorrectly a user account wont be created.
        """

        # User needs to be logged out to access register
        self.driver.find_element_by_id("logout").click()

        # Click register button on the nav bar
        self.driver.find_element_by_id("register").click()

        # Waits for the registration elements to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
        except:
            self.driver.close()

        # Fill in the false registration form for email (Less than 4 characters)
        self.driver.find_element_by_id("email").send_keys("t@t")
        self.driver.find_element_by_id("username").send_keys("Test2")
        self.driver.find_element_by_id("password1").send_keys("password")
        self.driver.find_element_by_id("password2").send_keys("password")
        self.driver.find_element_by_id("submit").click()

        # Asserts error message is shown
        error_message = self.driver.find_element_by_class_name(
            "alert").text
        assert "Email must be greater than 3 characters!" in error_message

        # Asserts error message is closed
        self.driver.find_element_by_class_name("close").click()
        AssertionError(self.driver.find_element_by_class_name("alert"))

        # Fill in the false registration form for username (Less than 1 character)
        self.driver.find_element_by_id("email").send_keys("test2@hotmail.com")
        self.driver.find_element_by_id("username").send_keys("")
        self.driver.find_element_by_id("password1").send_keys("password")
        self.driver.find_element_by_id("password2").send_keys("password")
        self.driver.find_element_by_id("submit").click()

        # Asserts error message is shown
        error_message = self.driver.find_element_by_class_name(
            "alert").text
        assert "Username must be at least 1 character!" in error_message

        # Asserts error message is closed
        self.driver.find_element_by_class_name("close").click()
        AssertionError(self.driver.find_element_by_class_name("alert"))

        # Fill in the false registration form for password (not matching)
        self.driver.find_element_by_id("email").send_keys("test2@hotmail.com")
        self.driver.find_element_by_id("username").send_keys("Test2")
        self.driver.find_element_by_id("password1").send_keys("password1")
        self.driver.find_element_by_id("password2").send_keys("password2")
        self.driver.find_element_by_id("submit").click()

        # Asserts error message is shown
        error_message = self.driver.find_element_by_class_name(
            "alert").text
        assert "The passwords do not match!" in error_message

        # Asserts error message is closed
        self.driver.find_element_by_class_name("close").click()
        AssertionError(self.driver.find_element_by_class_name("alert"))

        # Fill in the false registration form for password (Too short)
        self.driver.find_element_by_id("email").send_keys("test2@hotmail.com")
        self.driver.find_element_by_id("username").send_keys("Test2")
        self.driver.find_element_by_id("password1").send_keys("pas")
        self.driver.find_element_by_id("password2").send_keys("pas")
        self.driver.find_element_by_id("submit").click()

        # Asserts error message is shown
        error_message = self.driver.find_element_by_class_name(
            "alert").text
        assert "The password must be greater than 3 characters!" in error_message

        # Asserts error message is closed
        self.driver.find_element_by_class_name("close").click()
        AssertionError(self.driver.find_element_by_class_name("alert"))

        # Fill in the false registration form for username (Already existing)
        self.driver.find_element_by_id("email").send_keys("test2@hotmail.com")
        self.driver.find_element_by_id("username").send_keys("Test")
        self.driver.find_element_by_id("password1").send_keys("password")
        self.driver.find_element_by_id("password2").send_keys("password")
        self.driver.find_element_by_id("submit").click()

        # Asserts error message is shown
        error_message = self.driver.find_element_by_class_name(
            "alert").text
        assert "his username already exists!" in error_message

        # Asserts error message is closed
        self.driver.find_element_by_class_name("close").click()
        AssertionError(self.driver.find_element_by_class_name("alert"))

        # Fill in the correct registration form
        self.driver.find_element_by_id("email").send_keys("test2@hotmail.com")
        self.driver.find_element_by_id("username").send_keys("Test2")
        self.driver.find_element_by_id("password1").send_keys("password")
        self.driver.find_element_by_id("password2").send_keys("password")
        self.driver.find_element_by_id("submit").click()

        # Waits for the homepage elements to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, "picture"))
            )
        except:
            print("Element not found on homepage")
            self.driver.close()

        # Asserts that the browser redirects to the homepage
        assert 'http://127.0.0.1:5000/' in self.driver.current_url

        # Asserts success message is shown
        success_message = self.driver.find_element_by_class_name(
            "alert").text
        assert "Account created!" in success_message

        # Remove the Test2 json file from the Data folder
        os.remove('./Data/Test2.json')

    def test_login(self):
        """
        Test that a user can login and that they will be redirected to
        the homepage. If the login form is filled out
        incorrectly a user account wont be created.
        """
        # User needs to be logged out to access login
        self.driver.find_element_by_id("logout").click()

        # Click login button on the nav bar
        self.driver.find_element_by_id("login").click()

        # Waits for the login elements to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
        except:
            self.driver.close()

        # Fill in the false login form (Non exisiting username)
        self.driver.find_element_by_id("username").send_keys("Test2")
        self.driver.find_element_by_id("password").send_keys("password")
        self.driver.find_element_by_id("login_button").click()

        # Asserts error message is shown
        error_message = self.driver.find_element_by_class_name(
            "alert").text
        assert "The username does not exist!" in error_message

        # Asserts error message is closed
        self.driver.find_element_by_class_name("close").click()
        AssertionError(self.driver.find_element_by_class_name("alert"))

        # Fill in the false login form (Wrong password)
        self.driver.find_element_by_id("username").send_keys("Test")
        self.driver.find_element_by_id("password").send_keys("password1")
        self.driver.find_element_by_id("login_button").click()

        # Asserts error message is shown
        error_message = self.driver.find_element_by_class_name(
            "alert").text
        assert "The password is wrong!" in error_message

        # Asserts error message is closed
        self.driver.find_element_by_class_name("close").click()
        AssertionError(self.driver.find_element_by_class_name("alert"))

        # Fill in the correct form
        self.driver.find_element_by_id("username").send_keys("Test")
        self.driver.find_element_by_id("password").send_keys("password")
        self.driver.find_element_by_id("login_button").click()

        # Asserts that the browser redirects to the homepage
        assert 'http://127.0.0.1:5000/' in self.driver.current_url

        # Asserts success message is shown
        success_message = self.driver.find_element_by_class_name(
            "alert").text
        assert "Logged in successfully" in success_message

    def test_logout(self):
        """
        Test that a user can logout and that they will be redirected to
        the homepage
        """
        # User needs to log out
        self.driver.find_element_by_id("logout").click()

        # Asserts that the browser redirects to the login page
        assert 'http://127.0.0.1:5000/login' in self.driver.current_url

        # Login is necessary to not conflict with the tearDown function
        # Click login button on the nav bar
        self.driver.find_element_by_id("login").click()

        # Waits for the login elements to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
        except:
            self.driver.close()

        # Fill in the correct form
        self.driver.find_element_by_id("username").send_keys("Test")
        self.driver.find_element_by_id("password").send_keys("password")
        self.driver.find_element_by_id("login_button").click()

    def test_habit_creation(self):
        """
        Test that a user can create a habit
        Checks the create function for wrong inputs
        Also inspects if a list of habits is generated
        """
        # Click habits button on the nav bar
        self.driver.find_element_by_id("habits").click()

        # Waits for the habit creation elements to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "task"))
            )
        except:
            self.driver.close()

        # Fill in the false create habit form (No task inserted)
        self.driver.find_element_by_id("task").send_keys("")
        self.driver.find_element_by_id("periodicity").send_keys("1")
        self.driver.find_element_by_id("create").click()

        # Asserts error message is shown
        error_message = self.driver.find_element_by_class_name(
            "alert").text
        assert "The task field cannot be empty" in error_message

        # Asserts error message is closed
        self.driver.find_element_by_class_name("close").click()
        AssertionError(self.driver.find_element_by_class_name("alert"))

        # Fill in the false create habit form (No periodicity inserted)
        self.driver.find_element_by_id("task").send_keys("TestTask")
        self.driver.find_element_by_id("periodicity").send_keys("")
        self.driver.find_element_by_id("create").click()

        # Asserts error message is shown
        error_message = self.driver.find_element_by_class_name(
            "alert").text
        assert "The periodicity field cannot be empty" in error_message

        # Asserts error message is closed
        self.driver.find_element_by_class_name("close").click()
        AssertionError(self.driver.find_element_by_class_name("alert"))

        # Fill in the false create habit form (Periodicity must be a number)
        self.driver.find_element_by_id("task").send_keys("TestTask")
        self.driver.find_element_by_id("periodicity").send_keys("Task")
        self.driver.find_element_by_id("create").click()

        # Asserts error message is shown
        error_message = self.driver.find_element_by_class_name(
            "alert").text
        assert "The periodicity must a number" in error_message

        # Asserts error message is closed
        self.driver.find_element_by_class_name("close").click()
        AssertionError(self.driver.find_element_by_class_name("alert"))

        # Fill in the correct create habit form
        self.driver.find_element_by_id("task").send_keys("TestTask")
        self.driver.find_element_by_id("periodicity").send_keys("1")
        self.driver.find_element_by_id("create").click()

        # Asserts success message is shown
        success_message = self.driver.find_element_by_class_name(
            "alert").text
        assert "Habit created!" in success_message

        # Asserts success message is closed
        self.driver.find_element_by_class_name("close").click()
        AssertionError(self.driver.find_element_by_class_name("alert"))

        # Fill in the false create habit form (Habit already exists)
        self.driver.find_element_by_id("task").send_keys("TestTask")
        self.driver.find_element_by_id("periodicity").send_keys("1")
        self.driver.find_element_by_id("create").click()

        # Asserts error message is shown
        error_message = self.driver.find_element_by_class_name(
            "alert").text
        assert "The habit already exsists!" in error_message

        # Asserts error message is closed
        self.driver.find_element_by_class_name("close").click()
        AssertionError(self.driver.find_element_by_class_name("alert"))

    def test_habit_check(self):
        """
        Test that a user can check off habits
        """
        # Click habits button on the nav bar
        self.driver.find_element_by_id("habits").click()

        # Waits for the habit creation elements to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "task"))
            )
        except:
            self.driver.close()

        # Fill in the correct create habit form
        self.driver.find_element_by_id("task").send_keys("TestTask")
        self.driver.find_element_by_id("periodicity").send_keys("1")
        self.driver.find_element_by_id("create").click()

        # User needs to be logged out
        self.driver.find_element_by_id("logout").click()

        # Content of the Test.json file is loaded into user_json
        with open(f"Data/Test.json", "r") as file:
            user_json = json.loads(file.read())

        # The date of yesterday is created, to simulate a 1-day streak
        today = date.today()
        yesterday = today - timedelta(days=1)
        user_json['habit_data'][0]['last_checked'] = yesterday.strftime(
            "%d/%m/%Y")
        json_str = json.dumps(user_json, indent=4, sort_keys=False)

        # Content of the jsonStr is written into Test.json file
        with open(f"Data/Test.json", "w") as file:
            file.write(json_str)

        # Click login button on the nav bar
        self.driver.find_element_by_id("login").click()

        # Waits for the login elements to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
        except:
            self.driver.close()

        # Fill in the correct form
        self.driver.find_element_by_id("username").send_keys("Test")
        self.driver.find_element_by_id("password").send_keys("password")
        self.driver.find_element_by_id("login_button").click()

        # Click habits button on the nav bar
        self.driver.find_element_by_id("habits").click()

        # Waits for the habit list elements to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "check"))
            )
        except:
            self.driver.close()

        # Asserts the table has been generated
        table = self.driver.find_element_by_class_name("table").text
        assert "Task" in table

        # Asserts the "Check" button has been generated
        check = self.driver.find_element_by_id("check").text
        assert "Check" in check

        # Checks off the Task habit
        self.driver.find_element_by_id("check").click()

        # Asserts success message is shown with 1-day streak
        success_message = self.driver.find_element_by_class_name(
            "alert").text
        assert "1-day streak" in success_message

        # Asserts that the current streak is 1
        assert "1" in table

        # Asserts error message is closed
        self.driver.find_element_by_class_name("close").click()
        AssertionError(self.driver.find_element_by_class_name("alert"))

        # Checks the habit break
        # User needs to be logged out
        self.driver.find_element_by_id("logout").click()

        # Content of the Test.json file is loaded into user_json
        with open(f"Data/Test.json", "r") as file:
            user_json = json.loads(file.read())

        # The date of 2 days ago is created, to simulate a habit break
        today = date.today()
        two_days_ago = today - timedelta(days=2)
        user_json['habit_data'][0]['last_checked'] = two_days_ago.strftime(
            "%d/%m/%Y")
        json_str = json.dumps(user_json, indent=4, sort_keys=False)

        # Content of the jsonStr is written into Test.json file
        with open(f"Data/Test.json", "w") as file:
            file.write(json_str)

        # Click login button on the nav bar
        self.driver.find_element_by_id("login").click()

        # Waits for the login elements to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
        except:
            self.driver.close()

        # Fill in the correct form
        self.driver.find_element_by_id("username").send_keys("Test")
        self.driver.find_element_by_id("password").send_keys("password")
        self.driver.find_element_by_id("login_button").click()

        # Click habits button on the nav bar
        self.driver.find_element_by_id("habits").click()

        # Waits for the habit list elements to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "check"))
            )
        except:
            self.driver.close()

        # Checks off the Task habit
        self.driver.find_element_by_id("check").click()

        # Asserts error message is shown with habit break
        error_message = self.driver.find_element_by_class_name(
            "alert").text
        assert "Streak broken" in error_message

    def test_habit_deletion(self):
        """
        Test that a user can delete habits
        """
        # Click habits button on the nav bar
        self.driver.find_element_by_id("habits").click()

        # Waits for the habit creation elements to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "task"))
            )
        except:
            self.driver.close()

        # Fill in the correct create habit form
        self.driver.find_element_by_id("task").send_keys("TestTask")
        self.driver.find_element_by_id("periodicity").send_keys("1")
        self.driver.find_element_by_id("create").click()

        # Asserts the table has been generated
        table = self.driver.find_element_by_class_name("table").text
        assert "Task" in table

        # Asserts the "Delete" button has been generated
        delete = self.driver.find_element_by_id("delete").text
        assert "Delete" in delete

        # Click delete button in the list
        self.driver.find_element_by_id("delete").click()

        # Asserts that Task is not in table anymore
        AssertionError("TestTask" in table)

    def test_analytics_habits_same_periodicity(self):
        """
        Test that a user can view habits with the same periodicity
        """
        # Click habits button on the nav bar
        self.driver.find_element_by_id("habits").click()

        # Waits for the habit creation elements to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "task"))
            )
        except:
            self.driver.close()

        # Fill in the correct create habit form
        self.driver.find_element_by_id("task").send_keys("TestTask")
        self.driver.find_element_by_id("periodicity").send_keys("1")
        self.driver.find_element_by_id("create").click()

        # Click analytics button on the nav bar
        self.driver.find_element_by_id("analytics").click()

        # Waits for the analytics elements to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "periodicity"))
            )
        except:
            self.driver.close()

        # Search for the periodicity input form and inputs 1
        self.driver.find_element_by_id("periodicity").send_keys("1")

        # Confirm for the firm, with simulation of the RETURN key
        self.driver.find_element_by_id("periodicity").send_keys(Keys.RETURN)

        # Asserts the table has been generated
        table = self.driver.find_element_by_class_name("table").text
        assert "Task" in table

        # Asserts the task is in table
        table = self.driver.find_element_by_class_name("table").text
        assert "TestTask" in table

    def test_analytics_longest_run_streak(self):
        """
        Test that a user can view a list of longest run streaks
        """

        # Click habits button on the nav bar
        self.driver.find_element_by_id("habits").click()

        # Waits for the habit creation elements to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "task"))
            )
        except:
            self.driver.close()

        # Fill in the correct create habit form
        self.driver.find_element_by_id("task").send_keys("TestTask")
        self.driver.find_element_by_id("periodicity").send_keys("1")
        self.driver.find_element_by_id("create").click()

        # Click analytics button on the nav bar
        self.driver.find_element_by_id("analytics").click()

        # Asserts the table has been generated
        table = self.driver.find_element_by_class_name("table").text
        assert "Task" in table

        # Asserts the task is in table
        table = self.driver.find_element_by_class_name("table").text
        assert "TestTask" in table

        # Asserts the longest streak is 0
        table = self.driver.find_element_by_class_name("table").text
        assert "0" in table

    def test_analytics_longest_streak_of_task(self):
        """
        Test that a user can view the longest run streak of a given task
        """
        # Click habits button on the nav bar
        self.driver.find_element_by_id("habits").click()

        # Waits for the habit creation elements to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "task"))
            )
        except:
            self.driver.close()

        # Fill in the correct create habit form
        self.driver.find_element_by_id("task").send_keys("TestTask")
        self.driver.find_element_by_id("periodicity").send_keys("1")
        self.driver.find_element_by_id("create").click()

        # Click analytics button on the nav bar
        self.driver.find_element_by_id("analytics").click()

        # Search for the task input form and inputs "TestTask"
        self.driver.find_element_by_id("task").send_keys("TestTask")

        # Confirm for the firm, with simulation of the RETURN key
        self.driver.find_element_by_id("task").send_keys(Keys.RETURN)

        # Asserts the table has been generated
        table = self.driver.find_element_by_class_name("table").text
        assert "Task" in table

        # Asserts the task is in table
        table = self.driver.find_element_by_class_name("table").text
        assert "TestTask" in table

        # Asserts the longest streak is 0
        table = self.driver.find_element_by_class_name("table").text
        assert "0" in table


if __name__ == '__main__':
    unittest.main()
