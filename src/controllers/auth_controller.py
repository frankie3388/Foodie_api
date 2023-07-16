from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, user_schema, users_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# This route lets users register
@auth_bp.route('/register', methods=['POST'])
def auth_register():
    try:
        body_data = request.get_json()

        # Create a new User model instance from the user info
        user = User()
        user.name = body_data.get('name')
        user.email = body_data.get('email')
        user.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
        # Add the user to the session
        db.session.add(user)
        # Commit to add the user to the database
        db.session.commit()
        # Respond to the client
        return user_schema.dump(user), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return { 'error': 'Email address already in use' }, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return { 'error': f'The {err.orig.diag.column_name} is required' }, 409