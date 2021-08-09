from HabitManagement import create_app
from HabitManagement import habits as h
from HabitManagement import analytics as a

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
