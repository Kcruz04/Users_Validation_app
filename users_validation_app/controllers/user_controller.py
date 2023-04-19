# users.py
from users_validation_app import app
from flask import render_template,redirect,request,session,flash
from users_validation_app.models.user_model import User

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/read(all)")
def read_all():
    # call the get all classmethod to get all userss
    users = User.get_all()
    print(users)
    return render_template("read(all).html",users=users)

# relevant code snippet from server.py
#This takes the anchor tag to create a new user and returns creat.html
@app.route('/new_user')
def new_user():
    return render_template("create.html")

@app.route('/create_user', methods=["POST"])
def create_user():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    data = {
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"]
    }
    # We pass the data dictionary into the save method from the User class.
    User.save(data)
    #If values in html are same as in db we can use
    #@app.route('/friends/create', methods=['POST'])
    # def create_friend():
    #     Friend.save(request.form)
    #     return redirect('/')

    # Don't forget to redirect after saving to the database.
    return redirect('/')

#Recieves requests from client direct to  show, edit, or delete and pages
@app.route('/read(one)/<int:id>')
def read_one(id):
    users_from_controller = User.get_one(id)
    return render_template("read(one).html", users_from_controller = users_from_controller)

@app.route('/edit/<int:id>')
def edit_user(id):
    user = User.get_one(id)
    return render_template("edit.html", user = user)

@app.route('/update', methods = ["POST"])
def update():
    print(request.form)
    User.update(request.form)
    return redirect(f"/read(one)/{request.form['id']}")

@app.route('/delete/<int:id>')
def delete(id):
    print(id)
    User.delete(id)
    return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    # if not User.validate_user(request.form):
        # we redirect to the template with the form.
        print(request.form)
        if not User.validate(request.form):
            return redirect('/')
        
        User.register(request.form)
        # return redirect('/')
    # ... do other things
        return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    print(request.form)
    valid_email = User.login(request.form)
    if valid_email:
        session['uid'] = valid_email.id
        return redirect('/dashboard')
    else:
        return redirect('/')
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(('/'))

@app.route('/dashboard')
def dash():
    if 'uid' not in session:
        return redirect('/')

    return render_template("dashboard.html", user = User.get_id(session['uid']))

# @app.route('/create', methods=['POST'])
# def create_burger():
#     # if there are errors:
#     # We call the staticmethod on Burger model to validate
#     if not Burger.validate_burger(request.form):
#         # redirect to the route where the burger form is rendered.
#         return redirect('/')
#     # else no errors:
#     Burger.save(request.form)
#     return redirect("/burgers")
