from flask import Flask
from backend.routes.auth_routes import auth_bp
from backend.routes.player_routes import player_bp
from backend.routes.club_routes import club_bp
from backend.routes.stats_routes import stats_bp
from backend.models import db
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "defaultsecret")

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///backend/database/enejistats.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(player_bp)
    app.register_blueprint(club_bp)
    app.register_blueprint(stats_bp)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
