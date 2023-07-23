from flask import Blueprint, request
from init import db
from models.favourites_list import Favourites_list
from models.favourite_restaurant import Favourite_restaurant, favourite_restaurant_schema, favourite_restaurants_schema
from models.restaurant import Restaurant
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
import functools

favourite_restaurant_bp = Blueprint('favourite_restaurants', __name__)

# This function can be used as a decorator for admin authourisation
# and user authorisation
def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        favourites_list_id = kwargs.get("favourites_list_id")
        fav_list_stmt = db.select(Favourites_list).filter_by(id=favourites_list_id)
        favourites_list = db.session.scalar(fav_list_stmt)
        if user.is_admin:
            return fn(*args, **kwargs)
        elif str(favourites_list.user_id) == get_jwt_identity():
            # This elif only lets users who have created the favourites list
            # delete their own favourite restaurant.
            return fn(*args, **kwargs)
        else:
            return {'error': 'Not authorised to perform delete'}, 403
    return wrapper


@favourite_restaurant_bp.route('/', methods=['POST'])
@jwt_required()
def create_favourite_restaurant(favourites_list_id):
    try:
        body_data = request.get_json()
        stmt = db.select(Favourites_list).filter_by(id=favourites_list_id)
        favourites_list = db.session.scalar(stmt)

        if favourites_list:
            if str(favourites_list.user_id) != get_jwt_identity():
                # This function does not let other users add a restaurant into
                # other user's favourites lists.
                return {"error": "Only the owner of the favourites list can add a restaurant to their favourites list"}, 403
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
@authorise_as_admin
def delete_favourite_restaurant(favourites_list_id, favourite_restaurants_id):
    fav_rest_stmt = db.select(Favourite_restaurant).filter_by(id=favourite_restaurants_id)
    favourite_restaurant = db.session.scalar(fav_rest_stmt)
    # fav_list_stmt = db.select(Favourites_list).filter_by(id=favourites_list_id)
    # favourites_list = db.session.scalar(fav_list_stmt)
    if favourite_restaurant:
        # if str(favourites_list.user_id) != get_jwt_identity():
        #         # This function does not let other users delete a restaurant from
        #         # other user's favourites lists.
        #         return {"error": "Only the owner of the favourites list can delete a restaurant from their favourites list"}, 403
        db.session.delete(favourite_restaurant)
        db.session.commit()
        return {'message': f'Favourite restaurant id {favourite_restaurant.id} deleted successfully'}
    else:
        return {'error': f'Favourite restaurant not found with id {favourite_restaurants_id}'}
    

