from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Vo@f!11pFP*mOEGO^@wCwXxDs2NAU^P*@FgOKm33i!w@U1YLaqeE!p#5$9wGVKlG1sgTj7C8l1r$yxH!osZRhzOmgzb@uA*2F1m'

    return app