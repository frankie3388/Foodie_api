from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.restaurant import Restaurant
from models.comments_ratings import Comments_ratings, comments_rating_schema
from datetime import date


comments_ratings_bp = Blueprint('comments_ratings', __name__)


@comments_ratings_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment_rating(restaurant_id):
    body_data = comments_rating_schema.load(request.get_json())
    stmt = db.select(Restaurant).filter_by(id=restaurant_id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        comments_ratings = Comments_ratings(
            message=body_data.get('message'),
            food_rating=body_data.get('food_rating'),
            experience_rating=body_data.get('experience_rating'),
            value_rating=body_data.get('value_rating'),
            date_created=date.today(),
            user_id=get_jwt_identity(),
            restaurant_id=restaurant.id
        )

        db.session.add(comments_ratings)
        db.session.commit()
        return comments_rating_schema.dump(comments_ratings), 201
    else:
        return {'error': f'Restaurant not found with id {restaurant_id}'}, 404
    

@comments_ratings_bp.route('/<int:comments_ratings_id>', methods=['DELETE'])
@jwt_required()
def delete_comment_rating(restaurant_id, comments_ratings_id):
    stmt = db.select(Comments_ratings).filter_by(id=comments_ratings_id)
    comments_ratings = db.session.scalar(stmt)
    if comments_ratings:
        db.session.delete(comments_ratings)
        db.session.commit()
        return {'message': f'Comment id {comments_ratings.id} deleted successfully'}
    else:
        return {'error': f'Comment not found with id {comments_ratings.id}'}, 404
    

@comments_ratings_bp.route('/<int:comments_ratings_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment_rating(restaurant_id, comments_ratings_id):
    body_data = request.get_json()
    stmt = db.select(Comments_ratings).filter_by(id=comments_ratings_id)
    comments_ratings = db.session.scalar(stmt)
    if comments_ratings:
        comments_ratings.message = body_data.get('message') or comments_ratings.message
        comments_ratings.food_rating = body_data.get('food_rating') or comments_ratings.food_rating
        comments_ratings.experience_rating = body_data.get('experience_rating') or comments_ratings.experience_rating
        comments_ratings.value_rating = body_data.get('value_rating') or comments_ratings.value_rating
        db.session.commit()
        return comments_rating_schema.dump(comments_ratings)
    else:
        return {'error': f'Comment not found with id {comments_ratings.id}'}, 404