from grid import Grid, Room, colorToString
from math import ceil

# Helper function to print and run test cases with debugging output
def run_test(test_func):
    print(f"\n[TEST] {test_func.__name__}: {test_func.__doc__}")  # Print test description
    try:
        test_func()
        print(f"[PASS] {test_func.__name__}")
    except AssertionError as e:
        print(f"[FAIL] {test_func.__name__} - {e}")
    except Exception as e:
        print(f"[ERROR] {test_func.__name__} - {e}")
	
# Test Case 1: Grid Initialization with Valid Inputs
def test_makeGrid_valid():
    """Ensures the grid is correctly initialized with expected dimensions and border colors."""
    x, y = 5, 5
    print(f"\tCreating grid with dimensions: {x}x{y}")
    sampleGrid = Grid(x, y)
    
    print(f"\tChecking grid shape: Expected {(x, y, 3)}, Got {(len(sampleGrid.grid), len(sampleGrid.grid[1]), len(sampleGrid.grid[1][1]))}")
    assert (x, y, 3) == (len(sampleGrid.grid), len(sampleGrid.grid[1]), len(sampleGrid.grid[1][1])), "Grid dimensions are incorrect."
    
    print("\tChecking top-left border cell (should be black):", sampleGrid.grid[0][0])
    assert sampleGrid.grid[0][0] == (0, 0, 0), "Grid borders should be black."

# Test Case 2: Grid Initialization with Invalid Inputs
def test_makeGrid_invalid():
    """Verifies that invalid inputs raise the correct exceptions."""
    invalid_inputs = [("5", 5), (5, "5"), (-1, 1), (1,-1)]
    for x, y in invalid_inputs:
        print(f"\tTesting invalid input: x={x}, y={y}")
        try:
            Grid(x, y)
            assert False, f"Expected exception for x={x}, y={y}"
        except BaseException as e:
            print(f"\tCorrectly caught exception: {e}")

# Test Case 3: Room Placement With Valid Inputs
def test_room_valid():
    """Ensures the room is correctly initialized with an expected rectangle and color."""
    x, y, width, height, color = 1, 2, 3, 4, (55, 55, 55)
    print(f"\tCreating room located at: {x}x{y} spanning {width}x{height}")
    sampleRoom = Room(x, y, width, height, color)
    
    print(f"\tChecking room location: Expected location - ({x},{y}), Got ({sampleRoom.x},{sampleRoom.y})")
    assert x == sampleRoom.x and y == sampleRoom.y, "Room location is incorrect."
    
    print(f"\tChecking room dimension: Expected dimension - ({width},{height}), Got ({sampleRoom.width},{sampleRoom.height})")
    assert width == sampleRoom.width and height == sampleRoom.height, "Room dimension is incorrect."
    
    print(f"\tChecking room color: Expected color - {color}, Got {sampleRoom.color}")
    assert sampleRoom.color == color, "Room color is incorrect."

# Test Case 4: Room Placement With Invalid Inputs
def test_room_invalid():
    """Verifies that invalid inputs raise the correct exceptions."""
    invalid_inputs = [
		("5", 5, 5, 5, (1,1,1)), (5, "5", 5, 5, (1,1,1)),
		(5, 5, "5", 5, (1,1,1)), (5, 5, 5, "5", (1,1,1)),
		(-1, 5, 5, 5, (1,1,1)),  (5, 5, 5, 5, 5),
		(5, 5, 5, 5, (1, 1)),    (5, 5, 5, 5, ("1", 1, 1)),
		]
    for x, y, width, height, color in invalid_inputs:
        print(f"\tTesting invalid input: x={x}, y={y}, width={width}, height={height}, color={color}")
        try:
            Room(x, y, width, height, color)
            assert False, f"\tExpected exception for x={x}, y={y}, width={width}, height={height}, color={color}"
        except BaseException as e:
            print(f"\tCorrectly caught exception: {e}")

# Test Case 5: Room Placement Within Bounds
def test_roomPlacement():
    """Checks if a room is correctly placed inside the grid boundaries."""
    sampleGrid = Grid(10, 10)
    room = Room(1, 1, 3, 3, (100, 100, 100))
    
    print(f"\tPlacing room at x={room.x}, y={room.y}, width={room.width}, height={room.height}, color={room.color}")
    room.place(sampleGrid)
    
    check_x, check_y = (room.x, room.y)
    print(f"\tChecking room color at ({check_x}, {check_y}): Expected {room.color}, Got {sampleGrid.grid[check_x][check_y]}")
    assert sampleGrid.grid[check_x][check_y] == room.color, "Room color not applied correctly."

