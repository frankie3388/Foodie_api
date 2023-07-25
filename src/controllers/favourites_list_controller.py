from flask import Blueprint, request
from init import db
from models.favourites_list import Favourites_list, favourites_list_schema, favourites_lists_schema
from models.user import User
from controllers.favourite_restaurant_controller import favourite_restaurant_bp
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required
import functools

favourites_list_bp = Blueprint('favourites_list', __name__, url_prefix='/favourites_list')
favourites_list_bp.register_blueprint(favourite_restaurant_bp, url_prefix='/<int:favourites_list_id>/favourite_restaurants')


# This function can be used as a decorator for admin authourisation
# and user authorisation
def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        favourites_list_id = kwargs.get("id")
        fav_list_stmt = db.select(Favourites_list).filter_by(id=favourites_list_id)
        favourites_list = db.session.scalar(fav_list_stmt)
        if user.is_admin:
            return fn(*args, **kwargs)
        elif str(favourites_list.user_id) == get_jwt_identity():
            # This elif only lets users who have created the favourites list
            # delete or update their own favourites list.
            return fn(*args, **kwargs)
        else:
            return {'error': 'Not authorised to perform delete or update'}, 403
    return wrapper


# This route gets all favourites lists
@favourites_list_bp.route('/')
def get_all_favourites_lists():
    stmt = db.select(Favourites_list).order_by(Favourites_list.date_created.desc())
    favourites_lists = db.session.scalars(stmt)
    return favourites_lists_schema.dump(favourites_lists)

# This route gets individual favourites list by entering id
@favourites_list_bp.route('/<int:id>')
def get_one_favourites_list(id):
    stmt = db.select(Favourites_list).filter_by(id=id)
    favourites_list = db.session.scalar(stmt)
    if favourites_list:
        return favourites_list_schema.dump(favourites_list)
    else:
        return {'error': f'Favourites List not found with id {id}'}, 404

# This route lets the client create a favourites list
@favourites_list_bp.route('/', methods=['POST'])
@jwt_required()
def create_favourites_list():
    body_data = request.get_json()
    favourites_list = Favourites_list(
        list_name=body_data.get('list_name'),
        date_created=date.today(),
        user_id=get_jwt_identity()
    )
    # Add that favourites list to session
    db.session.add(favourites_list)
    # Commit
    db.session.commit()
    return favourites_list_schema.dump(favourites_list), 201

# This route lets the client delete a favourites list
@favourites_list_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_favourites_list(id):
    stmt = db.select(Favourites_list).filter_by(id=id)
    favourites_list = db.session.scalar(stmt)
    if favourites_list:
        db.session.delete(favourites_list)
        db.session.commit()
        return {'message': f'Favourites list {favourites_list.list_name} deleted successfully'}
    else:
        return {'error': f'Favourites list not found with id {id}'}, 404
    
# This route lets the client update the favourites list
@favourites_list_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@authorise_as_admin
def update_favourites_list(id):
    body_data = request.get_json()
    stmt = db.select(Favourites_list).filter_by(id=id)
    favourites_list = db.session.scalar(stmt)
    if favourites_list:
        favourites_list.list_name = body_data.get('list_name') or favourites_list.list_name
        db.session.commit()
        return favourites_list_schema.dump(favourites_list)
    else:
        return {'error': f'Favourites list not found with id {id}'}, 404