from flask import Flask, request, jsonify, Blueprint, render_template
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import os
from datetime import datetime

# Flask app
app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY', 'fallback-secret')

# MongoDB connection
mongo_uri = os.getenv('MONGODB_URI')
if mongo_uri:
    client = MongoClient(mongo_uri)
    db = client['enejistats']
else:
    # Fallback for development
    client = MongoClient('mongodb://localhost:27017/')
    db = client['enejistats']

# Helper to convert ObjectId
def serialize_doc(doc):
    if doc and '_id' in doc:
        doc['_id'] = str(doc['_id'])
    return doc

# -------------------------------
# AUTH ROUTES
# -------------------------------
auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        required = ['username', 'email', 'password', 'role']
        if not all(field in data for field in required):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if db.users.find_one({'email': data['email']}):
            return jsonify({'error': 'User already exists'}), 400

        user = {
            'username': data['username'],
            'email': data['email'],
            'password': data['password'],  # Hash in production
            'role': data['role'],
            'created_at': datetime.now()
        }
        result = db.users.insert_one(user)
        return jsonify({'message': 'User registered', 'user_id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = db.users.find_one({'email': data.get('email'), 'password': data.get('password')})
        if user:
            return jsonify({
                'message': 'Login successful',
                'user': {
                    'id': str(user['_id']),
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role']
                }
            }), 200
        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': 'Login failed'}), 500

# -------------------------------
# PLAYER ROUTES
# -------------------------------
player_bp = Blueprint('player_bp', __name__)

@player_bp.route('', methods=['POST'])
def create_player():
    try:
        data = request.get_json()
        required = ['name', 'position', 'age', 'club', 'nationality']
        if not all(field in data for field in required):
            return jsonify({'error': 'Missing fields'}), 400

        data['created_at'] = datetime.now()
        result = db.players.insert_one(data)
        return jsonify({'message': 'Player created', 'player_id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': 'Failed to create player'}), 500

@player_bp.route('', methods=['GET'])
def get_players():
    try:
        players = list(db.players.find())
        return jsonify([serialize_doc(p) for p in players]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch players'}), 500

@player_bp.route('/<player_id>', methods=['GET'])
def get_player(player_id):
    try:
        if not ObjectId.is_valid(player_id):
            return jsonify({'error': 'Invalid player ID'}), 400
        
        player = db.players.find_one({'_id': ObjectId(player_id)})
        if player:
            return jsonify(serialize_doc(player)), 200
        return jsonify({'error': 'Player not found'}), 404
    except Exception as e:
        return jsonify({'error': 'Failed to fetch player'}), 500

@player_bp.route('/<player_id>', methods=['PUT'])
def update_player(player_id):
    try:
        if not ObjectId.is_valid(player_id):
            return jsonify({'error': 'Invalid player ID'}), 400
        
        data = request.get_json()
        result = db.players.update_one({'_id': ObjectId(player_id)}, {'$set': data})
        if result.modified_count:
            return jsonify({'message': 'Player updated'}), 200
        return jsonify({'error': 'Update failed'}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to update player'}), 500

@player_bp.route('/<player_id>', methods=['DELETE'])
def delete_player(player_id):
    try:
        if not ObjectId.is_valid(player_id):
            return jsonify({'error': 'Invalid player ID'}), 400
        
        result = db.players.delete_one({'_id': ObjectId(player_id)})
        if result.deleted_count:
            return jsonify({'message': 'Player deleted'}), 200
        return jsonify({'error': 'Player not found'}), 404
    except Exception as e:
        return jsonify({'error': 'Failed to delete player'}), 500

# -------------------------------
# SCOUT ROUTES
# -------------------------------
scout_bp = Blueprint('scout_bp', __name__)

@scout_bp.route('/reports', methods=['POST'])
def create_report():
    try:
        data = request.get_json()
        required = ['player_id', 'scout_name', 'rating', 'notes']
        if not all(field in data for field in required):
            return jsonify({'error': 'Missing fields'}), 400
        
        data['created_at'] = datetime.now()
        result = db.scout_reports.insert_one(data)
        return jsonify({'message': 'Report created', 'report_id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': 'Failed to create report'}), 500

@scout_bp.route('/reports', methods=['GET'])
def get_reports():
    try:
        reports = list(db.scout_reports.find())
        return jsonify([serialize_doc(r) for r in reports]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch reports'}), 500

@scout_bp.route('/reports/<player_id>', methods=['GET'])
def get_reports_by_player(player_id):
    try:
        reports = list(db.scout_reports.find({'player_id': player_id}))
        return jsonify([serialize_doc(r) for r in reports]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch player reports'}), 500

# -------------------------------
# CLUB ROUTES
# -------------------------------
club_bp = Blueprint('club_bp', __name__)

@club_bp.route('', methods=['POST'])
def create_club():
    try:
        data = request.get_json()
        required = ['name', 'league', 'coach', 'country', 'founded', 'stadium']
        if not all(field in data for field in required):
            return jsonify({'error': 'Missing fields'}), 400

        data['created_at'] = datetime.now()
        result = db.clubs.insert_one(data)
        return jsonify({'message': 'Club created', 'club_id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': 'Failed to create club'}), 500

@club_bp.route('', methods=['GET'])
def get_clubs():
    try:
        clubs = list(db.clubs.find())
        return jsonify([serialize_doc(c) for c in clubs]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch clubs'}), 500

@club_bp.route('/<club_id>', methods=['GET'])
def get_club(club_id):
    try:
        if not ObjectId.is_valid(club_id):
            return jsonify({'error': 'Invalid club ID'}), 400
        
        club = db.clubs.find_one({'_id': ObjectId(club_id)})
        if club:
            return jsonify(serialize_doc(club)), 200
        return jsonify({'error': 'Club not found'}), 404
    except Exception as e:
        return jsonify({'error': 'Failed to fetch club'}), 500

# -------------------------------
# MATCH ROUTES
# -------------------------------
match_bp = Blueprint('match_bp', __name__)

@match_bp.route('', methods=['POST'])
def create_match():
    try:
        data = request.get_json()
        required = ['home_team', 'away_team', 'date', 'status', 'venue']
        if not all(field in data for field in required):
            return jsonify({'error': 'Missing fields'}), 400

        data['created_at'] = datetime.now()
        result = db.matches.insert_one(data)
        return jsonify({'message': 'Match created', 'match_id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': 'Failed to create match'}), 500

@match_bp.route('', methods=['GET'])
def get_matches():
    try:
        matches = list(db.matches.find())
        return jsonify([serialize_doc(m) for m in matches]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch matches'}), 500

@match_bp.route('/<match_id>', methods=['GET'])
def get_match(match_id):
    try:
        if not ObjectId.is_valid(match_id):
            return jsonify({'error': 'Invalid match ID'}), 400
        
        match = db.matches.find_one({'_id': ObjectId(match_id)})
        if match:
            return jsonify(serialize_doc(match)), 200
        return jsonify({'error': 'Match not found'}), 404
    except Exception as e:
        return jsonify({'error': 'Failed to fetch match'}), 500

# -------------------------------
# Frontend Page
# -------------------------------
@app.route('/')
def index():
    return render_template('index.html')

# -------------------------------
# STATUS
# -------------------------------
@app.route('/api/status')
def status():
    try:
        return jsonify({
            'status': 'running',
            'users': db.users.count_documents({}),
            'players': db.players.count_documents({}),
            'clubs': db.clubs.count_documents({}),
            'matches': db.matches.count_documents({}),
            'reports': db.scout_reports.count_documents({})
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

# -------------------------------
# REGISTER BLUEPRINTS
# -------------------------------
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(player_bp, url_prefix='/api/players')
app.register_blueprint(club_bp, url_prefix='/api/clubs')
app.register_blueprint(match_bp, url_prefix='/api/matches')
app.register_blueprint(scout_bp, url_prefix='/api/scout')

# -------------------------------
# ERROR HANDLERS
# -------------------------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# -------------------------------
# APPLICATION ENTRY POINT
# -------------------------------
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
