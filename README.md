# Link to [Trello board](https://trello.com/b/rJpJ4X81/foodie-api)  
# Link to [Github](https://github.com/frankie3388/Foodie_api)

# R1/R2 Identification of the problem you are trying to solve by building this particular app. Why is it a problem that needs solving?  
The purpose of this application is to provide a platform for users to find information about a restaurant such as food reviews from other users, cuisine, address, etc.. Users will be able to find restaurants based on the ratings given to them from other users. It lets the user create a favourites list which they can add any restaurant they like to their list. It is an application that is made for foodies.  
As this application lets users create favourites lists with which they can add any restaurants they like to the list, it acts as a travel guide for foodies. For example, users can create a favourites list of restaurants for each country they want to visit. They can also review the restaurant that they have visited to help other like minded foodies. Users will be able to view the favourites lists of other users which can help them decide if they should visit the restaurant.  
Only users that have admin authorisation can add restaurants to the database. This reduces the amount of invalid information about the restaurant. Users can also filter restaurants by country, cuisine and if it has buffets. This gives the user more options when searching for specific restaurants to try. There are also, three types of ratings that the user can filter by, these are food rating, experience rating and value rating. Food rating is based on the taste and appearance of the food, experience rating is based on the service, setting and any unique experience that the restaurant offers, and lastly, value is based on if the restaurant offers value for money. These ratings can be scored from 0 to 5, where 0 is the worst and 5 is the best rating.  
In summary, this application makes it easier for foodies to find restaurants they want to try based on users reviews/ratings. It also acts as a travel planner as it lets the user save restaurants to a favourites list.

# R3 Why have you chosen this database system. What are the drawbacks compared to others?  
The database used for this application is PostgreSQL. PostgreSQL is an open source object-relational database management system (Ellingwood). There are numerous reason as to why PostgreSQL was used to store data for this application, these are:-  
* PostgreSQL is compatible with Python.  
* PostgreSQL has relational database features, this means that data is stored in tables consisting of rows and columns, where each table is an entity (IBM). Data can be related to each other through the use of primary keys and foreign keys from each entity/table (IBM). These features help with normalisation of data, which helps reduce redundancy or duplicated data. Since data is stored in tables and tables are linked to each other through primary keys and foreign keys, we can search for data using specific SQL queries. For example, if we want to search for the favourites lists of 'user_id 2' in the 'favourites_list' table of the application, we just use the SQL syntax 'select * from favourites_list where user_id=2'. In this case the 'user' table is linked to the 'favourites list' table through placing the primary key (id) from the 'user' table as the foreign key (user_id) column in the 'favourites_list' table.  
* PostgreSQL has object-oriented database features, which allows you to define your own complex data types (Ellingwood). An example of this is the 'comments_ratings' table in the application database, where different fields or attributes are stored in the table, such as 'message', 'food_rating', 'experience_rating', 'value_rating', 'date_created', 'user_id', and 'restaurant_id'. The 'message' attribute is a 'Text' datatype, the 'ratings' are a 'Integer' datatype, the 'date_create' is a 'date' datatype, and the foreign keys are 'Integer' datatypes.  
* It is ACID compliant (IBM). ACID is an acronym for Atomicity, Consistency, Isolation, and Durability, which essentially ensures that data transactions carried out in the database are conducted in a way to avoid validity errors and to maintain data integrity (Ellingwood). This feature is important for this application as I want the application to display valid information, especially when adding, deleting or updating restaurant information in the database.  
* PostgreSQL also maintains data integrity through using constraints when storing data into a table. This ensures that the correct data type is entered into the tables.  
* PostgreSQL has advanced security features like data encryption, SSL certificates, and authentication methods (Google Cloud 2007). This was a feature that allowed certain users have access to create, delete or update certain records in the database. For example, I need the admin user to have access to all features of the application, but normal users could only create, delete, or update their own records.  
* There is a large open source community that is actively working on updates and solutions to improve PostgreSQL (Google Cloud 2007).
If there is something wrong with the application's code that is related to PostgreSQL, there is most likely a solution online that can help
solve it, due to how widely used it is. 

Some of the drawbacks compared to other database management systems are:-
* Slower performance when compared to other relational database management systems such as SQL Server and MySQL (Google Cloud
2007).  
* It focuses on compatibility rather than speed (Google Cloud 2007).  
* Not beginner friendly in terms of installation (Google Cloud 2007).


# R4 Identify and discuss the key functionalities and benefits of an ORM  
ORM is an acronym for Object Relational Mapping, which is a Python tool or library like SQLAlchemy that serves as a bridge between an application's object-oriented code and a relational database (Hoyos 2018). By using an ORM, in this case SQLAlchemy, we can use object-oriented programming using the python language to create, read, update, and delete data in the postgreSQL database. ORMs like SQLAlchemy simplifies the process of interacting with the database by allowing developers to work with Python objects directly, thus removing the need to write raw SQL queries (Hoyos 2018). The key functionalities of SQLAlchemy are:-  
* SQLAlchemy provides an object-oriented approach to working with databases. Developers can define database models as python classes, where each class represents a table in the database, and each instance of the class represents a row in that table (Python Tutorial 2021). The code below is an example of the python class 'Restaurant' which defines a table called restaurants so that it can be deployed to the postgreSQL database. Attributes are defined in the model/table which make up the columns of the table. Constraints for each attribute are defined to ensure data integrity.
```python
db = SQLAlchemy(app)
class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text)
    cuisine = db.Column(db.String)
    buffet = db.Column(db.String)
    country = db.Column(db.String)
    date = db.Column(db.Date)
```  
*   One of the key functionalities of SQLAlchemy is the ability create, read, update and delete records in the database using OOP. The syntax of creating a record in the database is shown below, this is from the application:-  
```python
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
```
* This block of code creates a comment record in the 'comments_ratings' table of the database. It can be seen that a new 'Comments_ratings' object/model with the desired attributes are created then added to the session with the add method(). The code 'db.session.commit()' saves the record to the database. This is all part of SQLAlchemy which uses object-oriented programming to interact with the database. Retrieving a record from the database using SQLAlchemy is as easy as writing 'db.select(model name)', updating and deleting records also uses simple OOP queries.  
* SQLAlchemy supports defining relationships between different database tables using object-oriented relationships like one-to-one, one-to-many, and many-to-many. This simplifies the navigation and retrieval of related data.

Benefits of ORM (SQLAlchemy) inlclude:-  
* SQLAlchemy abstracts the differences between different database engines, allowing developers to write database-agnostic code. This enables easy switching between different database systems without changing the application's logic (vegibit).  
* SQLAlchemy offers a powerful and expressive query API that allows developers to build complex database queries using Python code (vegibit).  


