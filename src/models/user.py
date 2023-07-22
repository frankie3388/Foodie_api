from init import db, ma
from marshmallow import fields


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    favourites_list = db.relationship('Favourites_list', back_populates='user', cascade='all, delete')
    comments_ratings = db.relationship('Comments_ratings', back_populates='user')

class UserSchema(ma.Schema):
    favourites_lists = fields.List(fields.Nested('Favourites_listSchema', exclude=['user']))

    class Meta:
        fields = ('id', 'name', 'email', 'password', 'is_admin', 'favourites_lists')

user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])