# Test Case 6: Prevent Room Overlapping Borders
def test_roomBorders():
    """Ensures that rooms do not overwrite the black grid borders."""
    sampleGrid = Grid(10, 10)
    room = Room(0, 0, 3, 3, (100, 100, 100))
    print(f"\tPlacing room at the top-left corner: {room.x}, {room.y}, should not overwrite borders.")
    room.place(sampleGrid)

    print("\tChecking border cell at (0,0): Expected black (0,0,0), Got", sampleGrid.grid[0][0])
    assert sampleGrid.grid[0][0] == (0, 0, 0), "Room should not overwrite grid borders."

# Test Case 7: Generate Random Rooms and Verify Grid Change
def test_generateRandomRooms():
    """Ensures that generating random rooms modifies the grid as expected."""
    sampleGrid = Grid(10, 10)
    
    # Copied the makeGrid result
    initial_grid = [[ceil((x % 9)/(x+1)) % 2*ceil((y % 9)/(y+1)) % 2 == 1 and \
        (225,225,225) or (0,0,0) for x in range(10)] for y in range(10)]
    print("\tChecking if grid is equal to the simulated grid...")
    assert initial_grid == sampleGrid.grid, "The simulated grid is not the same as the actual grid."
        
    print("\tGenerating 5 random rooms...")
    sampleGrid.generateRooms(5)

    print("\tChecking if grid has changed after adding rooms...")
    assert not initial_grid == sampleGrid.grid, "Grid did not change after adding rooms."

# Test Case 8: Validate Empty Grid Graph Display
def test_displayGraph():
    """Verifies that the graph display function does not return any value."""
    sampleGrid = Grid(3,3)
    print("\tDisplaying grid as graph (should see a visual output)")
    assert sampleGrid.displayGrid('Graph') is None, "Graph function should not return anything."

