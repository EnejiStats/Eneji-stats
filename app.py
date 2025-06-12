from flask import Flask, request, jsonify, Blueprint, render_template
from flask_cors import CORS
from flask import rfrom flask import Flask, request, jsonify, Blueprint, render_template
from flask_cors import CORS
from flask import render_template
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
client = MongoClient(mongo_uri)
db = client['enejistats']

# Helper to convert ObjectId
def serialize_doc(doc):
    doc['_id'] = str(doc['_id'])
    return doc

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

@auth_bp.route('/login', methods=['POST'])
def login():
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

# -------------------------------
# PLAYER ROUTES
# -------------------------------
player_bp = Blueprint('player_bp', __name__)

@player_bp.route('', methods=['POST'])
def create_player():
    data = request.get_json()
    required = ['name', 'position', 'age', 'club', 'nationality']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing fields'}), 400

    data['created_at'] = datetime.now()
    result = db.players.insert_one(data)
    return jsonify({'message': 'Player created', 'player_id': str(result.inserted_id)}), 201

@player_bp.route('', methods=['GET'])
def get_players():
    players = list(db.players.find())
    return jsonify([serialize_doc(p) for p in players]), 200

@player_bp.route('/<player_id>', methods=['GET'])
def get_player(player_id):
    player = db.players.find_one({'_id': ObjectId(player_id)})
    if player:
        return jsonify(serialize_doc(player)), 200
    return jsonify({'error': 'Player not found'}), 404

@player_bp.route('/<player_id>', methods=['PUT'])
def update_player(player_id):
    data = request.get_json()
    result = db.players.update_one({'_id': ObjectId(player_id)}, {'$set': data})
    if result.modified_count:
        return jsonify({'message': 'Player updated'}), 200
    return jsonify({'error': 'Update failed'}), 400

# -------------------------------
# SCOUT ROUTES
# -------------------------------
scout_bp = Blueprint('scout_bp', __name__)

@scout_bp.route('/reports', methods=['POST'])
def create_report():
    data = request.get_json()
    required = ['player_id', 'scout_name', 'rating', 'notes']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing fields'}), 400
    
    data['created_at'] = datetime.now()
    result = db.scout_reports.insert_one(data)
    return jsonify({'message': 'Report created', 'report_id': str(result.inserted_id)}), 201

@scout_bp.route('/reports', methods=['GET'])
def get_reports():
    reports = list(db.scout_reports.find())
    return jsonify([serialize_doc(r) for r in reports]), 200

@scout_bp.route('/reports/<player_id>', methods=['GET'])
def get_reports_by_player(player_id):
    reports = list(db.scout_reports.find({'player_id': player_id}))
    return jsonify([serialize_doc(r) for r in reports]), 200

# -------------------------------
# CLUB ROUTES
# -------------------------------
club_bp = Blueprint('club_bp', __name__)

@club_bp.route('', methods=['POST'])
def create_club():
    data = request.get_json()
    required = ['name', 'league', 'coach', 'country', 'founded', 'stadium']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing fields'}), 400

    data['created_at'] = datetime.now()
    result = db.clubs.insert_one(data)
    return jsonify({'message': 'Club created', 'club_id': str(result.inserted_id)}), 201

@club_bp.route('', methods=['GET'])
def get_clubs():
    clubs = list(db.clubs.find())
    return jsonify([serialize_doc(c) for c in clubs]), 200

# -------------------------------
# MATCH ROUTES
# -------------------------------
match_bp = Blueprint('match_bp', __name__)

@match_bp.route('', methods=['POST'])
def create_match():
    data = request.get_json()
    required = ['home_team', 'away_team', 'date', 'status', 'venue']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing fields'}), 400

    data['created_at'] = datetime.now()
    result = db.matches.insert_one(data)
    return jsonify({'message': 'Match created', 'match_id': str(result.inserted_id)}), 201

@match_bp.route('', methods=['GET'])
def get_matches():
    matches = list(db.matches.find())
    return jsonify([serialize_doc(m) for m in matches]), 200

# -------------------------------
# Frontend Page
# -------------------------------

@app.route('/')
def index():
    return render_from flask import Flask, request, jsonify, Blueprint, render_template
from flask_cors import CORS
from flask import render_template
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
client = MongoClient(mongo_uri)
db = client['enejistats']

# Helper to convert ObjectId
def serialize_doc(doc):
    doc['_id'] = str(doc['_id'])
    return doc

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