# R5 Document all endpoints for your API  
### Endpoint - /auth/register  
* Description - Registers a new user to the database
* HTTP request verb - POST  
* Required data (JSON) -  
```
{
	"name": "User2",
	"email": "user2@email.com",
	"password": "password1"
}
```  
* Response data example- 
```
{
	"id": 3,
	"name": "User2",
	"email": "user2@email.com",
	"is_admin": false
}
```  
* Authentication methods - None.  

### Endpoint - /auth/login  
* Description - Registered users can login
* HTTP request verb - POST  
* Required data (JSON) -  
```
{
	"email": "user1@email.com",
	"password": "user123"
}
```  
* Response data - 
```
{
	"email": "user1@email.com",
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5MDQ3MTkxNSwianRpIjoiMWRkZjVhNDItY2FlMi00OWRkLThmODQtMmU5MGE0ZjUxZmUxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE2OTA0NzE5MTUsImV4cCI6MTY5MDU1ODMxNX0.YmUU-lSbSblt1uhEHEs7vSk9GlqZ9TU1cGSY0yhMRCs",
	"is_admin": false
}
```  
* Authentication methods - Email and password.  

### Endpoint - /favourites_list  
* Description - A GET request to the database retrieves all favourites lists
* HTTP request verb - GET  
* Required data (JSON) -  None
* Response data example- 
```
[
	{
		"id": 1,
		"list_name": "List 1",
		"date_created": "2023-07-28",
		"user": {
			"name": "admin",
			"email": "admin@admin.com"
		},
		"favourite_restaurant": [
			{
				"id": 1,
				"restaurant": {
					"id": 1,
					"restaurant_name": "Sono Japanese Restaurant",
					"address": "39 Hercules St, Hamilton QLD 4007",
					"cuisine": "Japanese",
					"buffet": "no",
					"country": "Australia",
					"date": "2023-07-28"
				}
			}
		]
	},
	{
		"id": 2,
		"list_name": "List 2",
		"date_created": "2023-07-28",
		"user": {
			"name": "User1",
			"email": "user1@email.com"
		},
		"favourite_restaurant": [
			{
				"id": 2,
				"restaurant": {
					"id": 2,
					"restaurant_name": "Rokkasen",
					"address": "Sun flower building F6・F7, 1-3-1, Nishishinjuku, Shinjiku-ku, Tokyo",
					"cuisine": "Japanese",
					"buffet": "yes",
					"country": "Japan",
					"date": "2023-07-28"
				}
			},
			{
				"id": 3,
				"restaurant": {
					"id": 3,
					"restaurant_name": "Yung Kee",
					"address": "32-40 Wellington Street, Central, Hong Kong",
					"cuisine": "Chinese",
					"buffet": "no",
					"country": "China",
					"date": "2023-07-28"
				}
			}
		]
	},
	{
		"id": 3,
		"list_name": "List 3",
		"date_created": "2023-07-28",
		"user": {
			"name": "User1",
			"email": "user1@email.com"
		},
		"favourite_restaurant": [
			{
				"id": 4,
				"restaurant": {
					"id": 4,
					"restaurant_name": "Ichiran",
					"address": "B1F, 1-22-7 Jinnan Shibuya-ku Tokyo-to",
					"cuisine": "Japanese",
					"buffet": "no",
					"country": "Japan",
					"date": "2023-07-28"
				}
			}
		]
	}
]
```  
* Authentication methods - None.  

### Endpoint - /favourites_list/<int:id>  
* Description - A GET request to the database retrieves a specific favourites list by id
* HTTP request verb - GET  
* Required data -  Id from the favourites_list table is required to be entered in the URL (int:id) - example URL:'localhost:8080/favourites_list/2'
* Response data example- 
```
{
	"id": 2,
	"list_name": "List 2",
	"date_created": "2023-07-28",
	"user": {
		"name": "User1",
		"email": "user1@email.com"
	},
	"favourite_restaurant": [
		{
			"id": 2,
			"restaurant": {
				"id": 2,
				"restaurant_name": "Rokkasen",
				"address": "Sun flower building F6・F7, 1-3-1, Nishishinjuku, Shinjiku-ku, Tokyo",
				"cuisine": "Japanese",
				"buffet": "yes",
				"country": "Japan",
				"date": "2023-07-28"
			}
		},
		{
			"id": 3,
			"restaurant": {
				"id": 3,
				"restaurant_name": "Yung Kee",
				"address": "32-40 Wellington Street, Central, Hong Kong",
				"cuisine": "Chinese",
				"buffet": "no",
				"country": "China",
				"date": "2023-07-28"
			}
		}
	]
}
```  
* Authentication methods - None.  

### Endpoint - /favourites_list/user_id/<int:user_id>  
* Description - A GET request to the database retrieves a specific favourites list by user id.
* HTTP request verb - GET  
* Required data -  User id from the favourites_list table is required to be entered in the URL (int:user_id) - example URL:'localhost:8080/favourites_list/user_id/2'
* Response data example- 
```
[
	{
		"id": 2,
		"list_name": "List 2",
		"date_created": "2023-07-28",
		"user": {
			"name": "User1",
			"email": "user1@email.com"
		},
		"favourite_restaurant": [
			{
				"id": 2,
				"restaurant": {
					"id": 2,
					"restaurant_name": "Rokkasen",
					"address": "Sun flower building F6・F7, 1-3-1, Nishishinjuku, Shinjiku-ku, Tokyo",
					"cuisine": "Japanese",
					"buffet": "yes",
					"country": "Japan",
					"date": "2023-07-28"
				}
			},
			{
				"id": 3,
				"restaurant": {
					"id": 3,
					"restaurant_name": "Yung Kee",
					"address": "32-40 Wellington Street, Central, Hong Kong",
					"cuisine": "Chinese",
					"buffet": "no",
					"country": "China",
					"date": "2023-07-28"
				}
			}
		]
	},
	{
		"id": 3,
		"list_name": "List 3",
		"date_created": "2023-07-28",
		"user": {
			"name": "User1",
			"email": "user1@email.com"
		},
		"favourite_restaurant": [
			{
				"id": 4,
				"restaurant": {
					"id": 4,
					"restaurant_name": "Ichiran",
					"address": "B1F, 1-22-7 Jinnan Shibuya-ku Tokyo-to",
					"cuisine": "Japanese",
					"buffet": "no",
					"country": "Japan",
					"date": "2023-07-28"
				}
			}
		]
	}
]
```  
* Authentication methods - None.  

