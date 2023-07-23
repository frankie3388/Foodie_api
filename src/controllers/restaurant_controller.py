from flask import Blueprint, request
from init import db
from models.restaurant import Restaurant, restaurant_schema, restaurants_schema
from controllers.comment_rating_controller import comments_ratings_bp

restaurant_bp = Blueprint('restaurant', __name__, url_prefix='/restaurant')
restaurant_bp.register_blueprint(comments_ratings_bp, url_prefix='/<int:restaurant_id>/comments_ratings')

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