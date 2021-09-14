# The habits.py file contains all the functionality of the Habit class

from flask import json, flash
from datetime import datetime


class Habit:
    # The Habit class is initialized
    def __init__(self):
        """Called at the instantiation of a habit object"""
        # The data structure of habit follows the same as the .json file
        self.user_data = []
        self.habit_data = []
        self.login_status = False

    def load_data(self, username):
        """Loads all data from the .json file into the habit object"""
        # The context manager opens the .json file based on the username
        # The content of the .json file is stored in user_json
        with open(f"Data/{username}.json", "r") as file:
            user_json = json.loads(file.read())

        # Loads the user data from the .json file and overwrites the user data of the habit object
        self.user_data = user_json['user_data']

        # Loads the habit data from the .json file and overwrites the habit data of the habit object
        self.habit_data = user_json['habit_data']

        # Sets the login status to True, this means the user is "logged in"
        self.login_status = True

    def save_data(self):
        """Takes all the data stored in the habit object and "dumps" it as .json file"""
        # The username stored in the habit object is stored in "username"
        username = self.user_data[0]['username']

        # The user data and habit data from the habit object are stored in user_json
        user_json = {"user_data": self.user_data,
                     "habit_data": self.habit_data}

        # The data from user_json is then formatted with json.dumps and stored in jsonStr
        jsonStr = json.dumps(user_json, indent=4, sort_keys=False)

        # The content of jsonStr is written to the .json file based on the username
        with open(f"Data/{username}.json", "w") as file:
            file.write(jsonStr)

    def create_habit(self, *args):
        """Creates a new habit based on the arguments passed into the function"""
        # Appends the arguments to the list of the habit object
        self.habit_data.append(*args)

    def delete_habit(self, task):
        """Deletes a chosen habit"""
        # All the dictionaries stored in habit data are iterated through
        # Stored in index is the index of the dictionary and the dictionary itself
        # Checks if the task in the dictionary is the same as the task passed into the function
        # Removes the element from the list based on the index
        for index, dic in enumerate(self.habit_data):
            if dic['task'] == task:
                self.habit_data.pop(index)

    def check_habit(self, task):
        """Checks off a habit"""
        # All the dictionaries stored in habit data are iterated through
        # Stored in index is the index of the dictionary and the dictionary itself
        # Checks if the task in the dictionary is the same as the task passed into the function
        for index, dic in enumerate(self.habit_data):
            if dic['task'] == task:
                # Sets the today variable as todays date
                today = datetime.today()

                # Sets the periodicity as the periodicity from the habit
                periodicity = self.habit_data[index]['periodicity']

                # Takes the last checked string from the habit and converts it into a date object
                last_checked = datetime.strptime(
                    self.habit_data[index]['last_checked'], '%d/%m/%Y')

                # Stores the day difference between today and last checked
                day_difference = today - last_checked

                # If the day difference is greater than the periodicty the habit was not fullfilled in a given time
                # The habit streak has been broken
                if day_difference.days > int(periodicity):
                    # The streak score is set to 0
                    self.habit_data[index]['streak'] = 0

                    # This flashes a message to the user that the message has been broken
                    flash('Streak broken', category="error")

                # If the day difference is less than the periodicty the habit has been fullfilled in a given time
                # The habit streak continues
                else:
                    # If it has been at least one day since the habit was last checked, the day-streak increases
                    if day_difference.days > 0:
                        self.habit_data[index]['streak'] += 1

                    # If the habit streak is greater than 0 a message is flashed, which shows the habit streak
                    if self.habit_data[index]['streak'] != 0:
                        days = self.habit_data[index]['streak']
                        flash(f'{days}-day streak', category="success")

                # If the streak of a given habit is greater than its longest streak, the longest streak is overwritten with the current streak
                if self.habit_data[index]['streak'] > self.habit_data[index]['longest_streak']:
                    self.habit_data[index]['longest_streak'] = self.habit_data[index]['streak']

                # The last checked date changes to today
                self.habit_data[index]['last_checked'] = today.strftime(
                    "%d/%m/%Y")
