
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from routes.auth_routes import auth_bp
from routes.player_routes import player_bp
from routes.club_routes import club_bp
from routes.scout_routes import scout_bp

load_dotenv()

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(player_bp, url_prefix='/api/players')
app.register_blueprint(club_bp, url_prefix='/api/clubs')
app.register_blueprint(scout_bp, url_prefix='/api/scout')

if __name__ == '__main__':
    app.run(debug=True)
