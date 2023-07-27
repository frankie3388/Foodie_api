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
* Required data -  
```
{
	"name": "User2",
	"email": "user2@email.com",
	"password": "password1"
}
```  
* Response data - 
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
  

# Reference List  
* Ellingwood, J, 'The benefits of PostgreSQL', *Prisma's Data Guide*, web log post, viewed 27 July 2023, https://www.prisma.io/dataguide/postgresql/benefits-of-postgresql  
* IBM, What is a relational database?, viewed 26 June 2023, https://www.ibm.com/topics/relational-databases 
* Hoyos, M, 2018, 'What is an ORM and Why You Should Use it', *Search Medium*, web log post, 25 December, viewed 27 July 2023, https://blog.bitsrc.io/what-is-an-orm-and-why-you-should-use-it-b2b6f75f5e2a  
* Python Tutorial, 2021, *What is ORM?*, viewed 27 July 2023, https://pythonbasics.org/flask-sqlalchemy/
* vegibit, *What Is the Role of SQLAlchemy in Python Database Interactions*, viewed 28 July 2023, https://vegibit.com/what-is-the-role-of-sqlalchemy-in-python-database-interactions/