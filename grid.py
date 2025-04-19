# if i break da code, return to this version 

from matplotlib import pyplot
import random
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from MazeRoomDescr import ROOM_TYPES

default_color = (0, 0, 0)
class Room:
    def __init__(self, x, y, width, height, color=default_color):
        if not all(isinstance(i, int) for i in [x, y, width, height]):
            raise BaseException('Room() - x, y, width, height must be ints.')
        if x < 0 or y < 0:
            raise BaseException('Room() - x and y must be >= 0.')
        if width < 1 or height < 1:
            raise BaseException('Room() - width and height must be >= 1.')
        if type(color) != tuple or len(color) != 3:
            raise BaseException('Room() - color must be a tuple of length 3.')

        # Set room attributes
        self.x, self.y, self.width, self.height, self.color = x, y, width, height, color

    # Places the room onto the grid and returns its location and color
    def place(self, grid):
        if type(grid) != Grid:
            raise BaseException('Room.place - Must be placed in a Grid.')
        for i in range(self.y, self.y + self.height):
            for j in range(self.x, self.x + self.width):
                if 0 <= i < grid.y and 0 <= j < grid.x:
                    grid.grid[i][j] = self.color
        return [(self.x, self.y), (self.x + self.width, self.y + self.height), self.color]

# Convert color to display characters for textual rendering
def colorToString(color):
    if color == (0, 0, 0): return '#'
    elif color == (225, 225, 225): return '.'
    return '_'  # for rooms