### Endpoint - /favourites_list  
* Description - This route creates a favourites list in the database
* HTTP request verb - POST  
* Required data (JSON) -  
```
{
	"list_name": "list 4"
}
```
* Response data example- 
```
{
	"id": 4,
	"list_name": "list 4",
	"date_created": "2023-07-28",
	"user": {
		"name": "User1",
		"email": "user1@email.com"
	},
	"favourite_restaurant": []
}
```  
* Authentication methods - Bearer Token.  
* Authourisation - Registered user with a token.  

### Endpoint - /favourites_list/<int:id>  
* Description - This route deletes a specific favourites list in the database by filtering with id.
* HTTP request verb - DELETE  
* Required data -  Favourites list id from the favourites_list table is required to be entered in the URL (int:id) - example URL:'localhost:8080/favourites_list/4'
* Response data example- 
```
{
	"message": "Favourites list list 4 deleted successfully"
}
```  
* Authentication methods - Bearer Token.  
* Authourisation - Only the user that created the favourites list and admin user can delete a favourites list.  

### Endpoint - /favourites_list/<int:id>  
* Description - This route updates a specific favourites list in the database by filtering with id.
* HTTP request verb - PUT, PATCH  
* Required data (JSON) -  Favourites list id from the favourites_list table is required to be entered in the URL (int:id) - example URL:'localhost:8080/favourites_list/4'. Also you can update the favourites list name by entering the list name in JSON format in the request body.
```
{
	"list_name": "list 4 updated"
}
```
* Response data example- 
```
{
	"id": 4,
	"list_name": "list 4 updated",
	"date_created": "2023-07-28",
	"user": {
		"name": "User1",
		"email": "user1@email.com"
	},
	"favourite_restaurant": []
}
```  
* Authentication methods - Bearer Token.  
* Authourisation - Only the user that created the favourites list and admin user can update a favourites list.  

### Endpoint - /restaurant 
* Description - This route retrieves all restaurants in the database
* HTTP request verb - GET 
* Required data (JSON) -  None
* Response data example- 
```
[
	{
		"id": 4,
		"restaurant_name": "Ichiran",
		"address": "B1F, 1-22-7 Jinnan Shibuya-ku Tokyo-to",
		"cuisine": "Japanese",
		"buffet": "no",
		"country": "Japan",
		"date": "2023-07-28",
		"comments_ratings": []
	},
	{
		"id": 2,
		"restaurant_name": "Rokkasen",
		"address": "Sun flower building F6・F7, 1-3-1, Nishishinjuku, Shinjiku-ku, Tokyo",
		"cuisine": "Japanese",
		"buffet": "yes",
		"country": "Japan",
		"date": "2023-07-28",
		"comments_ratings": [
			{
				"id": 1,
				"message": "Great Japanese food",
				"food_rating": 5,
				"experience_rating": 5,
				"value_rating": 4,
				"date_created": "2023-07-28",
				"user": {
					"name": "User1",
					"email": "user1@email.com"
				}
			}
		]
	},
]
```  
* Authentication methods - None
* Authourisation - None  

### Endpoint - /restaurant/<int:id>
* Description - This route retrieves a specific restaurant by id in the database
* HTTP request verb - GET 
* Required data -  Restaurant id from the restaurant table is required to be entered in the URL (int:id) - example URL:'localhost:8080/restaurant/3'.
* Response data example- 
```
{
	"id": 3,
	"restaurant_name": "Yung Kee",
	"address": "32-40 Wellington Street, Central, Hong Kong",
	"cuisine": "Chinese",
	"buffet": "no",
	"country": "China",
	"date": "2023-07-28",
	"comments_ratings": []
}
```  
* Authentication methods - None
* Authourisation - None  

### Endpoint - /restaurant/restaurant_name/<string:restaurant_name>
* Description - This route retrieves a specific restaurant by restaurant name in the database
* HTTP request verb - GET 
* Required data -  Restaurant name from the restaurant table is required to be entered in the URL (string:restaurant_name) - example URL:'localhost:8080/restaurant/restaurant_name/Rokkasen'.
* Response data example- 
```
[
	{
		"id": 2,
		"restaurant_name": "Rokkasen",
		"address": "Sun flower building F6・F7, 1-3-1, Nishishinjuku, Shinjiku-ku, Tokyo",
		"cuisine": "Japanese",
		"buffet": "yes",
		"country": "Japan",
		"date": "2023-07-28",
		"comments_ratings": [
			{
				"id": 1,
				"message": "Great Japanese food",
				"food_rating": 5,
				"experience_rating": 5,
				"value_rating": 4,
				"date_created": "2023-07-28",
				"user": {
					"name": "User1",
					"email": "user1@email.com"
				}
			}
		]
	}
]
```  
* Authentication methods - None
* Authourisation - None  

### Endpoint - /restaurant/country/<string:country>
* Description - This route retrieves specific restaurants by country in the database
* HTTP request verb - GET 
* Required data -  Country from the restaurant table is required to be entered in the URL (string:country) - example URL:'localhost:8080/restaurant/country/Japan'.
* Response data example- 
```
[
	{
		"id": 2,
		"restaurant_name": "Rokkasen",
		"address": "Sun flower building F6・F7, 1-3-1, Nishishinjuku, Shinjiku-ku, Tokyo",
		"cuisine": "Japanese",
		"buffet": "yes",
		"country": "Japan",
		"date": "2023-07-26",
		"comments_ratings": [
			{
				"id": 1,
				"message": "Great Japanese food",
				"food_rating": 5,
				"experience_rating": 5,
				"value_rating": 4,
				"date_created": "2023-07-26",
				"user": {
					"name": "User1",
					"email": "user1@email.com"
				}
			}
		]
	},
	{
		"id": 4,
		"restaurant_name": "Ichiran",
		"address": "B1F, 1-22-7 Jinnan Shibuya-ku Tokyo-to",
		"cuisine": "Japanese",
		"buffet": "no",
		"country": "Japan",
		"date": "2023-07-26",
		"comments_ratings": []
	}
]
```  
* Authentication methods - None
* Authourisation - None  

### Endpoint - /restaurant/buffet/<string:buffet>
* Description - This route retrieves specific restaurants by if they have buffet in the database
* HTTP request verb - GET 
* Required data -  Buffet (yes or no) from the restaurant table is required to be entered in the URL (string:buffet) - example URL:'localhost:8080/restaurant/buffet/yes'.
* Response data example- 
```
[
	{
		"id": 2,
		"restaurant_name": "Rokkasen",
		"address": "Sun flower building F6・F7, 1-3-1, Nishishinjuku, Shinjiku-ku, Tokyo",
		"cuisine": "Japanese",
		"buffet": "yes",
		"country": "Japan",
		"date": "2023-07-28",
		"comments_ratings": [
			{
				"id": 1,
				"message": "Great Japanese food",
				"food_rating": 5,
				"experience_rating": 5,
				"value_rating": 4,
				"date_created": "2023-07-28",
				"user": {
					"name": "User1",
					"email": "user1@email.com"
				}
			}
		]
	}
]
```  
* Authentication methods - None
* Authourisation - None  

