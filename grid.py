from matplotlib import pyplot
import random
import io
import base64
from math import ceil
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from MazeRoomDescr import ROOM_TYPES

def colorToString(color):
	if type(color) != tuple:
		raise BaseException('colorToString - Color must be a tuple.')
	if len(color) != 3:
		raise BaseException('colorToString - Color must be a tuple of length 3.')
	if type(color[0]) != int or type(color[1]) != int or type(color[2])!= int:
		# my favorite part of short circuits
		raise BaseException(f'colorToString - The {type(color[0]) != int and "first" or \
			type(color[1]) != int and "second" or \
			type(color[2]) != int and "third"} input into "color" must be an integer.') # your syntaxical colorer may not like this
	if color[0] < 0 or color[1] < 0 or color[2] < 0:
		raise BaseException(f'colorToString - The {color[0] < 0 and "first" or \
			color[1] < 0 and "second" or \
			color[2] < 0 and "third"} input into "color" must be at least 0.') # your syntaxical colorer may not like this
	if color == (0,0,0):
		return '#'
	elif color == (225,225,225):
		return '.'
	else:
		return '_'


# Class for the Grid
class Grid:
	# initializes the grid's size
	def __init__(self, x : int = 30, y : int = 30, seed : int = random.getrandbits(32)):
		random.seed(seed)
		if type(x) != int:
			raise BaseException('Grid() - The input "x" must be an int.')
		if type(y) != int:
			raise BaseException('Grid() - The input "y" must be an int.')
		if x < 3 or y < 3:
			raise BaseException('Grid() - The input for "x" or "y" must be at least 3.')
		self.x = x
		self.y = y
		self.seed = seed
		self.grid = self.makeGrid()
	# Creates a grid of x by y pixels, where the outermost layer is a black 1 pixel thick border
	def makeGrid(self):
	 	return [[ceil((x % (self.x-1))/(x+1)) % 2*ceil((y % (self.y-1))/(y+1)) % 2 == 1 and \
	 		(225,225,225) or (0,0,0) for x in range(self.x)] for y in range(self.y)]
     
	# generates n randomly sized rooms within grid 
	def generateRooms(self, n, max_room_size = 5):
		if type(n) != int or type(max_room_size) != int:
			raise BaseException('Grid.generateRooms - The input "n" must be an int.')
		if type(max_room_size) != int:
			raise BaseException('Grid.generateRooms - The input "max_room_size" must be an int.')
		if n < 1 or max_room_size < 1:
			raise BaseException('Grid.generateRooms - The input "n" or "max_room_size" must be at least 1.')
			
		room_types = list(ROOM_TYPES.keys())
		random.shuffle(room_types)
		
		# If we need more rooms than types, allow duplicates
		if n > len(room_types):
			room_types.extend(random.choices(room_types, k=n - len(room_types)))
		
		for i in range(n):
			width = random.randint(2, max_room_size)
			height = random.randint(2, max_room_size)
			x = random.randint(1, self.x - width)
			y = random.randint(1, self.y - height)
			# Uses color from ROOM_TYPES
			color = ROOM_TYPES[room_types[i]]['rgb']
			Room(x, y, width, height, color).place(self)
    
    # converts a rectangle from grid space into image space, then to a string
	def toImageLocation(self, point1, point2) -> str:
		if type(point1) != tuple or type(point2) != tuple:
			raise BaseException(f'Grid.toImageLocation - {type(point1) != tuple and "point1" or "point2"} must be a tuple.')
		if len(point1) != 2 or len(point2) != 2:
			raise BaseException(f'Grid.toImageLocation - {len(point1) != 2 and "point1" or "point2"} must be of length 2.')
		if type(point1[0]) != int or type(point1[1]) != int or type(point2[0]) != int or type(point2[1]) != int:
			raise BaseException(f'Grid.toImageLocation - {\
				(type(point1[0]) != int or type(point2[0]) != int) and "first" or "second"} input into {\
				(type(point1[0]) != int or type(point1[1]) != int) and "point1" or "point2"} must be an integer.') # your syntaxical colorer may not like this
		if point1[0] < 0 or point1[1] < 0 or point2[0] < 0 or point2[1] < 0:
			raise BaseException(f'Grid.toImageLocation - {\
				(point1[0] < 0 or point2[0] < 0) and "first" or "second"} input into {\
				(point1[0] < 0 or point1[1] < 0) and "point1" or "point2"} must be at least 0.') # your syntaxical colorer may not like this
		if point1[0] >= point2[0] or point1[1] >= point2[1]:
			raise BaseException(f'Grid.toImageLocation - {\
				point1[0] > point2[0] and "first" or "second"} input into point2 must be less than {\
				point1[0] > point2[0] and point1[0] or point1[1]}.') # your syntaxical colorer may not like this
		if point1[0] > self.x or point1[1] > self.y or point2[0] > self.x or point2[1] > self.y:
			raise BaseException(f'Grid.toImageLocation - {\
				(point1[0] > self.x or point1[1] > self.y) and "point1" or "point2"} cannot be beyond Grid(x={self.x},y={self.y}).')
		try:
			print(self.squareHeight)
		except:
			a = min(480*self.x/self.y, 640)
			b = min(640*self.y/self.x, 480)
			self.squareWidth = a/self.x # the width of each grid square
			self.squareHeight = b/self.y # the height of each grid square
			self.startWidth = (640 - a)/2
			self.startHeight = (480 - b)/2	
		return (
			self.startWidth + self.squareWidth*point1[0],
			self.startHeight + self.squareHeight*point1[1],
			self.startWidth + self.squareWidth*point2[0],
			self.startHeight + self.squareHeight*point2[1])
		
        
    
	# displays the grid either through an image or through text
	def displayGrid(self, variant = 'Image'):
		return variant == 'Image' and self.image() or \
			variant == 'Graph' and self.graph() or \
			variant == 'Text' and self.text() or \
			None
		
	# displays the graph onto the screen
	def graph(self):
		fig = pyplot.figure()
		ax = pyplot.Axes(fig, [0., 0., 1., 1.])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(self.grid)
		fig.clear()
		pass
	
	# converts the graph into an base64 image to be viewed on the web
	def image(self):
		fig = pyplot.figure()
		ax = pyplot.Axes(fig, [0., 0., 1., 1.])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(self.grid)
		# Source: https://gitlab.com/-/snippets/1924163
		pngImage = io.BytesIO()
		FigureCanvas(fig).print_png(pngImage)
		fig.clear()
		return "data:image/png;base64," + base64.b64encode(pngImage.getvalue()).decode('utf8')
        
	# saves the image as a png
	def save(self):
		pyplot.imsave('sample.png', self.grid)
		
	# textify
	def text(self):
		t = ""
		for x in range(self.y):
			for y in range(self.y):
				t += colorToString(self.grid[x][y])
			t += "\n"
		return t

