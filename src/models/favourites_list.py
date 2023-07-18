from init import db, ma 
from marshmallow import fields


class Favourites_list(db.Model):
    __tablename__="favourites_list"

    id = db.Column(db.Integer, primary_key=True)
    list_name = db.Column(db.String(100))
    date_created = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship('User', back_populates='favourites_list')


class Favourites_listSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])

    class Meta:
        fields = ('id', 'list_name', 'date_created', 'user')
        ordered = True

favourites_list_schema = Favourites_listSchema()
favourites_lists_schema = Favourites_listSchema(many=True)
