from flask import Blueprint, request
from init import db
from models.favourites_list import Favourites_list
from models.favourite_restaurant import Favourite_restaurant, favourite_restaurant_schema, favourite_restaurants_schema
from models.restaurant import Restaurant
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

favourite_restaurant_bp = Blueprint('favourite_restaurants', __name__)


@favourite_restaurant_bp.route('/', methods=['POST'])
@jwt_required()
def create_favourite_restaurant(favourites_list_id):
    try:
        body_data = request.get_json()
        stmt = db.select(Favourites_list).filter_by(id=favourites_list_id)
        favourites_list = db.session.scalar(stmt)
        if favourites_list:
            favourite_restaurant = Favourite_restaurant(
                favourites_list_id=favourites_list.id,
                restaurant_id=body_data.get('restaurant_id')
            )

            db.session.add(favourite_restaurant)
            db.session.commit()
            return favourite_restaurant_schema.dump(favourite_restaurant), 201
        else:
            return {'error': f'Favourites list not found with id {favourites_list_id}'}, 404
    except IntegrityError as err:
        body_data = request.get_json()
        restaurant_id=body_data.get('restaurant_id')
        if err.orig.pgcode == errorcodes.FOREIGN_KEY_VIOLATION:
            return {'error': f'Restaurant Id {restaurant_id} does not exist'}, 404
        

@favourite_restaurant_bp.route('/<int:favourite_restaurants_id>', methods=['DELETE'])
@jwt_required()
def delete_favourite_restaurant(favourites_list_id, favourite_restaurants_id):
    stmt = db.select(Favourite_restaurant).filter_by(id=favourite_restaurants_id)
    favourite_restaurant = db.session.scalar(stmt)
    if favourite_restaurant:
        db.session.delete(favourite_restaurant)
        db.session.commit()
        return {'message': f'Favourite restaurant id {favourite_restaurant.id} deleted successfully'}
    else:
        return {'error': f'Favourite restaurant not found with id {favourite_restaurants_id}'}
    

