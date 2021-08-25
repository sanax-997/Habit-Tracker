class Habit:
    list_of_habits = []

    def __init__(self, task, periodicity):
        self.task = task
        self.periodicity = periodicity
        self.list_of_habits.append(self.task)
        