# Grid class represents the maze grid and contains logic for maze generation
class Grid:
    def __init__(self, x=30, y=30, seed=None):
        self.x, self.y, self.seed = x, y, seed or random.getrandbits(32)
        random.seed(self.seed)
        self.grid = [[(0, 0, 0) for _ in range(x)] for _ in range(y)]  # initialize with walls
        self.rooms = []  # stores rooms placed on the grid

    # Recursive backtracking maze generation algorithm
    def generateMaze(self):
        visited = [[False] * self.x for _ in range(self.y)]

        def in_bounds(x, y): return 1 <= x < self.x - 1 and 1 <= y < self.y - 1

        def neighbors(x, y):
            dirs = [(2,0), (-2,0), (0,2), (0,-2)]
            random.shuffle(dirs)
            return [(x+dx, y+dy, dx, dy) for dx,dy in dirs if in_bounds(x+dx, y+dy) and not visited[y+dy][x+dx]]

        def dfs(x, y):
            visited[y][x] = True
            self.grid[y][x] = (225, 225, 225)  # path color
            for nx, ny, dx, dy in neighbors(x, y):
                if not visited[ny][nx]:
                    self.grid[y + dy//2][x + dx//2] = (225, 225, 225)  # carve passage
                    dfs(nx, ny)

        start_x, start_y = (random.randrange(1, self.x - 1, 2), random.randrange(1, self.y - 1, 2))
        dfs(start_x, start_y)
        self.addRandomEntranceExit()

    # entrance and exit markers
    def addRandomEntranceExit(self):
        sides = {
            'left':   [(0, y) for y in range(1, self.y - 1, 2) if self.grid[y][1] == (225, 225, 225)],
            'right':  [(self.x - 1, y) for y in range(1, self.y - 1, 2) if self.grid[y][self.x - 2] == (225, 225, 225)],
            'top':    [(x, 0) for x in range(1, self.x - 1, 2) if self.grid[1][x] == (225, 225, 225)],
            'bottom': [(x, self.y - 1) for x in range(1, self.x - 1, 2) if self.grid[self.y - 2][x] == (225, 225, 225)]
        }

        available_sides = [side for side in sides if sides[side]]
        if len(available_sides) < 2:
            return

        entrance_side = random.choice(available_sides)
        opposites = {'left': 'right', 'right': 'left', 'top': 'bottom', 'bottom': 'top'}
        exit_side = opposites[entrance_side] if sides.get(opposites[entrance_side]) else random.choice([s for s in available_sides if s != entrance_side])

        entrance = random.choice(sides[entrance_side])
        exit = random.choice(sides[exit_side])

        self.grid[entrance[1]][entrance[0]] = (255, 0, 255)
        self.grid[exit[1]][exit[0]] = (255, 0, 255)

    # the corridor layout with branching rooms
    def generateCorridorLayout(self, room_count, max_room_size, filter=None):
        self.grid = [[(0, 0, 0) for _ in range(self.x)] for _ in range(self.y)]
        self.rooms = []
        path = []
        y = self.y // 2
        x = 1
        while 1 <= y < self.y - 1 and 1 <= x < self.x - 1:
            self.grid[y][x] = (225, 225, 225)
            path.append((x, y))
            if random.random() < 0.2:
                dy = random.choice([-1, 1])
                if 1 <= y + dy < self.y - 1:
                    y += dy
            else:
                x += 1

        if path:
            entrance = path[0]
            exit = path[-1]
            self.grid[entrance[1]][entrance[0]] = (255, 0, 255)
            self.grid[exit[1]][exit[0]] = (255, 0, 255)

        if filter is None:
            filter = (1 << len(ROOM_TYPES)) - 1

        room_pool = [info for i, (name, info) in enumerate(ROOM_TYPES.items()) if (filter >> i) & 1]
        if room_count <= len(room_pool):
            room_colors = random.sample(room_pool, room_count)
        else:
            room_colors = room_pool.copy()
            room_colors += random.choices(room_pool, k=room_count - len(room_pool))

        # Try placing rooms without overlap
        placed = 0
        attempts = 0
        max_attempts = room_count * 10
        while placed < room_count and attempts < max_attempts:
            attempts += 1
            width = random.randint(2, max_room_size)
            height = random.randint(2, max_room_size)
            x = random.randint(1, self.x - width - 2)
            y = random.randint(1, self.y - height - 2)

            overlap = False
            for yi in range(y, y + height):
                for xi in range(x, x + width):
                    if self.grid[yi][xi] != (0, 0, 0):
                        overlap = True
                        break
                if overlap:
                    break
            if overlap:
                continue

            color = room_colors[placed]['rgb']
            for yi in range(y, y + height):
                for xi in range(x, x + width):
                    self.grid[yi][xi] = color
            self.rooms.append(((x, y), (x + width, y + height), color))
            placed += 1

        # Connect each room to the nearest corridor point
        for (x1, y1), (x2, y2), _ in self.rooms:
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            nearest = min(path, key=lambda p: abs(p[0] - cx) + abs(p[1] - cy))
            nx, ny = nearest
            for ix in range(min(cx, nx), max(cx, nx) + 1):
                self.grid[cy][ix] = (225, 225, 225)
            for iy in range(min(cy, ny), max(cy, ny) + 1):
                self.grid[iy][nx] = (225, 225, 225)

    # Random room placement in existing maze
    def generateRooms(self, n, max_room_size=5, filter=None):
        if n < 1 or max_room_size < 1:
            return
        if filter is None:
            filter = (1 << len(ROOM_TYPES)) - 1

        room_pool = [info for i, (name, info) in enumerate(ROOM_TYPES.items()) if (filter >> i) & 1]
        if not room_pool:
            print("No rooms match filter:", bin(filter))
            return

        placed = 0
        attempts = 0
        if n <= len(room_pool):
            required_rooms = random.sample(room_pool, n)
        else:
            required_rooms = room_pool.copy()
            required_rooms += random.choices(room_pool, k=n - len(required_rooms))

        while placed < n and attempts < n * 10:
            attempts += 1
            width = random.randint(2, max_room_size)
            height = random.randint(2, max_room_size)
            x = random.randint(1, self.x - width - 2)
            y = random.randint(1, self.y - height - 2)

            overlap = False
            for yi in range(y, y + height):
                for xi in range(x, x + width):
                    current = self.grid[yi][xi]
                    if current != (0, 0, 0) and current != (225, 225, 225):
                        overlap = True
                        break
                if overlap: break
            if overlap: continue

            color = required_rooms[placed]['rgb']
            room = Room(x, y, width, height, color)
            room.place(self)
            self.rooms.append(((x, y), (x + width, y + height), color))
            placed += 1

    # Returns either image or text view of the maze
    def displayGrid(self, variant='Image'):
        return self.image() if variant == 'Image' else self.text()

    # Converts grid coordinates to image 
    def toImageLocation(self, point1, point2):
        try:
            min(self.squareHeight)  # testing existence
        except:
            a = min(480 * self.x / self.y, 640)
            b = min(640 * self.y / self.x, 480)
            self.squareWidth = a / self.x
            self.squareHeight = b / self.y
            self.startWidth = (640 - a) / 2
            self.startHeight = (480 - b) / 2

        return (
            self.startWidth + self.squareWidth * point1[0],
            self.startHeight + self.squareHeight * point1[1],
            self.startWidth + self.squareWidth * point2[0],
            self.startHeight + self.squareHeight * point2[1]
        )

    def image(self):
        fig = pyplot.figure()
        ax = pyplot.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.imshow(self.grid)
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
        fig.clear()
        return "data:image/png;base64," + base64.b64encode(pngImage.getvalue()).decode('utf8')

    # Generate text grid using characters
    def text(self):
        return '\n'.join(''.join(colorToString(cell) for cell in row) for row in self.grid)
