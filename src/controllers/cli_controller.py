from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.favourites_list import Favourites_list
from models.restaurant import Restaurant
from models.favourite_restaurant import Favourite_restaurant
from models.comments_ratings import Comments_ratings
from datetime import date

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_all():
    db.create_all()
    print("Tables created")


@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")


@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            name='admin',
            email='admin@admin.com',
            password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin=True
        ),
        User(
            name='User1',
            email='user1@email.com',
            password=bcrypt.generate_password_hash('user123').decode('utf-8')
        )
    ]

    db.session.add_all(users)
    

    restaurants = [
        Restaurant(
            restaurant_name='Sono Japanese Restaurant',
            address='39 Hercules St, Hamilton QLD 4007',
            cuisine='Japanese Food',
            buffet='No',
            country='Australia',
            date=date.today()
        ),
        Restaurant(
            restaurant_name='Rokkasen',
            address='Sun flower building F6・F7, 1-3-1, Nishishinjuku, Shinjiku-ku, Tokyo',
            cuisine='Japanese Food',
            buffet='Yes',
            country='Japan',
            date=date.today()
        ),
        Restaurant(
            restaurant_name='Yung Kee',
            address='32-40 Wellington Street, Central, Hong Kong',
            cuisine='Cantonese Food (BBQ meats)',
            buffet='No',
            country='China',
            date=date.today()
        ),
        Restaurant(
            restaurant_name='Ichiran',
            address='B1F, 1-22-7 Jinnan Shibuya-ku Tokyo-to',
            cuisine='Japanese',
            buffet='No',
            country='Japan',
            date=date.today()
        ),
    ]
    
    db.session.add_all(restaurants)

    favourites_lists = [
        Favourites_list(
            list_name='List 1',
            date_created=date.today(),
            user=users[0]
        ),
        Favourites_list(
            list_name='List 2',
            date_created=date.today(),
            user=users[1]
        ),
        Favourites_list(
            list_name='List 3',
            date_created=date.today(),
            user=users[1],
        ),
    ]
    
    db.session.add_all(favourites_lists)
    
    favourite_restaurants = [
        Favourite_restaurant(
            favourites_list=favourites_lists[0],
            restaurant=restaurants[0]
        ),
        Favourite_restaurant(
            favourites_list=favourites_lists[1],
            restaurant=restaurants[1]
        ),
        Favourite_restaurant(
            favourites_list=favourites_lists[1],
            restaurant=restaurants[2]
        ),
        Favourite_restaurant(
            favourites_list=favourites_lists[2],
            restaurant=restaurants[3]
        ),
    ]
    
    db.session.add_all(favourite_restaurants)

    comments_ratings = [
        Comments_ratings(
            message='Great Japanese food',
            food_rating=5,
            experience_rating=5,
            value_rating=4,
            date_created=date.today(),
            user=users[1],
            restaurant=restaurants[1]
        ),
        Comments_ratings(
            message='Best Japanese restaurant in Brisbane',
            food_rating=5,
            experience_rating=5,
            value_rating=4,
            date_created=date.today(),
            user=users[1],
            restaurant=restaurants[0]
        ),
    ]

    db.session.add_all(comments_ratings)
    db.session.commit()
    print("Tables seeded")

