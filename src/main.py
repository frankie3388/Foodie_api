from flask import Flask
import os
from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_commands
from controllers.auth_controller import auth_bp
from controllers.favourites_list_controller import favourites_list_bp
from controllers.restaurant_controller import restaurant_bp
from controllers.comment_rating_controller import comments_ratings_bp_2
from marshmallow.exceptions import ValidationError


def create_app():
    app = Flask(__name__)

    app.json.sort_keys = False

    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")

    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'error': err.messages}, 400

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(auth_bp)
    app.register_blueprint(favourites_list_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(comments_ratings_bp_2)

    return app