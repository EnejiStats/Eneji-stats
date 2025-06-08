# File: backend/app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Import and register blueprints
from routes.players import players_bp
from routes.clubs import clubs_bp
from routes.stats import stats_bp
from routes.widget import widget_bp
from auth import auth_bp

app.register_blueprint(players_bp, url_prefix='/players')
app.register_blueprint(clubs_bp, url_prefix='/clubs')
app.register_blueprint(stats_bp, url_prefix='/stats')
app.register_blueprint(widget_bp, url_prefix='/widget')
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
