# routes/scout_routes.py

from flask import Blueprint, jsonify
from models.db import users

scout_bp = Blueprint('scout', __name__)

@scout_bp.route('/me', methods=['GET'])
def get_scout_profile():
    # In real app, use session auth
    # Here we fetch a mock scout (first one found)
    scout = users.find_one({'role': 'scout'})  # or use current_user if authenticated
    if not scout:
        return jsonify({'error': 'Scout not found'}), 404

    return jsonify({
        'name': scout.get('name', 'Unnamed'),
        'region': scout.get('region', 'Not specified'),
        'photo': scout.get('photo', '')
    })
