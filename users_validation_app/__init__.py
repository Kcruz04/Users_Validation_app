from flask import Flask
app=Flask(__name__)
from flask_bcrypt import Bcrypt

app.secret_key = "rootroot"
BCRYPT = Bcrypt(app)

DATABASE = "users_valid"
