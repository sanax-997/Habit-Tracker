# The globals.py file contains function, which initialized global variables

from .habits import Habit


def init_login_status():
    """Initializes the login status"""
    # login_status is initialized as global variable
    global login_status

    # login_status is set false, for the user to be "logged out" at the start of the program
    login_status = False


def init_habit():
    """Initalizes the habit object"""
    # Habit is initialized as global variable
    global habit

    # Habit initialized as object from the class Habit
    habit = Habit()
