from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Flask app config
app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY', 'fallback-secret')

# MongoDB setup
MONGO_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
client = MongoClient(MONGO_URI)
db = client['enejistats']

users = db['users']
players = db['players']
clubs = db['clubs']
matches = db['matches']
stats = db['stats']

# -------------------------------
# BLUEPRINT IMPORTS
# -------------------------------
from routes.auth_routes import auth_bp
from routes.player_routes import player_bp
from routes.scout_routes import scout_bp

# -------------------------------
# CLUB ROUTES
# -------------------------------
club_bp = Blueprint('club_bp', __name__)

@club_bp.route('', methods=['POST'])
def create_club():
    data = request.get_json()
    required = ['name', 'league', 'coach', 'country', 'founded', 'stadium']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing club fields'}), 400
    club = {
        'name': data['name'],
        'league': data['league'],
        'coach': data['coach'],
        'country': data['country'],
        'founded': int(data['founded']),
        'stadium': data['stadium']
    }
    clubs.insert_one(club)
    return jsonify({'message': 'Club created successfully'}), 201

@club_bp.route('', methods=['GET'])
def get_clubs():
    result = clubs.find()
    output = []
    for c in result:
        output.append({
            '_id': str(c['_id']),
            'name': c['name'],
            'league': c['league'],
            'coach': c['coach'],
            'country': c['country'],
            'founded': c['founded'],
            'stadium': c['stadium']
        })
    return jsonify(output), 200

# -------------------------------
# MATCH ROUTES
# -------------------------------
match_bp = Blueprint('match_bp', __name__)

@match_bp.route('', methods=['POST'])
def create_match():
    data = request.get_json()
    required = ['home_team', 'away_team', 'date', 'status', 'venue']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing match fields'}), 400
    match = {
        'home_team': data['home_team'],
        'away_team': data['away_team'],
        'date': data['date'],
        'status': data['status'],
        'score': data.get('score'),
        'venue': data['venue']
    }
    matches.insert_one(match)
    return jsonify({'message': 'Match created successfully'}), 201

@match_bp.route('', methods=['GET'])
def get_matches():
    result = matches.find()
    output = []
    for m in result:
        output.append({
            '_id': str(m['_id']),
            'home_team': m['home_team'],
            'away_team': m['away_team'],
            'date': m['date'],
            'status': m['status'],
            'score': m.get('score'),
            'venue': m['venue']
        })
    return jsonify(output), 200

# -------------------------------
# REGISTER ALL BLUEPRINTS
# -------------------------------
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(player_bp, url_prefix='/api/players')
app.register_blueprint(club_bp, url_prefix='/api/clubs')
app.register_blueprint(match_bp, url_prefix='/api/matches')
app.register_blueprint(scout_bp, url_prefix='/api/scout')

# -------------------------------
# RUN APP
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
