from init import db, ma 
from marshmallow import fields
from marshmallow.validate import OneOf
from validation_data.valid_data import VALID_RATINGS


class Comments_ratings(db.Model):
    __tablename__ = 'comments_ratings'

    id = db.Column(db.Integer, primary_key=True)

    message = db.Column(db.Text)
    food_rating = db.Column(db.Integer)
    experience_rating = db.Column(db.Integer)
    value_rating = db.Column(db.Integer)
    date_created = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    user = db.relationship('User', back_populates='comments_ratings')
    restaurant = db.relationship('Restaurant', back_populates='comments_ratings')


class Comments_ratingSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    restaurant = fields.Nested('RestaurantSchema', exclude=['comments_ratings'])

    food_rating = fields.Integer(validate=OneOf(VALID_RATINGS))
    experience_rating = fields.Integer(validate=OneOf(VALID_RATINGS))
    value_rating = fields.Integer(validate=OneOf(VALID_RATINGS))

    class Meta:
        fields = (
            'id', 'message', 'food_rating', 
            'experience_rating', 'value_rating', 'date_created', 
            'user', 'restaurant'
            )
        ordered = True

comments_rating_schema = Comments_ratingSchema()
comments_ratings_schema = Comments_ratingSchema(many=True)