### Endpoint - /restaurant/cuisine/Korean
* Description - This route retrieves specific restaurants by cuisine in the database
* HTTP request verb - GET 
* Required data -  Cuisine from the restaurant table is required to be entered in the URL (string:cuisine) - example URL:'localhost:8080/restaurant/cuisine/Chinese'.
* Response data example- 
```
[
	{
		"id": 3,
		"restaurant_name": "Yung Kee",
		"address": "32-40 Wellington Street, Central, Hong Kong",
		"cuisine": "Chinese",
		"buffet": "no",
		"country": "China",
		"date": "2023-07-28",
		"comments_ratings": []
	}
]
```  
* Authentication methods - None
* Authourisation - None  

### Endpoint - /restaurant
* Description - This route creates a restaurant in the database
* HTTP request verb - POST 
* Required data (JSON) -  
```
{
	"restaurant_name": "Sushizanmai Tsukijiekimae-Ten",
	"address": "104-0045 Tokyo, Chuo City, Tsukiji, 3 Chome−11−9",
	"cuisine": "Japanese",
	"buffet": "no",
	"country": "Japan"
}
```
* Response data example- 
```
{
	"id": 7,
	"restaurant_name": "Sushizanmai Tsukijiekimae-Ten",
	"address": "104-0045 Tokyo, Chuo City, Tsukiji, 3 Chome−11−9",
	"cuisine": "Japanese",
	"buffet": "no",
	"country": "Japan",
	"date": "2023-07-28",
	"comments_ratings": []
}
```  
* Authentication methods - Bearer token
* Authourisation - Admin only  

### Endpoint - /restaurant/<int:id>
* Description - This route deletes a specific restaurant by id in the database
* HTTP request verb - DELETE 
* Required data -  Id from the restaurant table is required to be entered in the URL (int:id) - example URL:'localhost:8080/restaurant/6'.

* Response data example- 
```
{
	"message": "Restaurant 6 deleted successfully"
}
```  
* Authentication methods - Bearer token
* Authourisation - Admin only 

### Endpoint - /restaurant/<int:id>
* Description - This route updates a specific restaurant by id in the database
* HTTP request verb - PUT, PATCH 
* Required data -  Id from the restaurant table is required to be entered in the URL (int:id) to find the restaurant to update - example URL:'localhost:8080/restaurant/6'. Also entering the field that you want to update is required in the request body in JSON format which is shown below.  
```
{
	"restaurant_name": "Sushizanmai Tsukijiekimae-Ten",
	"address": "104-0045 Tokyo, Chuo City, Tsukiji, 3 Chome−11−9",
	"cuisine": "Japanese",
	"buffet": "no",
	"country": "Japan"
}
```

* Response data example- 
```
{
	"id": 7,
	"restaurant_name": "Sushizanmai Tsukijiekimae-Ten",
	"address": "104-0045 Tokyo, Chuo City, Tsukiji, 3 Chome−11−9",
	"cuisine": "Japanese",
	"buffet": "no",
	"country": "Japan",
	"date": "2023-07-28",
	"comments_ratings": []
}
```  
* Authentication methods - Bearer token
* Authourisation - Admin only  

### Endpoint - /favourites_list/<int:id>/favourite_restaurants
* Description - This route adds a specific restaurant by id to a specific favourites list by id to the favourite_restaurants table in the database
* HTTP request verb - POST
* Required data -  Favourites list Id from the favourites list table is required to be entered in the URL (int:id) to find the favourites list to update - example URL:'localhost:8080/favourites_list/2/favourite_restaurants'. Also entering the restaurant id that you want to the favourites list is required in the request body in JSON format which is shown below.  
```
{
	"restaurant_id": 2
}
```

* Response data example- 
```
{
	"id": 2,
	"list_name": "List 2",
	"date_created": "2023-07-28",
	"user": {
		"name": "User1",
		"email": "user1@email.com"
	},
	"favourite_restaurant": [
		{
			"id": 2,
			"restaurant": {
				"id": 2,
				"restaurant_name": "Rokkasen",
				"address": "Sun flower building F6・F7, 1-3-1, Nishishinjuku, Shinjiku-ku, Tokyo",
				"cuisine": "Japanese",
				"buffet": "yes",
				"country": "Japan",
				"date": "2023-07-28"
			}
		},
		{
			"id": 3,
			"restaurant": {
				"id": 3,
				"restaurant_name": "Yung Kee",
				"address": "32-40 Wellington Street, Central, Hong Kong",
				"cuisine": "Chinese",
				"buffet": "no",
				"country": "China",
				"date": "2023-07-28"
			}
		},
		{
			"id": 5,
			"restaurant": {
				"id": 2,
				"restaurant_name": "Rokkasen",
				"address": "Sun flower building F6・F7, 1-3-1, Nishishinjuku, Shinjiku-ku, Tokyo",
				"cuisine": "Japanese",
				"buffet": "yes",
				"country": "Japan",
				"date": "2023-07-28"
			}
		}
	]
}
```  
* Authentication methods - Bearer token
* Authourisation - Only the user who created the favourites list can add a restaurant to the favourites list in the favourite restaurants table of the database.  

### Endpoint - /favourites_list/<int:id>/favourite_restaurants/<int:favourite_restaurants_id>
* Description - This route deletes a specific restaurant from a favourites list in the favourite_restaurants table in the database
* HTTP request verb - DELETE
* Required data -  Favourites list Id from the favourites list table is required to be entered in the URL (int:id) to find the favourites list to update. Also, the favourite restaurant id is required - example URL:'localhost:8080/favourites_list/2/favourite_restaurants/5'. 
* Response data example- 
```
{
	"message": "Favourite restaurant id 5 deleted successfully"
}
```  
* Authentication methods - Bearer token
* Authourisation - Only the user who created the favourites list and admin can delete a restaurant from the favourites list in the favourite restaurants table of the database.  

