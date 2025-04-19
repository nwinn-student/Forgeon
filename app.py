#if i break da code, return to this version

#Imports 
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
import math, string, random, grid, sqlite3, sys
from MazeRoomDescr import ROOM_TYPES, generate_room_description, set_rooms_seed

sys.setrecursionlimit(10000)

connection = sqlite3.connect("Forgeon.db", check_same_thread=False)
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Maze (
    maze_id BIGINT,
    user varchar(255),
    name varchar(255),
    x INT, y INT,
    seed INT,
    args varchar(512)
)""")

# Flask App Initialization
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = ''.join(random.choices(string.ascii_letters, k=255))

# DB and Login Setup 
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
    return current_user.username if current_user.is_authenticated else ""

def generate_image(x=30, y=30, seed=None, filter=None, max_room_size=8, room_num=8, template='default'):
    seed = seed or random.getrandbits(32)
    sampleGrid = grid.Grid(x, y, seed)
    if filter is None:
        filter = (1 << len(ROOM_TYPES)) - 1  # all room types allowed
    if template == "corridor":
        sampleGrid.generateCorridorLayout(room_count=room_num, max_room_size=max_room_size, filter=filter)
    else:
        sampleGrid.generateMaze()
        sampleGrid.generateRooms(room_num, max_room_size=max_room_size, filter=filter)
    return sampleGrid

# Extract Room Data from Grid 
def grab_map(grid_obj):
    set_rooms_seed(grid_obj.seed)
    result = []
    for topleft, bottomright, color in grid_obj.rooms:
        for type_name, info in ROOM_TYPES.items():
            if info['rgb'] == color:
                result.append({
                    "x": topleft[0], "y": topleft[1],
                    "x2": bottomright[0], "y2": bottomright[1],
                    "type": type_name,
                    "description": f"{type_name}: {generate_room_description(type_name)}"
                })
                break
    return result

#Home
@app.route('/')
def welcome_page():
    sampleGrid = generate_image()
    context = {
        "username": get_username(),
        "image": sampleGrid.displayGrid(),
        "maze": grab_map(sampleGrid),
        "room_types": list(ROOM_TYPES),
        "x": sampleGrid.x,
        "y": sampleGrid.y,
        "seed": sampleGrid.seed,
        "args": "rf=0;rnum=8;mrsize=8;template=default"
    }
    if current_user.is_authenticated:
        return render_template("home.html", **context)
    return render_template("index.html", text=sampleGrid.displayGrid("Text"), **context)

#Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('was_once_logged_in', None)
    flash("You have been logged out.")
    return redirect('/')

#Register account
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not Users.query.filter_by(username=request.form.get("username")).first():
            user = Users(username=request.form.get("username"), password=request.form.get("password"))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
        return render_template("register.html", username_exists=True, username=get_username())
    return render_template("register.html", username_exists=False, username=get_username())

#Login user
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(username=request.form.get("username")).first()
        if user and user.password == request.form.get("password"):
            login_user(user)
            return redirect('/')
        return render_template("login.html", failed=True, username=get_username())
    return render_template("login.html", failed=False, username=get_username())

#Account Settings Page
@app.route('/account')
@login_required
def account_settings():
    return render_template("settings.html", username=get_username())

#Password
@app.route('/account/password-update', methods=["POST"])
@login_required
def update_password():
    if request.form.get('password') == request.form.get('password-verification'):
        db.session.query(Users).filter(Users.id == current_user.get_id()).update({'password': request.form.get('password')})
        db.session.commit()
    return render_template("settings.html", username=get_username())

@app.route('/maze')
@login_required
def maze_redir():
    return redirect(f"/maze/30/30/{random.getrandbits(32)}")

#Random Maze Generator
@app.route('/maze/randomize')
@login_required
def randomize_maze():
    x = random.randint(10, 150)
    y = random.randint(100, 150)
    seed = random.getrandbits(32)
    room_filter = random.getrandbits(len(ROOM_TYPES))
    max_room_size = random.randint(round(math.sqrt(min(x, y) / 4)), round(math.sqrt(min(x, y) * 4)))
    room_num = random.randint(round(math.sqrt((x + y) / 4)), round(math.sqrt(x * y / (2 * max_room_size))))
    sampleGrid = generate_image(x, y, seed, room_filter, max_room_size, room_num)
    return render_template('gridview.html', username=get_username(), image=sampleGrid.displayGrid(), x=x, y=y, seed=seed, args=f"rf={room_filter};rnum={room_num};mrsize={max_room_size}", room_types=list(ROOM_TYPES), maze=grab_map(sampleGrid))

#Load Maze
@app.route('/maze/<int:x>/<int:y>/<int:seed>/<string:args>')
@login_required
def arg_maze(x, y, seed, args):
    if x < 10 or x > 200 or y < 10 or y > 200:
        flash("Invalid maze dimensions.", "danger")
        return redirect(url_for('maze_view', x=30, y=30, seed=random.getrandbits(32)))

    parsed = dict(arg.split('=') for arg in args.split(';') if '=' in arg)
    room_filter = int(parsed.get('rf', 0))
    room_num = int(parsed.get('rnum', 8))
    max_room_size = int(parsed.get('mrsize', 8))
    template = parsed.get('template', 'default')

    sampleGrid = generate_image(x, y, seed, room_filter, max_room_size, room_num, template)
    return render_template('gridview.html', username=get_username(), image=sampleGrid.displayGrid(), x=x, y=y, seed=seed, room_types=list(ROOM_TYPES), args=args, maze=grab_map(sampleGrid))

#Generate Maze filter
@app.route('/maze/custom', methods=["POST"])
@login_required
def custom_maze():
    x = int(request.form.get('width', 30))
    y = int(request.form.get('height', 30))
    seed = random.getrandbits(32)
    room_num = int(request.form.get('room-num', 8))
    max_room_size = int(request.form.get('max-room-size', 8))
    template = request.form.get('template', 'default')
    selected_rooms = request.form.getlist('room_type')

    room_filter = 0
    for i, name in enumerate(ROOM_TYPES):
        if name in selected_rooms:
            room_filter |= (1 << i)

    args = f"rf={room_filter};rnum={room_num};mrsize={max_room_size};template={template}"
    return redirect(url_for('arg_maze', x=x, y=y, seed=seed, args=args))

#Saving Maze to DB
@app.route('/save-maze', methods=["POST"])
@login_required
def save_maze():
    cursor.execute("SELECT MAX(maze_id) FROM Maze WHERE user = ?", (current_user.username,))
    row = cursor.fetchone()
    maze_id = row[0] + 1 if row[0] else 1
    cursor.execute("INSERT INTO Maze (maze_id, user, name, x, y, seed, args) VALUES (?, ?, ?, ?, ?, ?, ?)", (
        maze_id, current_user.username,
        request.json.get("name"),
        request.json.get("x"),
        request.json.get("y"),
        request.json.get("seed"),
        request.json.get("args")
    ))
    connection.commit()
    return jsonify({"success": True})

#List of Saved Mazes 
@app.route('/my-mazes')
@login_required
def user_mazes():
    cursor.execute("SELECT maze_id, name, x, y, seed, args FROM Maze WHERE user = ? ORDER BY maze_id", (current_user.username,))
    data = cursor.fetchall()
    return render_template("mazes.html", mazes=[list(row) for row in data] if data else None, username=get_username())

#Delete a Maze and Shift IDs
@app.route('/delete-maze', methods=["POST"])
@login_required
def delete_maze():
    maze_id = int(request.json.get("id"))
    cursor.execute("DELETE FROM Maze WHERE maze_id = ? AND user = ?", (maze_id, current_user.username))
    cursor.execute("SELECT MAX(maze_id) FROM Maze WHERE user = ?", (current_user.username,))
    max_id = cursor.fetchone()[0]
    max_id = max_id + 1 if max_id else 1
    for i in range(maze_id + 1, max_id):
        cursor.execute("UPDATE Maze SET maze_id = ? WHERE maze_id = ? AND user = ?", (i - 1, i, current_user.username))
    connection.commit()
    return jsonify({"success": True})

#Running Server
if __name__ == "__main__":
    app.run(debug=True)