@auth_bp.route('/login', methods=['POST'])
def login():
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

# -------------------------------
# PLAYER ROUTES
# -------------------------------
player_bp = Blueprint('player_bp', __name__)

@player_bp.route('', methods=['POST'])
def create_player():
    data = request.get_json()
    required = ['name', 'position', 'age', 'club', 'nationality']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing fields'}), 400

    data['created_at'] = datetime.now()
    result = db.players.insert_one(data)
    return jsonify({'message': 'Player created', 'player_id': str(result.inserted_id)}), 201

@player_bp.route('', methods=['GET'])
def get_players():
    players = list(db.players.find())
    return jsonify([serialize_doc(p) for p in players]), 200

@player_bp.route('/<player_id>', methods=['GET'])
def get_player(player_id):
    player = db.players.find_one({'_id': ObjectId(player_id)})
    if player:
        return jsonify(serialize_doc(player)), 200
    return jsonify({'error': 'Player not found'}), 404

@player_bp.route('/<player_id>', methods=['PUT'])
def update_player(player_id):
    data = request.get_json()
    result = db.players.update_one({'_id': ObjectId(player_id)}, {'$set': data})
    if result.modified_count:
        return jsonify({'message': 'Player updated'}), 200
    return jsonify({'error': 'Update failed'}), 400

# -------------------------------
# SCOUT ROUTES
# -------------------------------
scout_bp = Blueprint('scout_bp', __name__)

@scout_bp.route('/reports', methods=['POST'])
def create_report():
    data = request.get_json()
    required = ['player_id', 'scout_name', 'rating', 'notes']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing fields'}), 400
    
    data['created_at'] = datetime.now()
    result = db.scout_reports.insert_one(data)
    return jsonify({'message': 'Report created', 'report_id': str(result.inserted_id)}), 201

@scout_bp.route('/reports', methods=['GET'])
def get_reports():
    reports = list(db.scout_reports.find())
    return jsonify([serialize_doc(r) for r in reports]), 200

@scout_bp.route('/reports/<player_id>', methods=['GET'])
def get_reports_by_player(player_id):
    reports = list(db.scout_reports.find({'player_id': player_id}))
    return jsonify([serialize_doc(r) for r in reports]), 200

# -------------------------------
# CLUB ROUTES
# -------------------------------
club_bp = Blueprint('club_bp', __name__)

@club_bp.route('', methods=['POST'])
def create_club():
    data = request.get_json()
    required = ['name', 'league', 'coach', 'country', 'founded', 'stadium']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing fields'}), 400

    data['created_at'] = datetime.now()
    result = db.clubs.insert_one(data)
    return jsonify({'message': 'Club created', 'club_id': str(result.inserted_id)}), 201

@club_bp.route('', methods=['GET'])
def get_clubs():
    clubs = list(db.clubs.find())
    return jsonify([serialize_doc(c) for c in clubs]), 200

# -------------------------------
# MATCH ROUTES
# -------------------------------
match_bp = Blueprint('match_bp', __name__)

@match_bp.route('', methods=['POST'])
def create_match():
    data = request.get_json()
    required = ['home_team', 'away_team', 'date', 'status', 'venue']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing fields'}), 400

    data['created_at'] = datetime.now()
    result = db.matches.insert_one(data)
    return jsonify({'message': 'Match created', 'match_id': str(result.inserted_id)}), 201

@match_bp.route('', methods=['GET'])
def get_matches():
    matches = list(db.matches.find())
    return jsonify([serialize_doc(m) for m in matches]), 200

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
    return jsonify({
        'status': 'running',
        'users': db.users.count_documents({}),
        'players': db.players.count_documents({}),
        'clubs': db.clubs.count_documents({}),
        'matches': db.matches.count_documents({}),
        'reports': db.scout_reports.count_documents({})
    }), 200

# -------------------------------
# REGISTER BLUEPRINTS
# -------------------------------
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(player_bp, url_prefix='/api/players')
app.register_blueprint(club_bp, url_prefix='/api/clubs')
app.register_blueprint(match_bp, url_prefix='/api/matches')
app.register_blueprint(scout_bp, url_prefix='/api/scout')
template('index.html')

# -------------------------------
# STATUS
# -------------------------------
@app.route('/api/status')
def status():
    return jsonify({
        'status': 'running',
        'users': db.users.count_documents({}),
        'players': db.players.count_documents({}),
        'clubs': db.clubs.count_documents({}),
        'matches': db.matches.count_documents({}),
        'reports': db.scout_reports.count_documents({})
    }), 200

