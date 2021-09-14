# The analytics.py module contains all the functions to analyze the habits

from HabitManagement import globals as g


def same_periodicity(periodicity):
    """Shows all habits, which have the same periodicity"""
    # Returns a list of dictionaries, which contain all dicts of a chosen periodicity
    return [dic for dic in (g.habit.habit_data) if dic['periodicity'] == periodicity]


def longest_streak_all():
    """Shows the habits with the longest streak from all habits"""

    def search_max():
        """Searches for the dictionary with the longest streak"""
        # It returns the highest, longest streak integer of all dictionaries
        return max([dic[key] for dic in (g.habit.habit_data) for key in dic if key == "longest_streak"])

    # search_dict
    def search_dict(search_max):
        """Searches for the dictionary index based on the longest streak"""
        # It returns the index of the dictionary
        return [index for index, dic in enumerate(g.habit.habit_data) if dic['longest_streak'] == search_max]

    # Returns the wanted dictionary
    return return_dict(search_dict(search_max()))


def longest_streak_task(task):
    """Shows the longest streak of a given habit"""

    def search_dict(task):
        """Searches for the dictionary index based on a task"""
        # It returns the index of the dictionary
        return [index for index, dic in enumerate(g.habit.habit_data) if dic['task'] == task]

    # Returns the wanted dictionary
    return return_dict(search_dict(task))


def return_dict(search_dict):
    """Returns a dictionary based on the index"""
    # Returns the wanted dictionary
    return [g.habit.habit_data[index] for index in search_dict]
