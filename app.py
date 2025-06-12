from flask import Flask, request, jsonify, Blueprint, render_template
from flask_cors import CORS
import os
from datetime import datetime

# Flask app config
app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY', 'fallback-secret-key-for-dev')

# In-memory storage (replacing MongoDB)
data_store = {
    'users': [],
    'players': [],
    'clubs': [],
    'matches': [],
    'stats': [],
    'scouts': []
}

# Helper function to generate IDs
def generate_id():
    return str(len(data_store['users']) + len(data_store['players']) + 
              len(data_store['clubs']) + len(data_store['matches']) + 1000)

# -------------------------------
# AUTH ROUTES
# -------------------------------
auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required = ['username', 'email', 'password', 'role']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user exists
    for user in data_store['users']:
        if user['email'] == data['email']:
            return jsonify({'error': 'User already exists'}), 400
    
    user = {
        '_id': generate_id(),
        'username': data['username'],
        'email': data['email'],
        'password': data['password'],  # In production, hash this
        'role': data['role'],
        'created_at': datetime.now().isoformat()
    }
    data_store['users'].append(user)
    return jsonify({'message': 'User registered successfully', 'user_id': user['_id']}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    for user in data_store['users']:
        if user['email'] == email and user['password'] == password:
            return jsonify({
                'message': 'Login successful',
                'user': {
                    'id': user['_id'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role']
                }
            }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

# -------------------------------
# PLAYER ROUTES
# -------------------------------
player_bp = Blueprint('player_bp', __name__)

@player_bp.route('', methods=['POST'])
def create_player():
    data = request.get_json()
    required = ['name', 'position', 'age', 'club', 'nationality']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing player fields'}), 400
    
    player = {
        '_id': generate_id(),
        'name': data['name'],
        'position': data['position'],
        'age': int(data['age']),
        'club': data['club'],
        'nationality': data['nationality'],
        'market_value': data.get('market_value', 0),
        'goals': data.get('goals', 0),
        'assists': data.get('assists', 0),
        'created_at': datetime.now().isoformat()
    }
    data_store['players'].append(player)
    return jsonify({'message': 'Player created successfully', 'player_id': player['_id']}), 201

@player_bp.route('', methods=['GET'])
def get_players():
    return jsonify(data_store['players']), 200

@player_bp.route('/<player_id>', methods=['GET'])
def get_player(player_id):
    for player in data_store['players']:
        if player['_id'] == player_id:
            return jsonify(player), 200
    return jsonify({'error': 'Player not found'}), 404

@player_bp.route('/<player_id>', methods=['PUT'])
def update_player(player_id):
    data = request.get_json()
    for i, player in enumerate(data_store['players']):
        if player['_id'] == player_id:
            # Update player fields
            for key, value in data.items():
                if key != '_id':
                    player[key] = value
            player['updated_at'] = datetime.now().isoformat()
            return jsonify({'message': 'Player updated successfully'}), 200
    return jsonify({'error': 'Player not found'}), 404

# -------------------------------
# SCOUT ROUTES
# -------------------------------
scout_bp = Blueprint('scout_bp', __name__)

@scout_bp.route('/reports', methods=['POST'])
def create_scout_report():
    data = request.get_json()
    required = ['player_id', 'scout_name', 'rating', 'notes']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing scout report fields'}), 400
    
    report = {
        '_id': generate_id(),
        'player_id': data['player_id'],
        'scout_name': data['scout_name'],
        'rating': float(data['rating']),
        'notes': data['notes'],
        'technical_skills': data.get('technical_skills', 0),
        'physical_attributes': data.get('physical_attributes', 0),
        'mental_attributes': data.get('mental_attributes', 0),
        'recommendation': data.get('recommendation', 'Further evaluation needed'),
        'created_at': datetime.now().isoformat()
    }
    data_store['scouts'].append(report)
    return jsonify({'message': 'Scout report created successfully', 'report_id': report['_id']}), 201

@scout_bp.route('/reports', methods=['GET'])
def get_scout_reports():
    return jsonify(data_store['scouts']), 200

@scout_bp.route('/reports/<player_id>', methods=['GET'])
def get_player_scout_reports(player_id):
    reports = [report for report in data_store['scouts'] if report['player_id'] == player_id]
    return jsonify(reports), 200

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
        '_id': generate_id(),
        'name': data['name'],
        'league': data['league'],
        'coach': data['coach'],
        'country': data['country'],
        'founded': int(data['founded']),
        'stadium': data['stadium'],
        'created_at': datetime.now().isoformat()
    }
    data_store['clubs'].append(club)
    return jsonify({'message': 'Club created successfully', 'club_id': club['_id']}), 201

@club_bp.route('', methods=['GET'])
def get_clubs():
    return jsonify(data_store['clubs']), 200

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
        '_id': generate_id(),
        'home_team': data['home_team'],
        'away_team': data['away_team'],
        'date': data['date'],
        'status': data['status'],
        'score': data.get('score'),
        'venue': data['venue'],
        'created_at': datetime.now().isoformat()
    }
    data_store['matches'].append(match)
    return jsonify({'message': 'Match created successfully', 'match_id': match['_id']}), 201

@match_bp.route('', methods=['GET'])
def get_matches():
    return jsonify(data_store['matches']), 200

# -------------------------------
# FRONTEND ROUTE
# -------------------------------
@app.route('/')
def index():
    return render_template('index.html')

# -------------------------------
# API STATUS ROUTE
# -------------------------------
@app.route('/api/status')
def api_status():
    return jsonify({
        'status': 'running',
        'message': 'EnejiStats API is operational',
        'data_counts': {
            'users': len(data_store['users']),
            'players': len(data_store['players']),
            'clubs': len(data_store['clubs']),
            'matches': len(data_store['matches']),
            'scout_reports': len(data_store['scouts'])
        }
    }), 200

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
    app.run(debug=True, host='0.0.0.0', port=5000)