### Endpoint - /comments_ratings/food_rating/<int:food_rating>
* Description - This route retrieves all comments based on food_rating field from the comments_ratings table in the database.
* HTTP request verb - GET
* Required data -  Food rating value from the comments_ratings table is required to be entered in the URL (int:food_rating) to find all comments with a specific food rating - example URL:'localhost:8080/comments_ratings/food_rating/5'. 
* Response data example- 
```
[
	{
		"id": 1,
		"message": "Great Japanese food",
		"food_rating": 5,
		"experience_rating": 5,
		"value_rating": 4,
		"date_created": "2023-07-28",
		"user": {
			"name": "User1",
			"email": "user1@email.com"
		},
		"restaurant": {
			"id": 2,
			"restaurant_name": "Rokkasen",
			"address": "Sun flower building F6・F7, 1-3-1, Nishishinjuku, Shinjiku-ku, Tokyo",
			"cuisine": "Japanese",
			"buffet": "yes",
			"country": "Japan",
			"date": "2023-07-28"
		}
	},
	{
		"id": 2,
		"message": "Best Japanese restaurant in Brisbane",
		"food_rating": 5,
		"experience_rating": 5,
		"value_rating": 4,
		"date_created": "2023-07-28",
		"user": {
			"name": "User1",
			"email": "user1@email.com"
		},
		"restaurant": {
			"id": 1,
			"restaurant_name": "Sono Japanese Restaurant",
			"address": "39 Hercules St, Hamilton QLD 4007",
			"cuisine": "Japanese",
			"buffet": "no",
			"country": "Australia",
			"date": "2023-07-28"
		}
	}
]
```  
* Authentication methods - None
* Authourisation - None  

### Endpoint - /comments_ratings/experience_rating/<int:experience_rating>
* Description - This route retrieves all comments based on experience_rating field from the comments_ratings table in the database.
* HTTP request verb - GET
* Required data -  Experience rating value from the comments_ratings table is required to be entered in the URL (int:experience_rating) to find all comments with a specific experience rating - example URL:'localhost:8080/comments_ratings/experience_rating/5'. 
* Response data example- 
```
[
	{
		"id": 1,
		"message": "Great Japanese food",
		"food_rating": 5,
		"experience_rating": 5,
		"value_rating": 4,
		"date_created": "2023-07-28",
		"user": {
			"name": "User1",
			"email": "user1@email.com"
		},
		"restaurant": {
			"id": 2,
			"restaurant_name": "Rokkasen",
			"address": "Sun flower building F6・F7, 1-3-1, Nishishinjuku, Shinjiku-ku, Tokyo",
			"cuisine": "Japanese",
			"buffet": "yes",
			"country": "Japan",
			"date": "2023-07-28"
		}
	},
	{
		"id": 2,
		"message": "Best Japanese restaurant in Brisbane",
		"food_rating": 5,
		"experience_rating": 5,
		"value_rating": 4,
		"date_created": "2023-07-28",
		"user": {
			"name": "User1",
			"email": "user1@email.com"
		},
		"restaurant": {
			"id": 1,
			"restaurant_name": "Sono Japanese Restaurant",
			"address": "39 Hercules St, Hamilton QLD 4007",
			"cuisine": "Japanese",
			"buffet": "no",
			"country": "Australia",
			"date": "2023-07-28"
		}
	}
]
```  
* Authentication methods - None
* Authourisation - None 

### Endpoint - /comments_ratings/value_rating/<int:value_rating>
* Description - This route retrieves all comments based on value_rating field from the comments_ratings table in the database.
* HTTP request verb - GET
* Required data -  Value rating value from the comments_ratings table is required to be entered in the URL (int:value_rating) to find all comments with a specific value rating - example URL:'localhost:8080/comments_ratings/value_rating/4'. 
* Response data example- 
```
[
	{
		"id": 1,
		"message": "Great Japanese food",
		"food_rating": 5,
		"experience_rating": 5,
		"value_rating": 4,
		"date_created": "2023-07-28",
		"user": {
			"name": "User1",
			"email": "user1@email.com"
		},
		"restaurant": {
			"id": 2,
			"restaurant_name": "Rokkasen",
			"address": "Sun flower building F6・F7, 1-3-1, Nishishinjuku, Shinjiku-ku, Tokyo",
			"cuisine": "Japanese",
			"buffet": "yes",
			"country": "Japan",
			"date": "2023-07-28"
		}
	},
	{
		"id": 2,
		"message": "Best Japanese restaurant in Brisbane",
		"food_rating": 5,
		"experience_rating": 5,
		"value_rating": 4,
		"date_created": "2023-07-28",
		"user": {
			"name": "User1",
			"email": "user1@email.com"
		},
		"restaurant": {
			"id": 1,
			"restaurant_name": "Sono Japanese Restaurant",
			"address": "39 Hercules St, Hamilton QLD 4007",
			"cuisine": "Japanese",
			"buffet": "no",
			"country": "Australia",
			"date": "2023-07-28"
		}
	}
]
```  
* Authentication methods - None
* Authourisation - None  

### Endpoint - /restaurant/<int:restaurant_id>/comments_ratings
* Description - This route creates a comments ratings record for a specfic restaurant in the comments_ratings table in the database
* HTTP request verb - POST
* Required data -  Restaurant id from the comments_ratings table is required to be entered in the URL (int:restaurant_id) to find the restaurant to comment on - example URL:'localhost:8080/restaurant/3/comments_ratings'. Also, to create a comment you need to enter in a message, food_rating, experience_rating, and value_rating in the request body in JSON format.  
```
{
	"message": "Best BBQ meats in Hong Kong",
	"food_rating": 5,
	"experience_rating": 5,
	"value_rating": 5
}
```

* Response data example- 
```
{
	"id": 3,
	"message": "Best BBQ meats in Hong Kong",
	"food_rating": 5,
	"experience_rating": 5,
	"value_rating": 5,
	"date_created": "2023-07-28",
	"user": {
		"name": "User1",
		"email": "user1@email.com"
	},
	"restaurant": {
		"id": 3,
		"restaurant_name": "Yung Kee",
		"address": "32-40 Wellington Street, Central, Hong Kong",
		"cuisine": "Chinese",
		"buffet": "no",
		"country": "China",
		"date": "2023-07-28"
	}
}
```  
* Authentication methods - Bearer token
* Authourisation - Only logged in users can create a comment.  

### Endpoint - /restaurant/<int:restaurant_id>/comments_ratings/<int:comments_ratings_id>
* Description - This route deletes a comment ratings record for a specfic restaurant in the comments_ratings table in the database
* HTTP request verb - DELETE
* Required data -  Restaurant id from the comments_ratings table is required to be entered in the URL (int:restaurant_id) to find the restaurant to delete, as well as the comments_ratings_id - example URL:'localhost:8080/restaurant/3/comments_ratings/3'. 
* Response data example- 
```
{
	"message": "Comment id 3 deleted successfully"
}
```  
* Authentication methods - Bearer token
* Authourisation - Only users who created the comment and admin can delete the comment.  