# Test Case 9: Validate Empty Grid Image Display
def text_displayImage():
    """Verifies that the image display function returns the correct value."""
    sampleGrid = Grid(3,3)
    # pyramid shape because why not
    grid_image_text = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA"\
       "oAAAAHgCAYAAAA10dzkAAAAOnRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb"\
       "24zLjEwLjAsIGh0dHBzOi8vbWF0cGxvdGxpYi5vcmcvlHJYcgAAAAlwSFlzAAAPYQ"\
       "AAD2EBqD+naQAACPRJREFUeJzt2LGNw1AMBUHzcH2o/7JUCd2DFHwYO5MTeOGCs7v7"\
       "4bGZOT0BAHLkyzt/L+8BAPgxAhAAIEYAAgDECEAAgBgBCAAQIwABAGIEIABAjAAEAIg"\
       "RgAAAMQIQACBGAAIAxAhAAIAYAQgAECMAAQBiBCAAQIwABACIEYAAADECEAAgRgACAMQ"\
       "IQACAGAEIABAjAAEAYgQgAECMAAQAiBGAAAAxAhAAIEYAAgDECEAAgBgBCAAQIwABAGIE"\
       "IABAjAAEAIgRgAAAMQIQACBGAAIAxAhAAIAYAQgAECMAAQBiBCAAQIwABACIEYAAADECEA"\
       "AgRgACAMQIQACAGAEIABAjAAEAYgQgAECMAAQAiBGAAAAxAhAAIEYAAgDECEAAgBgBCAAQI"\
       "wABAGIEIABAjAAEAIgRgAAAMQIQACBGAAIAxAhAAIAYAQgAECMAAQBiBCAAQIwABACIEYAAA"\
       "DECEAAgRgACAMQIQACAGAEIABAjAAEAYgQgAECMAAQAiBGAAAAxAhAAIEYAAgDECEAAgBgBCA"\
       "AQIwABAGIEIABAjAAEAIgRgAAAMQIQACBGAAIAxAhAAIAYAQgAECMAAQBiBCAAQIwABACIEYAA"\
       "ADECEAAgRgACAMQIQACAGAEIABAjAAEAYgQgAECMAAQAiBGAAAAxAhAAIEYAAgDECEAAgBgBCAA"\
       "QIwABAGIEIABAjAAEAIgRgAAAMQIQACBGAAIAxAhAAIAYAQgAECMAAQBiBCAAQIwABACIEYAAADE"\
       "CEAAgRgACAMQIQACAGAEIABAjAAEAYgQgAECMAAQAiBGAAAAxAhAAIEYAAgDECEAAgBgBCAAQIwAB"\
       "AGIEIABAjAAEAIgRgAAAMQIQACBGAAIAxAhAAIAYAQgAECMAAQBiBCAAQIwABACIEYAAADECEAAgRg"\
       "ACAMQIQACAGAEIABAjAAEAYgQgAECMAAQAiBGAAAAxAhAAIEYAAgDECEAAgBgBCAAQIwABAGIEIABAj"\
       "AAEAIgRgAAAMQIQACBGAAIAxAhAAIAYAQgAECMAAQBiBCAAQMz/6QHAc/d9n55A2HVdpycAD/kAAgDEC"\
       "EAAgBgBCAAQIwABAGIEIABAjAAEAIgRgAAAMQIQACBGAAIAxAhAAIAYAQgAECMAAQBiBCAAQIwABACIEY"\
       "AAADECEAAgRgACAMQIQACAGAEIABAjAAEAYgQgAECMAAQAiBGAAAAxAhAAIEYAAgDECEAAgBgBCAAQIwAB"\
       "AGIEIABAjAAEAIgRgAAAMQIQACBGAAIAxAhAAIAYAQgAECMAAQBiBCAAQIwABACIEYAAADECEAAgRgACAMQ"\
       "IQACAGAEIABAjAAEAYgQgAECMAAQAiBGAAAAxAhAAIEYAAgDECEAAgBgBCAAQIwABAGIEIABAjAAEAIgRgAA"\
       "AMQIQACBGAAIAxAhAAIAYAQgAECMAAQBiBCAAQIwABACIEYAAADECEAAgRgACAMQIQACAGAEIABAjAAEAYgQg"\
       "AECMAAQAiBGAAAAxAhAAIEYAAgDECEAAgBgBCAAQIwABAGIEIABAjAAEAIgRgAAAMQIQACBGAAIAxAhAAIAYAQ"\
       "gAECMAAQBiBCAAQIwABACIEYAAADECEAAgRgACAMQIQACAGAEIABAjAAEAYgQgAECMAAQAiBGAAAAxAhAAIEYAA"\
       "gDECEAAgBgBCAAQIwABAGIEIABAjAAEAIgRgAAAMQIQACBGAAIAxAhAAIAYAQgAECMAAQBiBCAAQIwABACIEYAAA"\
       "DECEAAgRgACAMQIQACAGAEIABAjAAEAYgQgAECMAAQAiBGAAAAxAhAAIEYAAgDECEAAgBgBCAAQIwABAGIEIABAjA"\
       "AEAIgRgAAAMQIQACBGAAIAxAhAAIAYAQgAECMAAQBiBCAAQIwABACIEYAAADECEAAgRgACAMQIQACAGAEIABAjAAEA"\
       "YgQgAECMAAQAiBGAAAAxAhAAIEYAAgDECEAAgBgBCAAQIwABAGIEIABAjAAEAIgRgAAAMQIQACBGAAIAxAhAAIAYAQg"\
       "AECMAAQBiBCAAQIwABACIEYAAADGzu3t6xC+bmdMTACBHvrzjAwgAECMAAQBiBCAAQIwABACIEYAAADECEAAgRgACAMQ"\
       "IQACAGAEIABAjAAEAYgQgAECMAAQAiBGAAAAxAhAAIEYAAgDECEAAgBgBCAAQIwABAGIEIABAjAAEAIgRgAAAMQIQACBG"\
       "AAIAxAhAAIAYAQgAECMAAQBiBCAAQIwABACIEYAAADECEAAgRgACAMQIQACAGAEIABAjAAEAYgQgAECMAAQAiBGAAAAxAh"\
       "AAIEYAAgDECEAAgBgBCAAQIwABAGIEIABAjAAEAIgRgAAAMQIQACBGAAIAxAhAAIAYAQgAECMAAQBiBCAAQIwABACIEYAAA"\
       "DECEAAgRgACAMQIQACAGAEIABAjAAEAYgQgAECMAAQAiBGAAAAxAhAAIEYAAgDECEAAgBgBCAAQIwABAGIEIABAjAAEAIgRg"\
       "AAAMQIQACBGAAIAxAhAAIAYAQgAECMAAQBiBCAAQIwABACIEYAAADECEAAgRgACAMQIQACAGAEIABAjAAEAYgQgAECMAAQAiB"\
       "GAAAAxAhAAIEYAAgDECEAAgBgBCAAQIwABAGIEIABAjAAEAIgRgAAAMQIQACBGAAIAxAhAAIAYAQgAECMAAQBiBCAAQIwABACI"\
       "EYAAADECEAAgRgACAMQIQACAGAEIABAjAAEAYgQgAECMAAQAiBGAAAAxAhAAIEYAAgDECEAAgBgBCAAQIwABAGIEIABAjAAEAIg"\
       "RgAAAMQIQACBGAAIAxAhAAIAYAQgAECMAAQBiBCAAQIwABACIEYAAADECEAAgRgACAMQIQACAGAEIABAjAAEAYgQgAECMAAQAiBG"\
       "AAAAxAhAAIEYAAgDECEAAgBgBCAAQIwABAGIEIABAjAAEAIgRgAAAMQIQACBGAAIAxAhAAIAYAQgAECMAAQBiBCAAQIwABACIEYAA"\
       "ADECEAAgRgACAMQIQACAGAEIABAjAAEAYgQgAECMAAQAiBGAAAAxAhAAIEYAAgB8Wr4aBBS5PVFClAAAAABJRU5ErkJggg=="
    
    
    print("\tChecking the image output to ensure it matches the actual...")
    assert sampleGrid.displayGrid() == grid_image_text, "Image function result does not match the actual."

