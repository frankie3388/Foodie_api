from flask import Blueprint, request
from init import db
from models.restaurant import Restaurant, restaurant_schema, restaurants_schema
from models.user import User
from controllers.comment_rating_controller import comments_ratings_bp
from flask_jwt_extended import get_jwt_identity, jwt_required
from validation_data.valid_data import VALID_BUFFET, VALID_COUNTRIES, VALID_CUISINES
import functools
from datetime import date

restaurant_bp = Blueprint('restaurant', __name__, url_prefix='/restaurant')
restaurant_bp.register_blueprint(comments_ratings_bp, url_prefix='/<int:restaurant_id>/comments_ratings')

def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user.is_admin:
            return fn(*args, **kwargs)
        else:
            return {'error': 'Not authorised to create, delete, or update a restaurant'}, 403
    return wrapper


# This route gets all restaurants
@restaurant_bp.route('/')
def get_all_restaurants():
    stmt = db.select(Restaurant).order_by(Restaurant.restaurant_name.asc())
    restaurant = db.session.scalars(stmt)
    return restaurants_schema.dump(restaurant)

# This route gets individual restaurants
@restaurant_bp.route('/<int:id>')
def get_one_restaurant(id):
    stmt = db.select(Restaurant).filter_by(id=id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        return restaurant_schema.dump(restaurant)
    else:
        return {'error': f'Restaurant not found with id {id}'}, 404

# This route gets the restaurants by restaurant name
@restaurant_bp.route('/restaurant_name/<string:restaurant_name>')
def get_restaurant_by_name(restaurant_name):
    stmt = db.select(Restaurant).filter_by(restaurant_name=restaurant_name)
    result = db.session.execute(stmt)
    restaurants = result.scalars().all()
    if not restaurants:
        return {'error': f'Restaurant not found with name {restaurant_name}'}, 404
    return restaurants_schema.dump(restaurants)

# This route gets the restaurants by country
@restaurant_bp.route('/country/<string:country>')
def get_restaurant_by_country(country):
    if country not in VALID_COUNTRIES:
        return {'error': f'Country must be one of: {VALID_COUNTRIES}'}, 400
    stmt = db.select(Restaurant).filter_by(country=country)
    result = db.session.execute(stmt)
    restaurants = result.scalars().all()
    if not restaurants:
        return {'error': f'Restaurant not found in {country}'}, 404
    return restaurants_schema.dump(restaurants)

# This route gets the restaurants by buffet
@restaurant_bp.route('/buffet/<string:buffet>')
def get_restaurant_by_buffet(buffet):
    if buffet not in VALID_BUFFET:
        return {'error': f'Buffet must be one of: {VALID_BUFFET}'}, 400
    stmt = db.select(Restaurant).filter_by(buffet=buffet)
    result = db.session.execute(stmt)
    restaurants = result.scalars().all()
    if not restaurants:
        return {'error': f'There are no Restaurants with buffet {buffet}'}, 404
    return restaurants_schema.dump(restaurants)
    
# This route gets the restaurants by cuisine
@restaurant_bp.route('/cuisine/<string:cuisine>')
def get_restaurant_by_cuisine(cuisine):
    if cuisine not in VALID_CUISINES:
        return {'error': f'Cuisine must be one of: {VALID_CUISINES}'}, 400
    stmt = db.select(Restaurant).filter_by(cuisine=cuisine)
    result = db.session.execute(stmt)
    restaurants = result.scalars().all()
    if not restaurants:
        return {'error': f'There are no Restaurants with cuisine {cuisine}'}, 404
    return restaurants_schema.dump(restaurants)

@restaurant_bp.route('/', methods=['POST'])
@jwt_required()
@authorise_as_admin
def create_restaurant():
    body_data = restaurant_schema.load(request.get_json())
    restaurant = Restaurant(
        restaurant_name=body_data.get('restaurant_name'),
        address=body_data.get('address'),
        cuisine=body_data.get('cuisine'),
        buffet=body_data.get('buffet'),
        country=body_data.get('country'),
        date=date.today()
    )
    db.session.add(restaurant)
    db.session.commit()
    return restaurant_schema.dump(restaurant), 201


@restaurant_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_restaurant(id):
    stmt = db.select(Restaurant).filter_by(id=id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return {'message': f'Restaurant {restaurant.id} deleted successfully'}
    else:
        return {'error': f'Restaurant not found with id {id}'}, 404


@restaurant_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@authorise_as_admin
def update_restaurant(id):
    body_data = restaurant_schema.load(request.get_json())
    stmt = db.select(Restaurant).filter_by(id=id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        restaurant.restaurant_name = body_data.get('restaurant_name') or restaurant.restaurant_name
        restaurant.address = body_data.get('address') or restaurant.address
        restaurant.cuisine = body_data.get('cuisine') or restaurant.cuisine
        restaurant.buffet = body_data.get('buffet') or restaurant.buffet
        restaurant.country = body_data.get('country') or restaurant.country
        db.session.commit()
        return restaurant_schema.dump(restaurant)
    else:
        return {'error': f'Restaurant not found with id {id}'}, 404