### Endpoint - /restaurant/<int:restaurant_id>/comments_ratings/<int:comments_ratings_id>
* Description - This route updates a comment ratings record for a specfic restaurant in the comments_ratings table in the database
* HTTP request verb - PUT, PATCH
* Required data -  Restaurant id from the comments_ratings table is required to be entered in the URL (int:restaurant_id) to find the restaurant to update, as well as the comments_ratings_id - example URL:'localhost:8080/restaurant/3/comments_ratings/4'. 
* Response data example- 
```
{
	"id": 4,
	"message": "Best roast BBQ meats in Hong Kong (updated)",
	"food_rating": 4,
	"experience_rating": 5,
	"value_rating": 5,
	"date_created": "2023-07-28",
	"user": {
		"name": "User1",
		"email": "user1@email.com"
	},
	"restaurant": {
		"id": 3,
		"restaurant_name": "Yung Kee",
		"address": "32-40 Wellington Street, Central, Hong Kong",
		"cuisine": "Chinese",
		"buffet": "no",
		"country": "China",
		"date": "2023-07-28"
	}
}
```  
* Authentication methods - Bearer token
* Authourisation - Only users who created the comment and admin can update the comment.  


# R6 An ERD for your app  
![Picture of ERD for the application](./docs/ERD-foodie_api.png)  

# R7 Detail any third party services that your app will use  
### Flask  
Flask was used to build this application. Flask is a popular web application framework or library written in Python, that is used for developing web pages and applications efficiently and easily (Garcia 2012 - 2023). It is built upon the Werkzeug WSGI toolkit and the Jinja2 template engine (Python Tutorial 2021). Werkzeug is a WSGI toolkit that implements various functionalities like requests, response objects, and utility functions (Python Tutorial 2021). Jinja2 is a widely used template engine for Python. It enables the combination of templates with specific data sources to dynamically render web pages (Python Tutorial 2021). The flask application starts by creating an instance of the Flask class, which acts as the central application object. This object is responsible for handling requests, routing, managing the application's configuration and other tasks (Flask 2010).Below is an example of how the Flask framework is used in the application:-  
```python
def create_app():
    app = Flask(__name__)

    app.json.sort_keys = False

    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")

    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'error': err.messages}, 400

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(auth_bp)
    app.register_blueprint(favourites_list_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(comments_ratings_bp_2)

    return app
```  

### PostgresQL  
PostgreSQL was used as the database management system for this application. For a detailed description of PostgreSQL, refer to R3.  

### SQLAlchemy  
SQLAlchemy was used as the ORM for this application. For a detailed description of SQLAlchemy, refer to R4.  

### Psycopg  
Psycopg2 is a popular Python library that acts as an adapter between flask and postgreSQL database (sourav_pd 2022). It basically builds a connection between flask and the database so that we can perform CRUD operations with the help of other third party libraries like SQLAlchemy.  

### Marshmallow  
Marshmallow is a Python library that provides object serialization/deserialization (Loria 2023). It provides a simple and flexible way to convert complex data types, such as objects or database records, into Python data types, and vice versa. This process is often referred to as "serialization" when converting complex data to simple data types (e.g., dictionaries, lists), and "deserialization" when converting simple data types back to complex data (Loria 2023). To integrate SQLAlchemy with Marshmallow, marshmallow-sqlalchemy must also be installed. Below is an example of how the marshmallow library is used in the application.  
```python
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
```
The above code indicates that a Schema of 'class RestaurantSchema' was defined. This schema defines the structure of the data that is sent to the user (client). The fields indicate what is being sent to the user. Marshmallow can also be used to validate the incoming data against the defined schema, in this case buffet, country, and cuisine variables.  

### Flask-Bcrypt  
Flask-Bcrypt is a Flask extension that provides an easy way to work with password hashing and verification in Flask applications (harshalpatil73 2023). Bcrypt is a well-regarded password-hashing function designed to be slow and computationally intensive, making it more resilient against brute-force attacks (harshalpatil73 2023).  
When a new user registers or sets a new password, Flask-Bcrypt is used to securely hash the plain-text password before storing it in the database. The process uses the bcrypt algorithm, which includes a salt and a cost factor to slow down the hashing process, making it computationally expensive for attackers to crack passwords via brute-force. This is utilised in the auth route of the application, when registering a new user as shown below.  
```python
# This route lets users register
@auth_bp.route('/register', methods=['POST'])
def auth_register():
    try:
        body_data = request.get_json()

        # Create a new User model instance from the user info
        user = User()
        user.name = body_data.get('name')
        user.email = body_data.get('email')
        # hashing the password in the database
        user.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
        # Add the user to the session
        db.session.add(user)
        # Commit to add the user to the database
        db.session.commit()
        # Respond to the client
        return user_schema.dump(user), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return { 'error': 'Email address already in use' }, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return { 'error': f'The {err.orig.diag.column_name} is required' }, 409
```

When a user attempts to log in, Flask-Bcrypt helps to compare the entered password with the hashed password stored in the database. This way, the application can determine if the provided password is correct without ever storing or transmitting the actual plain-text password. This can be seen in the login route of the application.  
```python
# This route lets the user login
@auth_bp.route('/login', methods=['POST'])
def auth_login():
    body_data = request.get_json()
    # Find the user by email address
    stmt = db.select(User).filter_by(email=body_data.get('email'))
    user = db.session.scalar(stmt)
    # If user exists and password is correct (verification step)
    if user and bcrypt.check_password_hash(user.password, body_data.get('password')):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return { 'email': user.email, 'token': token, 'is_admin': user.is_admin }
    else:
        return { 'error': 'Invalid email or password' }, 401
```

### Flask-JWT-Extended  
Flask-JWT-Extended is an extension of Flask that allows the use of JSON web tokens (JWT) for authentication and authorisation purposes in Flask applications (neekhara 2021). JWTs are used in this application for authentication and authorisation purposes. Once a user logs in, a JWT is generated, this token is used to authenticate the user to allow the user access to certain routes and operations. An example of how the token is used is shown below:-  
![Picture of auth login route and jwt token](./docs/auth-jwt.png)  
The above picture shows the auth route for when users login using Insomina platform, this generates a jWT token. The token can then be used on a route that requires authentication like creating a favourites list in the applicaiton using the token (Bearer Token).  
JSON Web Tokens are also a good way to securely transmit information between two parties as a JSON object (Auth0). There are three parts to the JWT token, these are header, payload, and signature which are seperated by dots (Auth0). The header typically consists of two parts: the type of token (which is JWT) and the signing algorithm being used (e.g., HMAC SHA256 or RSA). The payload contains the claims. Claims are statements about an entity (typically, the user) and additional data. There are three types of claims: registered, public, and private claims (Auth0). To create the signature part, you have to take the encoded header, the encoded payload, a secret, and the algorithm specified in the header, and sign that (Auth0). The signature is used to verify that the sender of the JWT is who it says it is and to ensure that the message wasn't changed along the way (Auth0).  
Several methods were used in the application from the Flask-jwt-extended library, these were 'create_access_token', 'jwt_required', and 'get_jwt_identity'. The 'create_access_token()' method generates the token so that the user can use this token to access certain routes. The 'jwt_required()' method was used as authourisation purposes, to ensure that the user had to be logged in to perform a certain operation. The 'get_jwt_identity()' method was used to get the user's id through the JSON Web Token.  

