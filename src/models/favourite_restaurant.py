from init import db, ma
from marshmallow import fields


class Favourite_restaurant(db.Model):
    __tablename__ = 'favourite_restaurants'

    id = db.Column(db.Integer, primary_key=True)

    favourites_list_id = db.Column(db.Integer, db.ForeignKey('favourites_list.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    favourites_list = db.relationship('Favourites_list', back_populates='favourite_restaurant')
    restaurant = db.relationship('Restaurant', back_populates='favourite_restaurant')


class Favourite_restaurantSchema(ma.Schema):
    favourites_list = fields.Nested('Favourites_listSchema', only=['list_name', 'user'])
    restaurant = fields.Nested('RestaurantSchema')

    class Meta:
        fields = ('id', 'favourites_list', 'restaurant')
        ordered = True
    
favourite_restaurant_schema = Favourite_restaurantSchema()
favourite_restaurants_schema = Favourite_restaurantSchema(many=True)