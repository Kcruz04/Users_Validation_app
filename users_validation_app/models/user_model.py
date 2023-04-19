# import the function that will return an instance of a connection
from users_validation_app.config.mysqlconnection import connectToMySQL
from flask import flash
from users_validation_app import DATABASE, app, BCRYPT
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)    # we are creating an object called bcrypt, 
                        # which is made by invoking the function Bcrypt with our app as an argument
class User:
    DB= "users_valid"
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database

    @classmethod
    def get_id(cls, id):
        data = {
            "id" : id
        }
        query = """
            SELECT * FROM users_valid
            WHERE id = %(id)s;
        """
        return cls(connectToMySQL(cls.DB).query_db( query, data )[0])
    
    @classmethod
    def validate(cls, form):
        is_valid = True # we assume this is true
        if len(form['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(form['email']):
            flash('invalid email')
            is_valid = False
        elif cls.get_by_email(form['email']):
            flash('email already registered')
        if form['password'] != form['confirm_password']:
            flash('passwords do not match')
            is_valid = False

        return is_valid

    @classmethod
    def valid_email(cls, form):
        pass

    @classmethod
    def register(cls, form):

        hash = BCRYPT.generate_password_hash( form['password'])
        print(hash)
        query = """INSERT INTO users_valid ( name , email , password ) 
        VALUES ( %(name)s , %(email)s ,%(password)s);"""
        # data is a dictionary that will be passed into the save method from server.py
        form = {
            **form,
            "password" : hash
        }
        return connectToMySQL(cls.DB).query_db( query, form )
    
    @classmethod
    def get_by_email(cls, email):
        data = {
            'email' : email
        }

        query = """
        SELECT * FROM users_valid
        WHERE email = %(email)s
        """
        results = connectToMySQL(cls.DB).query_db( query, data)
    
        if results:
            return cls(results[0])

        else:
            return False

    @classmethod
    def login(cls, form):
        valid_email = cls.get_by_email(form['email'])
        if valid_email:
            if BCRYPT.check_password_hash( valid_email.password, form['password']):
                return valid_email
            else:
                flash('Invalid password')
                return False
        else:
            flash("Invalid email!")
            return False




    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users_valid;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.DB).query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user) )
        return users
    @classmethod
    def get_one(cls, id):
        data = {
            "id" : id
        }
        query = """
            SELECT * FROM users_valid
            WHERE id = %(id)s;
        """
        connectToMySQL(cls.DB).query_db( query, data )
        results = connectToMySQL(cls.DB).query_db( query, data )
        user = cls(results[0])
        return user

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users_valid ( name , email , password created_at, updated_at ) VALUES ( %(name)s , %(email)s ,%(password)s, NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def update(cls, data):
        query = """
        UPDATE users_valid
        SET
        name = %(name)s,
        email = %(email)s
        WHERE id = %(id)s;
        """
        connectToMySQL(cls.DB).query_db( query, data )


    @classmethod
    def delete(cls,id):
        data = {
            "id" : id
        }
        query = """
        DELETE FROM users_valid
        WHERE id=%(id)s;
        """
        connectToMySQL(cls.DB).query_db( query, data )



