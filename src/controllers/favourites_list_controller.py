from flask import Blueprint, request
from init import db
from models.favourites_list import Favourites_list, favourites_list_schema, favourites_lists_schema

favourites_list_bp = Blueprint('favourites_list', __name__, url_prefix='/favourites_list')

@favourites_list_bp.route('/')
def get_all_favourites_lists():
    stmt = db.select(Favourites_list).order_by(Favourites_list.date_created.desc())
    favourites_lists = db.session.scalars(stmt)
    return favourites_lists_schema.dump(favourites_lists)