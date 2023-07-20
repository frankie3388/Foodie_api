from init import db, ma
from marshmallow import fields


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

class RestaurantSchema(ma.Schema):
    class Meta:
        fields = ('id', 'restaurant_name', 'address', 'cuisine', 'buffet', 'country', 'date')
        ordered = True


restaurant_schema = RestaurantSchema()
restaurants_schema = RestaurantSchema(many=True) 
