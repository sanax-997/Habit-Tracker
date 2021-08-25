#A blueprint is an object that allows defining application functions without requiring an application object ahead of time.
from flask import Blueprint, render_template, request, flash, json
from .habits import Habit
from HabitManagement import settings

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", login_status = settings.login_status)

@views.route('/analytics')
def analytics():
    return render_template("analytics.html", login_status = settings.login_status)

@views.route('/habits', methods=['GET', 'POST'])
def habits():
    if request.method == 'POST':
        task = request.form.get('task')
        periodicity = request.form.get('periodicity')

        user=settings.current_user
        with open(f"Data/{user}.json", "r") as file:
             user_json = json.loads(file.read())

        if len(task) < 1:
            flash('The task field cannot be empty', category="error")
        elif len(periodicity) < 1:
            flash('The periodicity field cannot be empty', category="error")
        elif not(periodicity.isnumeric()):
            flash('The periodicity must a number', category="error")
        elif any(habit_data['task']==task for habit_data in user_json['habit_data']):
            flash('The habit already exsists!', category="error")
        else:
            new_habit = Habit(task, periodicity)
            
            habit_data = {"task" : task, "periodicity": periodicity}
            user_json['habit_data'].append(habit_data)
            jsonStr = json.dumps(user_json, indent = 4 ,sort_keys = False)

            with open(f"Data/{user}.json", "w") as file:
                file.write(jsonStr)       

            flash('Habit created!', category="success")
            for i in Habit.list_of_habits:
                print(i)
        
    return render_template("habits.html", login_status = settings.login_status, boolean=True)