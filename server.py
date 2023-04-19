from users_validation_app import app

from users_validation_app.controllers import user_controller
# ...server.py

if __name__ == "__main__":
    app.run(debug = True, port = 5001)
