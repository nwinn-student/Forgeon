from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
import string
import random
import grid
import sqlite3

connection = sqlite3.connect("Forgeon.db")
cursor = connection.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS Maze (maze_id BIGINT, user varchar(255), name varchar(255),
x INT, y INT, seed INT) """)

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
    
def grab_map(grid):
    '''
	    Takes the Grid and gets the room descriptions/locations
	    A sample for how the input should be:
		    [coords , description, more as needed (change the loop in the html files)]
		Default image size is 640 x 480, and it scales image up/down
    '''
    '''
		Potential formula (waiting on actual values to test practically):
		a = min(480x/y, 640)
		b = min(640y/x, 480)
		where x, y is grid.x, grid.y and a, b is the size of the image within the 640x480 image
		
		squareWidth = a/x # the width of each grid square
		squareHeight = b/y # the height of each grid square
		
		startWidth = (640 - a)/2 and startHeight = (480 - b)/2
		Should these be correct, upon receiving the rectangle for each room description we can output:
			["{startWidth + squareWidth*c_1.x},
			{startHeight + squareHeight*c_1.y},
			{startWidth + squareWidth*c_2.x}, 
			{startHeight + squareHeight*c_2.y}" , {roomDescription} , {whatever else we want to add...} ]
		for a single room.
		where c_1 is the topleft corner point and c_2 is the bottomright corner point
		
    '''
    return [["0,0,100,100","Sample description"]]

@app.route('/')
def welcome_page():
    sampleGrid = generate_image()
    # Check if the user is already authenticated
    if current_user.is_authenticated:
        # Redirect to the main page if logged in
        return render_template('home.html', 
		        username=get_username(), 
		        image=sampleGrid.displayGrid(),
		        maze=grab_map(sampleGrid) # use a better approach, this is for a sample
		    )
    # 
    return render_template('index.html', 
        username=get_username(), 
        image=sampleGrid.displayGrid(), 
        text=sampleGrid.displayGrid("Text"),
        maze=grab_map(sampleGrid) # use a better approach, this is for a sample
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
    # Random width between 10 and 100
    x = random.randint(10, 100)  
    # Random height between 10 and 100
    y = random.randint(10, 100)  
    seed = random.getrandbits(32)  
    return redirect(url_for('maze_view', x=x, y=y, seed=seed))

@app.route('/maze/<int:x>/<int:y>/<int:seed>')
@login_required
def maze_view(x, y, seed):
    # make sure user input is valid
    if x < 10 or x > 200 or y < 10 or y > 200:
        flash(f"Invalid input: Width and height must be between 10 and 200.", "danger")
        # Redirect to default maze
        return redirect(url_for('maze_view', x=30, y=30, seed=random.getrandbits(32)))
    return render_template('gridview.html', username=get_username(), image=generate_image(x, y, seed).displayGrid(), x=x, y=y, seed=seed)

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
    print(request.form.get('name'))
    cursor.execute("INSERT INTO Maze (maze_id, user, name, x, y, seed) VALUES (?, ?, ?, ?, ?, ?)", (maze_id, current_user.username, request.json.get('name'), request.json.get('x'), request.json.get('y'), request.json.get('seed')))
    connection.commit()
    return jsonify({"success": True})

@app.route('/my-mazes')
@login_required
def user_mazes():
    cursor.execute("SELECT maze_id, name, x, y, seed FROM Maze WHERE user = ? ORDER BY maze_id", (current_user.username,))
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