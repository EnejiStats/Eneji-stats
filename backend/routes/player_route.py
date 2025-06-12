# routes/player_routes.py

from flask import Blueprint, request, jsonify
from bson import ObjectId
from models.db import players, users

player_bp = Blueprint('players', __name__)

@player_bp.route('/filter', methods=['POST'])
def filter_players():
    data = request.json or {}
    query = {}

    if data.get('age_min'):
        query['age'] = {'$gte': int(data['age_min'])}
    if data.get('age_max'):
        query.setdefault('age', {}).update({'$lte': int(data['age_max'])})
    if data.get('nationality'):
        query['nationality'] = {'$regex': data['nationality'], '$options': 'i'}
    if data.get('min_goals'):
        query['goals'] = {'$gte': int(data['min_goals'])}
    if data.get('min_pass_accuracy'):
        query['pass_accuracy'] = {'$gte': int(data['min_pass_accuracy'])}
    if data.get('min_interceptions'):
        query['interceptions'] = {'$gte': int(data['min_interceptions'])}
    if data.get('max_fouls'):
        query['fouls'] = {'$lte': int(data['max_fouls'])}

    result = players.find(query)
    output = []
    for p in result:
        output.append({
            '_id': str(p['_id']),
            'name': p.get('name'),
            'age': p.get('age'),
            'nationality': p.get('nationality')
        })
    return jsonify(output)


@player_bp.route('/compare')
def compare_players():
    ids = request.args.get('ids', '').split(',')
    ids = [ObjectId(i) for i in ids if ObjectId.is_valid(i)]
    result = players.find({'_id': {'$in': ids}})
    output = []
    for p in result:
        output.append({
            '_id': str(p['_id']),
            'name': p.get('name'),
            'goals': p.get('goals', 0),
            'pass_accuracy': p.get('pass_accuracy', 0),
            'interceptions': p.get('interceptions', 0),
            'fouls': p.get('fouls', 0)
        })
    return jsonify(output)
