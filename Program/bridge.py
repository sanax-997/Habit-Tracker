# Bridge.py is the main file of the Program

from HabitManagement import create_app

# Assigns app the return value from create_app
app = create_app()

# If this is the main file of the program the code is executed
if __name__ == "__main__":
    # Runs the webserver
    app.run()
