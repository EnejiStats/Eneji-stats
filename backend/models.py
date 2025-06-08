# File: backend/models.py
from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # CTO, Admin, Scout

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))
    stats = db.relationship('PlayerStat', backref='player', lazy=True)

class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    players = db.relationship('Player', backref='club', lazy=True)
    stats = db.relationship('ClubStat', backref='club', lazy=True)

class PlayerStat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    match_date = db.Column(db.DateTime, default=datetime.utcnow)
    short_pass_s = db.Column(db.Integer, default=0)
    short_pass_u = db.Column(db.Integer, default=0)
    long_pass_s = db.Column(db.Integer, default=0)
    long_pass_u = db.Column(db.Integer, default=0)
    dribbles_s = db.Column(db.Integer, default=0)
    dribbles_u = db.Column(db.Integer, default=0)
    shots_ot = db.Column(db.Integer, default=0)
    shots_oft = db.Column(db.Integer, default=0)
    clearance = db.Column(db.Integer, default=0)
    aerial_duel_w = db.Column(db.Integer, default=0)
    aerial_duel_l = db.Column(db.Integer, default=0)
    fouls_f = db.Column(db.Integer, default=0)
    fouls_a = db.Column(db.Integer, default=0)
    yellow_card = db.Column(db.Integer, default=0)
    red_card = db.Column(db.Integer, default=0)
    gk_saves = db.Column(db.Integer, default=0)

class ClubStat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))
    match_date = db.Column(db.DateTime, default=datetime.utcnow)
    possession = db.Column(db.Float, default=0.0)
    corner_kicks = db.Column(db.Integer, default=0)
    shots_ot = db.Column(db.Integer, default=0)
    shots_oft = db.Column(db.Integer, default=0)
    gk_saves = db.Column(db.Integer, default=0)
    yellow_card = db.Column(db.Integer, default=0)
    red_card = db.Column(db.Integer, default=0)
    fouls = db.Column(db.Integer, default=0)
    goals = db.Column(db.Integer, default=0)
