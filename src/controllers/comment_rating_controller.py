from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.restaurant import Restaurant
from models.user import User
from models.comments_ratings import Comments_ratings, comments_rating_schema, comments_ratings_schema
from validation_data.valid_data import VALID_RATINGS
from datetime import date
import functools

comments_ratings_bp = Blueprint('comments_ratings', __name__)
comments_ratings_bp_2 = Blueprint('comments_ratings', __name__, url_prefix='/comments_ratings')


# This function can be used as a decorator for admin authourisation
# and user authorisation
def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        comments_ratings_id = kwargs.get("comments_ratings_id")
        comments_stmt = db.select(Comments_ratings).filter_by(id=comments_ratings_id)
        comments_ratings = db.session.scalar(comments_stmt)
        if user.is_admin:
            return fn(*args, **kwargs)
        elif str(comments_ratings.user_id) == get_jwt_identity():
            # This elif only lets users who have created the favourites list
            # delete or update their own favourites list.
            return fn(*args, **kwargs)
        else:
            return {'error': 'Not authorised to perform delete'}, 403
    return wrapper

# This route gets all comments by food rating (example - food rating of 5 gets all comments_ratings records with food rating of 5).
# The returned response is a JSON object that has fields of ('id', 'message', 'food_rating', 'experience_rating', 'value_rating', 'date_created', 'user', 'restaurant').
# The Comments_ratingSchema is setup to display what user created what comment on what restaurant.
@comments_ratings_bp_2.route('/food_rating/<int:food_rating>')
def get_comments_ratings_by_food_rating(food_rating):
    if food_rating not in VALID_RATINGS:
        return {'error': f'Food rating must be one of: {VALID_RATINGS}'}, 400
    stmt = db.select(Comments_ratings).filter_by(food_rating=food_rating)
    result = db.session.execute(stmt)
    comments_ratings = result.scalars().all()
    if not comments_ratings:
        return {'error': f'Restaurant not found with food rating {food_rating}'}, 404
    return comments_ratings_schema.dump(comments_ratings)

# This route gets all comments by experience rating (example - experience rating of 5 gets all comments_ratings records with experience rating of 5).
# The returned response is a JSON object that has fields of ('id', 'message', 'food_rating', 'experience_rating', 'value_rating', 'date_created', 'user', 'restaurant').
# The Comments_ratingSchema is setup to display what user created what comment on what restaurant.
@comments_ratings_bp_2.route('/experience_rating/<int:experience_rating>')
def get_comments_ratings_by_experience_rating(experience_rating):
    if experience_rating not in VALID_RATINGS:
        return {'error': f'Experience rating must be one of: {VALID_RATINGS}'}, 400
    stmt = db.select(Comments_ratings).filter_by(experience_rating=experience_rating)
    result = db.session.execute(stmt)
    comments_ratings = result.scalars().all()
    if not comments_ratings:
        return {'error': f'Restaurant not found with experience rating {experience_rating}'}, 404
    return comments_ratings_schema.dump(comments_ratings)

# This route gets all comments by value rating (example - value rating of 5 gets all comments_ratings records with value rating of 5).
# The returned response is a JSON object that has fields of ('id', 'message', 'food_rating', 'experience_rating', 'value_rating', 'date_created', 'user', 'restaurant').
# The Comments_ratingSchema is setup to display what user created what comment on what restaurant.
@comments_ratings_bp_2.route('/value_rating/<int:value_rating>')
def get_comments_ratings_by_value_rating(value_rating):
    if value_rating not in VALID_RATINGS:
        return {'error': f'Value rating must be one of: {VALID_RATINGS}'}, 400
    stmt = db.select(Comments_ratings).filter_by(value_rating=value_rating)
    result = db.session.execute(stmt)
    comments_ratings = result.scalars().all()
    if not comments_ratings:
        return {'error': f'Restaurant not found with value rating {value_rating}'}, 404
    return comments_ratings_schema.dump(comments_ratings)

# This route creates a comments_ratings record in the database.
# Only a logged in user can create a comment.
# The restaurant id is used to find the restaurant to comment on.
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
    
# This route deletes a comment_ratings record by comments_ratings_id.
# Only the user who created the comment_ratings record and admin can delete the record.
@comments_ratings_bp.route('/<int:comments_ratings_id>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_comment_rating(restaurant_id, comments_ratings_id):
    stmt = db.select(Comments_ratings).filter_by(id=comments_ratings_id)
    comments_ratings = db.session.scalar(stmt)
    if comments_ratings:
        db.session.delete(comments_ratings)
        db.session.commit()
        return {'message': f'Comment id {comments_ratings.id} deleted successfully'}
    else:
        return {'error': f'Comment not found with id {comments_ratings.id}'}, 404
    
# This route updates a comments_ratings record by comments_ratings_id.
# Only the user who created the comment_ratings record and admin can update the record.
@comments_ratings_bp.route('/<int:comments_ratings_id>', methods=['PUT', 'PATCH'])
@jwt_required()
@authorise_as_admin
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