# Class for Rooms
class Room:
	# initializes room
	def __init__(self, x, y, width, height, color=(0, 0, 0)):
		if type(x) != int or type(y) != int or type(width) != int or type(height) != int:
			raise BaseException(f'Room() - The input {type(x) != int and "x" or \
				type(y) != int and "y" or \
				type(width) != int and "width" or \
				type(height) != int and "height"} must be an int.') # your syntaxical colorer may not like this
		if x < 0 or y < 0:
			raise BaseException('Room() - The input for "x" or "y" must be at least 0.')
		if width < 1 or height < 1:
			raise BaseException('Room() - The input for "width" or "height" must be at least 1.')
		if type(color) != tuple or len(color) != 3:
			raise BaseException('Room() - The input for "color" must be a tuple of length 3.')
		if type(color[0]) != int or type(color[1]) != int or type(color[2])!= int:
			raise BaseException(f'colorToString - The {type(color[0]) != int and "first" or \
				type(color[1]) != int and "second" or \
				type(color[2]) != int and "third"} input into "color" must be an integer.') # your syntaxical colorer may not like this
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color
		
	# places generated rooms onto grid
	def place(self, grid):
		if type(grid) != Grid:
			raise BaseException('Room.place - Room must be placed within a Grid object.')
		# reminder to make sure that the values for x, y, width, height are within the bounds of the Grid object
		max_y, max_x = grid.y, grid.x  # get grid dimensions
		for i in range(self.y, self.y + self.height):
			for j in range(self.x, self.x + self.width):
				if 0 <= i < max_y and 0 <= j < max_x:  #  ensure within bounds
					if grid.grid[i][j] != (0, 0, 0):  # avoid overwriting borders
						grid.grid[i][j] = self.color
		return grid      
