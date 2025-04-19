from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
import math
import string
import random
import grid
import sqlite3
import sys
from MazeRoomDescr import ROOM_TYPES, generate_room_description, set_rooms_seed

sys.setrecursionlimit(10000)

connection = sqlite3.connect("Forgeon.db", check_same_thread=False)
cursor = connection.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS Maze (maze_id BIGINT, user varchar(255), name varchar(255),
x INT, y INT, seed INT, args varchar(512)) """)

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
def generate_image(
		x = 30, 
		y = 30, 
		seed = random.getrandbits(32), 
		filter=sum([0 | (1 << i) for i in range(0, len(ROOM_TYPES.keys()))]), 
		max_room_size=8, 
		room_num=8
	):
    """Creates a Grid object using the inputs and generates rooms/paths onto the grid."""
    sampleGrid = grid.Grid(x,y,seed)
    sampleGrid.generateRooms(room_num, max_room_size=max_room_size, filter=filter)
    sampleGrid.generatePath(1)
    return sampleGrid
    
def grab_map(grid):
    '''
    Takes the Grid and gets the room descriptions/locations
    Returns a list of [coordinates, roomName, description] pairs for each room
    '''
    set_rooms_seed(grid.seed)
    maze_data = []    
    for topleft, bottomright, color in grid.rooms:
        for type_name, info in ROOM_TYPES.items():
            if info['rgb'] == color:
                # Get coordinates for the room
                coords = grid.toImageLocation(topleft, bottomright)
                maze_data.append([
                    '{},{},{},{}'.format(*coords),
                    type_name,
                    f"{type_name}: {generate_room_description()}" # regenerates when you refresh page, intended?
                ])
                break    
    return maze_data

@app.route('/')
def welcome_page():
    sampleGrid = generate_image()
    # Check if the user is already authenticated
    if current_user.is_authenticated:
        # Redirect to the main page if logged in
        return render_template('home.html', 
		        username=get_username(), 
		        image=sampleGrid.displayGrid(),
		        maze=grab_map(sampleGrid),
                room_types=(list(ROOM_TYPES.keys()))
		    )
    return render_template('index.html', 
        username=get_username(), 
        image=sampleGrid.displayGrid(), 
        text=sampleGrid.displayGrid("Text"),
        maze=grab_map(sampleGrid)
        )

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
	
@app.route('/maze/randomize')
@login_required
def randomize_maze():
    # Randomize the maze parameters and generate a new maze with these parameters
    # Random width between 10 and 150
    x = random.randint(10, 150)
    # Random height between 10 and 150
    y = random.randint(100, 150)
    seed = random.getrandbits(32)
    # Customized to suite the grid size
    room_filter = random.getrandbits(len(ROOM_TYPES.keys()))
    max_room_size = random.randint(round(math.sqrt(min(x,y)/4)), round(math.sqrt(min(x,y)*4)))
    room_num = random.randint(round(math.sqrt((x+y)/4)), round(math.sqrt(x * y / (2*max_room_size))))
    sampleGrid = generate_image(x, y, seed, room_filter, max_room_size, room_num=room_num)
    return render_template('gridview.html', username=get_username(), image=sampleGrid.displayGrid(), x=x, y=y, seed=seed, args=f"rf={room_filter};rnum={room_num};mrsize={max_room_size}", room_types=list(ROOM_TYPES.keys()), maze=grab_map(sampleGrid))

@app.route('/maze/<int:x>/<int:y>/<int:seed>')
@login_required
def maze_view(x, y, seed):
    # make sure user input is valid
    if x < 10 or x > 200 or y < 10 or y > 200:
        flash(f"Invalid input: Width and height must be between 10 and 200.", "danger")
        # Redirect to default maze
        return redirect(url_for('maze_view', x=30, y=30, seed=random.getrandbits(32)))
    sampleGrid = generate_image(x, y, seed)
    return render_template('gridview.html', username=get_username(), image=sampleGrid.displayGrid(), x=x, y=y, seed=seed, args="", room_types=list(ROOM_TYPES.keys()), maze=grab_map(sampleGrid))

@app.route('/maze/<int:x>/<int:y>/<int:seed>/<string:args>')
@login_required
def arg_maze(x, y, seed, args):
    if x < 10 or x > 200 or y < 10 or y > 200:
        flash(f"Invalid input: Width and height must be between 10 and 200.", "danger")
        return redirect(url_for('maze_view', x=30, y=30, seed=random.getrandbits(32)))
    arg_list = args.split(';')
    room_filter = None
    room_num = 8
    max_room_size = None
    for arg in arg_list:
        if arg.split('=')[0] == 'rf':
            room_filter = int(arg.split('=')[1])
        elif arg.split('=')[0] == 'rnum':
            if int(arg.split('=')[1]) <= round(x * y / 100):
                room_num = int(arg.split('=')[1])
            else:
                flash(f"Invalid input: Room number must be less than {round(math.sqrt(x * y))} for dimensions ({x}, {y})", "danger")
                return redirect('/')
        elif arg.split('=')[0] == 'mrsize':
            if int(arg.split('=')[1]) < 5 or int(arg.split('=')[1]) > min(x,y):
                flash(f"Invalid input: Max room size must be between 5 and {min(x,y)}.", "danger")
                return redirect('/')
            else:
                max_room_size = int(arg.split('=')[1])

    if room_filter and max_room_size:
        sampleGrid = generate_image(x, y, seed, room_filter, max_room_size, room_num=room_num)
    elif room_filter:
        sampleGrid = generate_image(x, y, seed, room_filter, room_num=room_num)
    elif max_room_size:
        sampleGrid = generate_image(x, y, seed, max_room_size=max_room_size, room_num=room_num)
    else:
        sampleGrid = generate_image(x, y, seed, room_num=room_num)
    return render_template('gridview.html', username=get_username(), image=sampleGrid.displayGrid(), x=x, y=y, seed=seed, room_types=list(ROOM_TYPES.keys()), args=args, maze=grab_map(sampleGrid))

@app.route('/maze/custom', methods=['POST'])
@login_required
def custom_maze():
    # default values of 30x30
    x = int(request.form.get('width', 30))
    y = int(request.form.get('height', 30))
    
    # Random seed
    seed = random.getrandbits(32) 
    return redirect(url_for('maze_view', x=x, y=y, seed=seed))

@app.route('/save-maze', methods=['POST'])
@login_required
def save_maze():
    cursor.execute("SELECT MAX(maze_id) FROM Maze WHERE user = ?", (current_user.username,))
    maze_id = cursor.fetchone()
    if maze_id[0] != None:
        maze_id = int(maze_id[0]) + 1
    else:
        maze_id = 1
    # print(request.form.get('name'))
    cursor.execute("INSERT INTO Maze (maze_id, user, name, x, y, seed, args) VALUES (?, ?, ?, ?, ?, ?, ?)", (maze_id, current_user.username, request.json.get('name'), request.json.get('x'), request.json.get('y'), request.json.get('seed'), request.json.get('args')))
    connection.commit()
    return jsonify({"success": True})

@app.route('/my-mazes')
@login_required
def user_mazes():
    cursor.execute("SELECT maze_id, name, x, y, seed, args FROM Maze WHERE user = ? ORDER BY maze_id", (current_user.username,))
    mazes = cursor.fetchall()
    if len(mazes) == 0:
        return render_template('mazes.html', mazes=None, username=get_username())
    return render_template('mazes.html', mazes=[list(i) for i in mazes], username=get_username())

@app.route('/delete-maze', methods=['POST'])
@login_required
def delete_maze():
    cursor.execute("DELETE FROM Maze WHERE maze_id = ? AND user = ?", (int(request.json.get('id')), current_user.username))
    cursor.execute("SELECT MAX(maze_id) FROM Maze WHERE user = ?", (current_user.username,))
    maze_count = cursor.fetchone()
    if maze_count[0] != None:
        maze_count = int(maze_count[0]) + 1
    else:
        maze_count = 1

    for i in range(int(request.json.get('id')) + 1, maze_count):
        cursor.execute("UPDATE Maze SET maze_id = ? WHERE maze_id = ? AND user = ?", (i - 1, i, current_user.username))

    connection.commit()

    return jsonify({"success": True})
