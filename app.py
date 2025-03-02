from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
import string
import random
import grid

app = Flask(__name__)
secret_key = ''
for i in range(255):
    secret_key += random.choice(string.ascii_letters)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = secret_key

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

db.init_app(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

def get_username():
    if current_user and current_user.is_authenticated:
        return current_user.username
    else:
        return ""

# For grid
def generate_image(x = 30, y = 30, seed = random.getrandbits(32)):
    sampleGrid = grid.Grid(x,y,seed)
    sampleGrid.generateRooms(8, max_room_size=8)
    return sampleGrid

@app.route('/')
def welcome_page():
    sampleGrid = generate_image()
    # Check if the user is already authenticated
    if current_user.is_authenticated:
        # Redirect to the main page if logged in
        return render_template('home.html', username=get_username(), image=sampleGrid.displayGrid())
    # 
    return render_template('index.html', username=get_username(), image=sampleGrid.displayGrid(), text=sampleGrid.displayGrid("Text"))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    if session.get('was_once_logged_in'):
        del session['was_once_logged_in']
    flash('You have been logged out. Feel free to close the browser.')
    return redirect('/')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if Users.query.filter_by(username=request.form.get("username")).first() == None:
            user = Users(username=request.form.get("username"),
                        password=request.form.get("password"),)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login", username=get_username()))
        else:
            return render_template("register.html", username=get_username(), username_exists=True)
    return render_template("register.html", username=get_username(), username_exists=False)

@app.route('/login', methods=["GET", "POST"])
def login():
    user = None
    if request.method == "POST":
        user = Users.query.filter_by(username=request.form.get("username")).first()
        if user and user.password == request.form.get("password"):
            login_user(user)
            return redirect('/')
        else:
            return render_template("login.html", failed=True, username=get_username())
    return render_template("login.html", failed=False, username=get_username())

@app.route('/account')
@login_required
def account_settings():
    if current_user.is_authenticated:
        return render_template("settings.html", username=get_username())


@app.route('/account/password-update', methods=["POST"])
@login_required
def update_password():
    if current_user.is_authenticated:
        if request.form.get('password') == request.form.get('password-verification'):
            db.session.query(Users).filter(Users.id == current_user.get_id()).update({'password': request.form.get('password')})
            db.session.commit()
        return render_template("settings.html", username=get_username())

@app.route('/maze')
@login_required
def maze_redir():
    return redirect('/maze/30/30/' + str(random.getrandbits(32)))

@app.route('/maze/<int:x>/<int:y>/<int:seed>')
@login_required
def maze_view(x, y, seed):
    return render_template('gridview.html', image=generate_image(x, y, seed).displayGrid(), x=x, y=y, seed=seed)