### Python-dotenv  
Python-dotenv is a Python library that provides a convenient way to load environment variables from a .env file into your Python application. It is particularly useful for managing configuration settings and sensitive information, such as API keys, database credentials, and other environment-specific variables (Chandra). This application stored the password that allows the connection to the database in a '.env' file, as well as the JWT secret key. By using dotenv, you can keep your sensitive information separate from the source code.  


# R8 Describe your projects models in terms of the relationships they have with each other  
### User model  
The User model is created with the help of SQLAlchemy (db.Model) and Flask. This essentially defines the structure of the table (users) to be created in the postgreSQL database. Below is code of the User model in the application.  
```python
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    favourites_list = db.relationship('Favourites_list', back_populates='user', cascade='all, delete')
    comments_ratings = db.relationship('Comments_ratings', back_populates='user', cascade='all, delete')
```  
It can be seen in the above code that the table name to be used is called 'users'. The attributes (which are columns in the table) for the User model are id, name, email, password, and is_admin. Contraints were defined for each attribute. Id is an Integer datatype, and is assigned as the primary key. Name is a String datatype that has a maximum character length of 100. Email is a String datatype that has a maximum character length of 100, it can't be empty (nullable=False), and must be unique (can't already exist). Password is a String datatype that has a maximum character length of 100, and can't be empty (nullable=False). The is_admin attribute is a Boolean datatype, and it's default state is False.  
The User Model has a one to many relationship with the Favourites_list model, as one user can create many favourites lists, thus the db.relationship() method is used to link these two models together to create more meaningful data. A 'favourites_list' variable is used to assign the relationship between User and Favourites_list models, which is used in 'back_populates' (attribute) in the 'Favourites_list' model. This links both models together as it can be seen that in the 'back_populates' attribute of the User model it states 'user', which is the variable that assigns the relationship between User and Favourites_list in the Favourites_list model. The 'cascade=all, delete' attribute deletes all records in the favourites_list table related to that user if that specific user is deleted.  
The User Model also has a one to many relationship with the Comments_ratings model, as one user can create multiple comments_ratings. The relationship method is used in the User model to link the 'Comments_raings' model.  

### Favourites_list Model  
With the Favourites_list Model the table name created for this in the database was 'favourites_list'. There were four attributes (columns) in the Model, which were id, list_name, date_created, and user_id. The code for the Favourites_list model is shown below.  
```python
class Favourites_list(db.Model):
    __tablename__="favourites_list"

    id = db.Column(db.Integer, primary_key=True)
    list_name = db.Column(db.String(100))
    date_created = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship('User', back_populates='favourites_list')
    favourite_restaurant = db.relationship('Favourite_restaurant', back_populates='favourites_list', cascade='all, delete')
```
The id was made as the primary key, list_name was a String datatype with maximum 100 character length, date_created was a Date datatype, and user_id is from the id of the User Model. The user_id is the foreign key in the Favourites_list model as it is the many side of the relationship between the User model. To create a bidirectional relationship with the User model the relationship() method is used 'user = db.relationship('User', back_populates='favourites_list')'.  
The Favourites_list model also has a one to many relationship with the Favourite_restaurant model, as one favourite list can have many favourite restaurants in it. The relationship() method was used to create the one to many relationship with the Favourite_restaurant model. The cascade='all, delete' option was used to ensure that the records in the favourite_restaurants table linked to the favourites_list id would be deleted, to maintain data integrity.  

### Favourite_restaurant Model  
With the Favourite_restaurant Model the table name created for this in the database was 'favourite_restaurants'. There are three attributes (columns) in the Model, which are id, favourites_list_id (foreign key), and restaurant_id (foreign key). The code for the Favourite_restaurant model is shown below.  
```python
class Favourite_restaurant(db.Model):
    __tablename__ = 'favourite_restaurants'

    id = db.Column(db.Integer, primary_key=True)

    favourites_list_id = db.Column(db.Integer, db.ForeignKey('favourites_list.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    favourites_list = db.relationship('Favourites_list', back_populates='favourite_restaurant')
    restaurant = db.relationship('Restaurant', back_populates='favourite_restaurant')
```  
The Favourite_restaurant model has one to many relationships with the Favourites_list model and the Restaurant model. This Model was created due to the many to many relationship between Favourites_list model and Restaurant model, as a favourites list can have many restaurants and a restaurant can be in many favourites lists. Foreign keys of 'favourites_list_id' and 'restaurant_id' from the favourites_list table and restaurants table help with establishing a many to many relationship through the Favourite_restaurants model. To create a bidirectional relationship with the Favourites_list model and the Restaurant model, the 'db.relationship()' method was used in the Favourite_restaurant model.  

### Restaurant Model  
With the Restaurant Model the table name created for this in the database was 'restaurants'. There are seven attributes (columns) in the Model, which are id (primary key), restaurant_name, address, cuisine, buffet, country, and date. The code for the Favourite_restaurant model is shown below.  
```python
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
```  
The Restaurant model has a one to many relationship with Favourite_restaurant model and the Comments_ratings model, as one restaurant can be in many Favourite_restaurants and one restaurant can have many comments_ratings. The Restaurant model has a many to many relationship with the User model, as a user can comment on many restaurants and a restaurant can be commented by many users. Hence, the Comments_ratings model was created. 

### Comments_ratings Model  
The Comments_ratings model was created due to a many to many relationship between the User model and Restaurant model. The Comments_ratings model has eight attributes, which are id (primary key), message, food_rating, experience_rating, value_rating, date_created, user_id (foreign key), and restaurant_id (foreign key). The code for the Comments_ratings model is shown below.  
```python
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
```   
The Comments_ratings model also, has a many to one relationship with the Restaurant and User models, hence the foreign keys of user_id and restaurant_id. These foreign keys have a constraint of 'nullable=False', as a record of a comment_rating must be created by a user on a restaurant, thus cannot be empty. The 'db.relationship()' method is used to create the association with the User and Restaurant model.  

### R9 Discuss the database relations to be implemented in your application  
Please refer to R6 for the ERD of the application, this ERD illustrates the relationships between each entity.  