# -------------------------------
# REGISTER BLUEPRINTS
# -------------------------------
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(player_bp, url_prefix='/api/players')
app.register_blueprint(club_bp, url_prefix='/api/clubs')
app.register_blueprint(match_bp, url_prefix='/api/matches')
app.register_blueprint(scout_bp, url_prefix='/api/scout')
ender_template
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
client = MongoClient(mongo_uri)
db = client['enejistats']

# Helper to convert ObjectId
def serialize_doc(doc):
    doc['_id'] = str(doc['_id'])
    return doc

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

@auth_bp.route('/login', methods=['POST'])
def login():
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

# -------------------------------
# PLAYER ROUTES
# -------------------------------
player_bp = Blueprint('player_bp', __name__)

@player_bp.route('', methods=['POST'])
def create_player():
    data = request.get_json()
    required = ['name', 'position', 'age', 'club', 'nationality']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing fields'}), 400

    data['created_at'] = datetime.now()
    result = db.players.insert_one(data)
    return jsonify({'message': 'Player created', 'player_id': str(result.inserted_id)}), 201

@player_bp.route('', methods=['GET'])
def get_players():
    players = list(db.players.find())
    return jsonify([serialize_doc(p) for p in players]), 200

@player_bp.route('/<player_id>', methods=['GET'])
def get_player(player_id):
    player = db.players.find_one({'_id': ObjectId(player_id)})
    if player:
        return jsonify(serialize_doc(player)), 200
    return jsonify({'error': 'Player not found'}), 404

@player_bp.route('/<player_id>', methods=['PUT'])
def update_player(player_id):
    data = request.get_json()
    result = db.players.update_one({'_id': ObjectId(player_id)}, {'$set': data})
    if result.modified_count:
        return jsonify({'message': 'Player updated'}), 200
    return jsonify({'error': 'Update failed'}), 400

# -------------------------------
# SCOUT ROUTES
# -------------------------------
scout_bp = Blueprint('scout_bp', __name__)

@scout_bp.route('/reports', methods=['POST'])
def create_report():
    data = request.get_json()
    required = ['player_id', 'scout_name', 'rating', 'notes']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing fields'}), 400
    
    data['created_at'] = datetime.now()
    result = db.scout_reports.insert_one(data)
    return jsonify({'message': 'Report created', 'report_id': str(result.inserted_id)}), 201

@scout_bp.route('/reports', methods=['GET'])
def get_reports():
    reports = list(db.scout_reports.find())
    return jsonify([serialize_doc(r) for r in reports]), 200

@scout_bp.route('/reports/<player_id>', methods=['GET'])
def get_reports_by_player(player_id):
    reports = list(db.scout_reports.find({'player_id': player_id}))
    return jsonify([serialize_doc(r) for r in reports]), 200

# -------------------------------
# CLUB ROUTES
# -------------------------------
club_bp = Blueprint('club_bp', __name__)

@club_bp.route('', methods=['POST'])
def create_club():
    data = request.get_json()
    required = ['name', 'league', 'coach', 'country', 'founded', 'stadium']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing fields'}), 400

    data['created_at'] = datetime.now()
    result = db.clubs.insert_one(data)
    return jsonify({'message': 'Club created', 'club_id': str(result.inserted_id)}), 201

@club_bp.route('', methods=['GET'])
def get_clubs():
    clubs = list(db.clubs.find())
    return jsonify([serialize_doc(c) for c in clubs]), 200

# -------------------------------
# MATCH ROUTES
# -------------------------------
match_bp = Blueprint('match_bp', __name__)

@match_bp.route('', methods=['POST'])
def create_match():
    data = request.get_json()
    required = ['home_team', 'away_team', 'date', 'status', 'venue']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing fields'}), 400

    data['created_at'] = datetime.now()
    result = db.matches.insert_one(data)
    return jsonify({'message': 'Match created', 'match_id': str(result.inserted_id)}), 201

@match_bp.route('', methods=['GET'])
def get_matches():
    matches = list(db.matches.find())
    return jsonify([serialize_doc(m) for m in matches]), 200

# -------------------------------
# Frontend Page
# -------------------------------

@app.route('/')
def index():
    return render_from flask import Flask, request, jsonify, Blueprint, render_template