# Test Case 10: Validate Empty Grid Text Display
def test_displayText():
    """Checks that the text display function is correctly handled."""
    sampleGrid = Grid(3,3)
    
    grid_text = "###\n#.#\n###\n"
    
    print("\tChecking text display output to ensure it matches the actual...")
    assert sampleGrid.displayGrid('Text') == grid_text, "Text display result does not match the actual."

# Test Case 11: Converting Color to String w/ a Valid Input
def test_colorToString_valid():
    """Ensures the correct string is returned based on the provided color.
    TODO: Add checks for other colors added."""
    valid_inputs = [
        (0,0,0), (225,225,225), (15,162,84)
    ]
    expected = ["#",".","_"]
    output = []
    for color in valid_inputs:
        print(f"\tChecking color {color} to ensure it matches {expected[len(output)]}")
        output.append(colorToString(color))
        assert expected[len(output) - 1] == output[len(output) - 1], "Color did not yield the expected string value."
    assert output == expected, "Strings do not match the expected result."

# Test Case 12: Converting Color to String w/ Invalid Inputs
def test_colorToString_invalid():
    """Exhaustive check to ensure that all invalid colors raise the correct exception."""
    invalid_inputs = [
        1, (0,0), (1.1,0,0), (0,"",0), (0,0,[1,2,3]),
        (-1,0,0), (0,-1,0), (0,0,-1)
    ]
    for color in invalid_inputs:
        print(f"\tTesting invalid input: color={color}")
        try:
            colorToString(color)
            assert False, f"\tExpected exception for color={color}"
        except BaseException as e:
            print(f"\tCorrectly caught exception: {e}")

# Test Case 13: Converting Grid location to Image location w/ Valid Inputs
def test_gridToImageLocation_valid():
    """Ensures that the top-left corner of the grid is correctly translated to the image location."""
    x, y = 5, 5
    sampleGrid = Grid(x, y)
    point1, point2 = (0,0), (1,1)
    loc = sampleGrid.toImageLocation(point1,point2)
    expected = (80, 0, 176, 96)
    print(f"\tChecking room location: Expected location - {expected}, Got ({loc[0]},{loc[1]},{loc[2]},{loc[3]})")
    assert loc == expected, "Grid location did not properly convert to image location"

# Test Case 14: Converting Grid location to Image location w/ Invalid Inputs
def test_gridToImageLocation_invalid():
    """Exhaustive check to ensure that all invalid rectangles raise the correct exception."""
    x, y = 5, 5
    sampleGrid = Grid(x, y)
    print(f"\tInitializing Grid(x={x}, y={y}) to test.")
    invalid_inputs = [
		(1,()), ((),1), ((),()), ((1,1),()), 
		((1.1,1),(1,1)), ((1,1.1),(1,1)), ((1,1),(1.1,1)), ((1,1),(1,1.1)), 
		((-1,1),(1,1)), ((1,-1),(1,1)), ((1,1),(-1,1)), ((1,1),(1,-1)),
		((1,1),(0,0)), ((0,1),(1,0)),
		((0,0),(6,6)),((6,6),(10,10))
    ]
    for point1, point2 in invalid_inputs:
        print(f"\tTesting invalid input: point1={point1}, point2={point2}")
        try:
            sampleGrid.toImageLocation(point1,point2)
            assert False, f"\tExpected exception for point1={point1}, point2={point2}"
        except BaseException as e:
            print(f"\tCorrectly caught exception: {e}")
# Run all tests
test_cases = [
    test_makeGrid_valid,
    test_makeGrid_invalid,
    test_room_valid,
    test_room_invalid,
    test_roomPlacement, 
    test_roomBorders,
    test_generateRandomRooms,
    test_displayGraph,
    text_displayImage,
    test_displayText,
    test_colorToString_valid,
    test_colorToString_invalid,
    test_gridToImageLocation_valid,
    test_gridToImageLocation_invalid,
]

print("Running tests...\n")
for test in test_cases:
    run_test(test)

print("\nAll tests completed!")
