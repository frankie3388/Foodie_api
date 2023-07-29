from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf
from validation_data.valid_data import VALID_BUFFET, VALID_COUNTRIES, VALID_CUISINES

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text)
    cuisine = db.Column(db.String)
    buffet = db.Column(db.String)
    country = db.Column(db.String)
    date = db.Column(db.Date)

    favourite_restaurant = db.relationship('Favourite_restaurant', back_populates='restaurant', cascade='all, delete')
    comments_ratings = db.relationship('Comments_ratings', back_populates='restaurant', cascade='all, delete')

class RestaurantSchema(ma.Schema):
    comments_ratings = fields.List(fields.Nested('Comments_ratingSchema', exclude=['restaurant']))

    buffet = fields.String(validate=OneOf(VALID_BUFFET))
    country = fields.String(validate=OneOf(VALID_COUNTRIES))
    cuisine = fields.String(validate=OneOf(VALID_CUISINES))

    class Meta:
        fields = ('id', 'restaurant_name', 'address', 'cuisine', 'buffet', 'country', 'date', 'comments_ratings')
        ordered = True

restaurant_schema = RestaurantSchema()
restaurants_schema = RestaurantSchema(many=True) 