from flask_cors import CORS
from flask import render_template
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
client = MongoClient(mongo_uri)
db = client['enejistats']

# Helper to convert ObjectId
def serialize_doc(doc):
    doc['_id'] = str(doc['_id'])
    return doc

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

@auth_bp.route('/login', methods=['POST'])
def login():
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

# -------------------------------
# PLAYER ROUTES
# -------------------------------
player_bp = Blueprint('player_bp', __name__)

@player_bp.route('', methods=['POST'])
def create_player():
    data = request.get_json()
    required = ['name', 'position', 'age', 'club', 'nationality']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing fields'}), 400

    data['created_at'] = datetime.now()
    result = db.players.insert_one(data)
    return jsonify({'message': 'Player created', 'player_id': str(result.inserted_id)}), 201

@player_bp.route('', methods=['GET'])
def get_players():
    players = list(db.players.find())
    return jsonify([serialize_doc(p) for p in players]), 200

@player_bp.route('/<player_id>', methods=['GET'])
def get_player(player_id):
    player = db.players.find_one({'_id': ObjectId(player_id)})
    if player:
        return jsonify(serialize_doc(player)), 200
    return jsonify({'error': 'Player not found'}), 404

@player_bp.route('/<player_id>', methods=['PUT'])
def update_player(player_id):
    data = request.get_json()
    result = db.players.update_one({'_id': ObjectId(player_id)}, {'$set': data})
    if result.modified_count:
        return jsonify({'message': 'Player updated'}), 200
    return jsonify({'error': 'Update failed'}), 400

# -------------------------------
# SCOUT ROUTES
# -------------------------------
scout_bp = Blueprint('scout_bp', __name__)

@scout_bp.route('/reports', methods=['POST'])
def create_report():
    data = request.get_json()
    required = ['player_id', 'scout_name', 'rating', 'notes']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing fields'}), 400
    
    data['created_at'] = datetime.now()
    result = db.scout_reports.insert_one(data)
    return jsonify({'message': 'Report created', 'report_id': str(result.inserted_id)}), 201

@scout_bp.route('/reports', methods=['GET'])
def get_reports():
    reports = list(db.scout_reports.find())
    return jsonify([serialize_doc(r) for r in reports]), 200

@scout_bp.route('/reports/<player_id>', methods=['GET'])
def get_reports_by_player(player_id):
    reports = list(db.scout_reports.find({'player_id': player_id}))
    return jsonify([serialize_doc(r) for r in reports]), 200

# -------------------------------
# CLUB ROUTES
# -------------------------------
club_bp = Blueprint('club_bp', __name__)

@club_bp.route('', methods=['POST'])
def create_club():
    data = request.get_json()
    required = ['name', 'league', 'coach', 'country', 'founded', 'stadium']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing fields'}), 400

    data['created_at'] = datetime.now()
    result = db.clubs.insert_one(data)
    return jsonify({'message': 'Club created', 'club_id': str(result.inserted_id)}), 201

@club_bp.route('', methods=['GET'])
def get_clubs():
    clubs = list(db.clubs.find())
    return jsonify([serialize_doc(c) for c in clubs]), 200

# -------------------------------
# MATCH ROUTES
# -------------------------------
match_bp = Blueprint('match_bp', __name__)

@match_bp.route('', methods=['POST'])
def create_match():
    data = request.get_json()
    required = ['home_team', 'away_team', 'date', 'status', 'venue']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing fields'}), 400

    data['created_at'] = datetime.now()
    result = db.matches.insert_one(data)
    return jsonify({'message': 'Match created', 'match_id': str(result.inserted_id)}), 201

@match_bp.route('', methods=['GET'])
def get_matches():
    matches = list(db.matches.find())
    return jsonify([serialize_doc(m) for m in matches]), 200

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
    return jsonify({
        'status': 'running',
        'users': db.users.count_documents({}),
        'players': db.players.count_documents({}),
        'clubs': db.clubs.count_documents({}),
        'matches': db.matches.count_documents({}),
        'reports': db.scout_reports.count_documents({})
    }), 200

# -------------------------------
# REGISTER BLUEPRINTS
# -------------------------------
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(player_bp, url_prefix='/api/players')
app.register_blueprint(club_bp, url_prefix='/api/clubs')
app.register_blueprint(match_bp, url_prefix='/api/matches')
app.register_blueprint(scout_bp, url_prefix='/api/scout')
template('index.html')
