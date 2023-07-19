from flask import Blueprint, request
from init import db
from models.favourites_list import Favourites_list, favourites_list_schema, favourites_lists_schema
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required

favourites_list_bp = Blueprint('favourites_list', __name__, url_prefix='/favourites_list')

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