### User Entity Relationships  
* It can be seen in the ERD that the users table/entity has a One-to-Many relationship with the favourites_list table/entity (indicated by crows foot notation). As one user can have multiple favourites lists. The primary key from the users entity is used as an attribute in the favourites_list table/entity as a foreign key to create the relationship.  
* For this particular application (food review app), there is a Many-to-Many relationship between the users entity and the restaurants entity. Hence a join table comments_ratings table/entity was created to help with data normalisation. A One-to-Many relationship to the comments_ratings entity can be seen in the ERD. The primary key of id from the users entity is used as a foreign key in the comments_ratings entity to create the relationship. Below is a picture of what the comments_ratings table looks like, with three records in it.
![Picture of comments_ratings table in postgresql](./docs/comments_ratings_table.png)  
It can be seen in the table above that the user_id column is included in the comments_ratings table as a foreign key. This helps normalise the data, reducing duplicate fields being stored in the database.  

### Favourites_list Entity Relationships  
* The favourites_list entity/table has a Many-to-One relationship with the users entity, as a favourites list can only come from one user. Therefore, a foreign key of user_id is used from the users entity to relate the tables with each other.  
* The favourites_list entity/table also has a One-to-Many relationship with the favourite_restaurants entity, as a favourites list can have many favourite restaurants. The primary key from the favourites_list table was used as a foreign key in the favourite_restaurants table to create the relationship between each other.  

### Favourite_restaurants Entity Relationships  
* The favourite_restaurants entity/table is the result of a Many-to-Many relationship between favourites_list and restaurants entities. It is a join table which helps with data normalisation. The favourite_restaurants entity has foreign keys of favourites_list_id and restaurant_id from the favourites_list (primary key) table and restaurants (primary key) table respectively. This join table is responsible for associating which favourites list contains what restaurants or which restaurants are in what favourites list.  

### Restaurants Entity Relationships  
* The restaurants entity has a One-to-Many relationship with the favourite_restaurants entity. To relate the tables with each other the primary key (id) from the restaurants table is used as a foreign key in the favourite_restaurants table.  
* The restaurants entity also has a One-to-Many relationship with the comments_ratings entity, as one restaurant can have many comments_ratings records associated with it. The primary key (id) from the restaurant table is used as a foreign key in the comment_ratings table to relate the tables with each other.  

### Comments_ratings Entity Relationships  
* The comments_ratings entity is a join table, as the user and restaurants entity has a Many-to-Many relationship. Join tables help in data normalisation, thus reducing duplicate data. The comments_ratings entity has foreign keys of user_id and restaurant_id which is from the users table (id - primary key) and restaurants table (id - primary key) respectively. This is how a relationship is created on these tables. This entity is used to associate which user created what comment for which restaurant/s or vice versa.  


### R10 Describe the way tasks are allocated and tracked in your project  
Trello was used to plan and track the tasks of this application. This is the link to the [Trello board](https://trello.com/b/rJpJ4X81/foodie-api). 
Trello is a widely used project management tool that shows what tasks need to be completed, who's working on tasks, and where each task is in the process. Cards were created in Trello to seperate the tasks into manageable chunks, which helped with the planning process.  
Six lists were created in the Trello board, these were API project Idea, To Do, Doing, Code Review, Testing and Done. The API project idea list outlined the overall idea of the project and what it's purpose was. The To Do list outlined the tasks that needed to be done to build the application. Cards were created in the To Do list to seperate all the tasks so that a timeline and priorities could be set for each task. Checklists were added into each card which outlined the more specific tasks within the card to be done. Due dates were set for each card and a 1 day reminder was setup so that I could keep track of when they needed to be done. Priorities 1 - 10 were given to the tasks. Priority 1 was creating the ERD and was considered the most important and needed to be done first, where as priority 10 was the least important, which was testing.  
The Doing list was used to show what tasks were currently being conducted and helped keep the API on track. The Code Review list was used as a reminder to review the code once all tasks had been completed. The Testing list was used as a reminder to conduct manual testing on the application to ensure all features worked properly. Lastly the Done list was used to ensure the project was progressing according to the timeline or due dates.


# Reference List  
* Ellingwood, J, 'The benefits of PostgreSQL', *Prisma's Data Guide*, web log post, viewed 27 July 2023, https://www.prisma.io/dataguide/postgresql/benefits-of-postgresql  
* IBM, What is a relational database?, viewed 26 July 2023, https://www.ibm.com/topics/relational-databases 
* Hoyos, M, 2018, 'What is an ORM and Why You Should Use it', *Search Medium*, web log post, 25 December, viewed 27 July 2023, https://blog.bitsrc.io/what-is-an-orm-and-why-you-should-use-it-b2b6f75f5e2a  
* Python Tutorial, 2021, *What is ORM?*, viewed 27 July 2023, https://pythonbasics.org/flask-sqlalchemy/
* vegibit, *What Is the Role of SQLAlchemy in Python Database Interactions*, viewed 28 July 2023, https://vegibit.com/what-is-the-role-of-sqlalchemy-in-python-database-interactions/  
* Garcia, M 2012 - 2023, 'Real Python', Use a Flask Blueprint to Architect Your Applications, web log post, viewed 28th July 2023,
https://realpython.com/flask-blueprint/  
* Python Tutorial, 2021, *What is Flask Python*, viewed 28 July 2023, https://pythonbasics.org/what-is-flask-python/  
* sourav_pd, 2022, 'Introduction to Psycopg2 module in Python', *GeeksforGeeks*, web log post, 2 December 2022, viewed 28 July 2023, https://www.geeksforgeeks.org/introduction-to-psycopg2-module-in-python/  
* Loria, S, 2023, *marshmallow: simplified object serialization*, viewed 28 July 2023, https://marshmallow.readthedocs.io/en/stable/  
* harshalpatil73, 2023, 'Password Hashing with Bcrypt in Flask', *GeeksforGeeks*, web log post, 21 March, viewed 28 July 2023, https://www.geeksforgeeks.org/password-hashing-with-bcrypt-in-flask/  
* aman neekhara, 2021, 'JSON web token | JWT', *GeeksforGeeks*, web log post, 21 December, viewed 28 July 2023, https://www.geeksforgeeks.org/json-web-token-jwt/  
* Auth0, *Introduction to JSON Web Tokens*, viewed 28 July 2023, https://jwt.io/introduction  
* Chandra, 'Unlock Secrets to Managing Your Credentials with “Python-dotenv”: Quickstart Guide', *Search Medium*, web log post, 30 March, viewed 28 July 2023, https://medium.com/@c17hawke/unlock-secrets-to-managing-your-credentials-with-python-dotenv-quickstart-guide-5e0e34cd5c9a