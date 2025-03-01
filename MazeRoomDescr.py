import random
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

# Constants
WALL = '#'
PATH = '.'
START = 'S'
EXIT = 'E'

# Room Types with correlating Colors
ROOM_TYPES = {
    "Prison Room": {"symbol": "E", "color": "Dark Grey", "rgb": (80, 80, 80)},
    "Treasure Room": {"symbol": "T", "color": "Gold", "rgb": (255, 215, 0)},
    "Trap Room": {"symbol": "X", "color": "Orange", "rgb": (255, 140, 0)},
    "Monster Lair": {"symbol": "M", "color": "Blue", "rgb": (30, 144, 255)},
    "Secret Room": {"symbol": "S", "color": "Pink", "rgb": (255, 105, 180)},
    "Armory": {"symbol": "A", "color": "Silver", "rgb": (192, 192, 192)},
    "Library": {"symbol": "B", "color": "Brown", "rgb": (139, 69, 19)},
    "Alchemy Lab": {"symbol": "L", "color": "Dark Green", "rgb": (0, 100, 0)},
    "Puzzle Room": {"symbol": "Z", "color": "Cyan", "rgb": (0, 255, 255)},
    "Magic Chamber": {"symbol": "C", "color": "Purple", "rgb": (138, 43, 226)}
}

# Mapping colors to Unicode symbols
COLOR_ICONS = {
    "Gold": "🟨", "Brown": "🟫", "Orange": "🟧", "Dark Grey": "⬛",
    "Silver": "⬜", "Pink": "🟪", "Dark Green": "🟩",
    "Blue": "🟦", "Purple": "🟪", "Cyan": "🟦"
}

#Shuffle deques for randomness
def shuffled_deque(items):
    random.shuffle(items)
    return deque(items)

#componets of description sentences (50+ each)
ADJECTIVES = shuffled_deque([
    "red", "orange", "yellow", "green", "blue", "indigo", "violet", "scarlet", "golden", "silver", "dingy", "furry", "iridescent", "bloody", "dangerous",
    "dimly lit", "ancient", "dusty", "ornate", "mystical", "shimmering", "overgrown", "crumbling", "icy", "cursed", "sinister", "clean", "botanical", "windowless"
    "hot", "colossal", "glamorous", "plain", "unkempt", "dazzling", "repulsive", "small", "tall", "lethal", "damp", "ancient", "broad", "glistening", "colorful",
    "fabulous", "sparkly", "peaceful", "ugly", "bright", "odd", "narrow", "jagged", "magical", "majestic", "dreary", "snowy", "suspicious", "fluffy", "monochromatic",
    "tense", "sad", "windy", "pristine", "rancid", "enchanting", "filthy", "glorious", "flat", "decayed", "disgusting", "pretty", "beautiful", "furry", "frigid",
    "murky", "gloomy", "eerie", "smoky", "glistening", "sacred", "foul-smelling", "charred", "echoing", "ominous", "extraordinary", "outstanding", "spikey", "gory"
])

FEATURES = shuffled_deque([
    "runes", "artifacts", "statues", "faint glows", "whispers", "cobwebs", "skeletons", "strange symbols", "globes", "invisible items", "colorful potions", "clown masks", "trap doors",
    "glowing crystals", "rotting books", "twisting vines", "cracked mirrors", "floating candles", "silver chalices", "sleeping animals", "jars of organs", "bamboo fans", "tall flowers",
    "stone tablets", "gargoyle carvings", "bloodstains", "piles of bones", "enchanted tomes", "golden relics", "broken robots", "dismembered limbs", "music boxes", "frozen cryptids", "shadow figures",
    "iron chains", "ancient writings", "piles of gold", "cursed paintings", "moss-covered walls", "shattered glass", "mouse traps", "faded sketches", "royal clothing", "delicious food", 
    "twisted roots", "burning torches", "glowing fungi", "dark portals", "rusted weapons", "torn banners", "coffins", "buttons", "bloodthirsty leeches", "mysterious powder", "funhouse mirrors",
    "scattered scrolls", "moonlit inscriptions", "arcane sigils", "hollow statues", "withered vines", "old maps", "oil paintings", "shifty eyeballs", "fungi", "colorful mushrooms", "meat hooks",
    "luminescent glyphs", "hidden doors", "skulls", "haunted dolls", "floating feathers", "corroded shields", "portraits", "mysterious fluids", "funny photos", "enchanted rings", "hand grenades",
    "blackened cauldrons", "jade ornaments", "phantom imprints", "strange artifacts", "shadowy figures", "mystic orbs", "tall pillars", "magical scrolls", "sleepy familiars", "radioactive signs"
])

SOUNDS = shuffled_deque([
    "a distant echo", "a low hum", "mysterious whispers", "a crackling fire", "dripping water",
    "a soft rustling", "a deep growl", "chanting voices", "faint music", "a sharp screech",
    "rattling chains", "an eerie silence", "a sudden gust of wind", "soft laughter", "a heartbeat-like thumping",
    "footsteps in the distance", "a hollow whisper", "a loud bang", "crackling static", "soft breathing",
    "a deep moan", "a spectral howl", "clinking metal", "soft scratching", "an otherworldly chime",
    "a pulsating vibration", "a distant explosion", "a metallic ringing", "a guttural growl", "a distant scream",
    "a single dripping noise", "a faint ticking", "muffled voices", "a sudden crash", "grinding stone",
    "a beastly snarl", "scraping wood", "a soft thud", "a chorus of whispers", "gasping breaths",
    "a ghostly moan", "drumming fingers", "a rhythmic tapping", "a low drone", "a mystical chime",
    "a gust of wind through cracks", "fluttering wings", "scratching from behind the walls", "a hollow knock", "echoing footsteps"
])

ACTIONS = shuffled_deque([
    "inviting you in", "sending chills down your spine", "filling the air with unease", "making you feel watched",
    "urging you to move forward", "making the air feel heavy", "bringing a sense of nostalgia", "whispering unintelligible secrets",
    "creating an eerie tension", "pulling you toward the center", "giving an overwhelming feeling of dread", "making the walls seem alive",
    "distorting the space around you", "tempting you to explore", "pushing you back with an unseen force", "draining the warmth from your body",
    "making your skin tingle", "causing your vision to blur", "making it hard to breathe", "surrounding you with an unseen presence",
    "making your heartbeat race", "clouding your mind", "provoking an unexplained sorrow", "making the floor feel unstable",
    "enveloping you in a strange warmth", "mimicking voices you recognize", "making the air hum with energy", "repeating your footsteps behind you",
    "causing the light to flicker", "making shadows move on their own", "giving off a magnetic pull", "causing a strange ringing in your ears",
    "making time seem to slow down", "erasing the sound of your footsteps", "intensifying your fear", "pressing a weight upon your shoulders",
    "giving you the sensation of falling", "sending a tingling sensation through your body", "making it feel like you are being followed",
    "stirring up old memories", "causing an inexplicable chill", "making you feel both welcomed and threatened", "casting flickering shadows on the walls",
    "leaving a metallic taste in your mouth", "causing your surroundings to vibrate slightly", "creating a forceful energy in the room",
    "tricking your mind into hearing distant voices", "making the ground feel uneven", "making you feel strangely at peace",
    "giving the sense that something is hiding nearby", "making you feel lost in time"
])
#descriptions sentences (15)
SENTENCE_STRUCTURES = shuffled_deque([
    "You go into a {adjective} chamber. {feature} line the walls, while {sound} fills the air, {action}.",
    "This {adjective} hall is filled with {feature}. The sound of {sound} echoes around you, {action}.",
    "A/An {adjective} passage stretches before you, adorned with {feature}. The air is thick with {sound}, {action}.",
    "You find yourself in a {adjective} room where {feature} stand ominously. {sound} can be heard, {action}.",
    "A/An unsettling, {adjective} aura lingers in the air. {feature} surround the room, while {sound} fills the silence, {action}.",
    "As you enter the {adjective} room, {feature} cast eerie shadows along the walls. The presence of {sound} is overwhelming, {action}.",
    "The {adjective} corridor twists ahead, lined with {feature}. A faint echo of {sound} follows you, {action}.",
    "A/An {adjective} archway looms before you, leading into a space filled with {feature}. In the distance, {sound} resonates, {action}.",
    "The {adjective} chamber hums with energy. {feature} flicker in the dim light as {sound} reverberates through the space, {action}.",
    "You cautiously walk into a {adjective} vault. The floor is littered with {feature}, while {sound} slowly disappears in the distance, {action}.",
    "A/An {adjective} energy is in the air. {feature} surround the room, while {sound} echos in the distance, {action}.",
    "You quickly step into a {adjective} room. The floor is covered with {feature}, while {sound} grows louder, {action}.",
    "You stumble into a {adjective} room. It contains numerous {feature}, while {sound} follow closely behind you, {action}.",
    "This {adjective} area is hoarded with {feature}. The sound of {sound} stop as you enter, {action}.",
    "You fall into a {adjective} room. It is filled with numerous {feature}, you no longer hear {sound}, {action}.",

])

def generate_room_description():
    """Generates unique room descriptions by cycling elements and reshuffling periodically."""
    if len(ACTIONS) < 3:
        random.shuffle(ACTIONS)
    if len(SOUNDS) < 3:
        random.shuffle(SOUNDS)

    structure = SENTENCE_STRUCTURES.popleft()
    SENTENCE_STRUCTURES.append(structure)

    action = ACTIONS.popleft()
    sound = SOUNDS.popleft()
    feature = FEATURES.popleft()
    adjective = ADJECTIVES.popleft()

    ACTIONS.append(action)
    SOUNDS.append(sound)
    FEATURES.append(feature)
    ADJECTIVES.append(adjective)

    return structure.format(
        adjective=adjective,
        feature=feature,
        sound=sound,
        action=action
    )

def generate_maze(width, height, room_count, seed=None):
    """Generate a maze with rooms and return the maze grid and descriptions."""
    if seed is None:
        seed = random.random()
        print(f"Generated New Seed: {seed} - Use this to regenerate the same maze!") # new maze seed number
    else:
        print(f"Using Provided Seed: {seed} - This will generate the same maze.") # seed number of old maze

    random.seed(seed)

    maze = [[WALL for _ in range(width)] for _ in range(height)]
    room_grid = [[None for _ in range(width)] for _ in range(height)]
    desc_list = []

    def carve_passages_from(x, y):
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < width - 1 and 0 < ny < height - 1 and maze[ny][nx] == WALL:
                maze[y + dy // 2][x + dx // 2] = PATH
                maze[ny][nx] = PATH
                carve_passages_from(nx, ny)

    maze[1][1] = START
    maze[0][1] = PATH
    carve_passages_from(1, 1)

    maze[height - 3][width - 2] = EXIT
    maze[height - 3][width - 3] = PATH

    generate_rooms(maze, room_grid, room_count, desc_list)

    return maze, room_grid, desc_list, seed

def generate_rooms(maze, room_grid, count, desc_list):
    """Ensureing all rooms are unique when count ≥7, allowing duplicates only after 10."""
    room_types = list(ROOM_TYPES.keys())
    random.shuffle(room_types)

    height, width = len(maze), len(maze[0]) 

    def is_valid_room(x, y):
        """Ensureing the room does not block exits and does not overlap with another room."""
        return room_grid[y][x] is None and maze[y][x] == PATH

    selected_rooms = random.choices(room_types, k=count)
    placed_rooms = 0  

    for room_type in selected_rooms:
        attempts = 0
        while attempts < 100:  
            x = random.randint(1, width - 2)
            y = random.randint(1, height - 2)

            if is_valid_room(x, y):
                room_grid[y][x] = room_type  
                maze[y][x] = room_type  
                desc_list.append((ROOM_TYPES[room_type]['color'], room_type, generate_room_description()))  
                placed_rooms += 1
                break  
            
            attempts += 1

    if placed_rooms < count:
        print(f"Warning: Only {placed_rooms} rooms placed out of {count}. Maze might be too small.")

def display_maze(maze):
    """Display the maze using Matplotlib."""
    height, width = len(maze), len(maze[0])
    image = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            if maze[y][x] == START:
                image[y, x] = (0, 255, 0)  
            elif maze[y][x] == EXIT:
                image[y, x] = (255, 0, 0)  
            elif maze[y][x] == WALL:
                image[y, x] = (0, 0, 0)  
            elif maze[y][x] in ROOM_TYPES:
                image[y, x] = ROOM_TYPES[maze[y][x]]["rgb"]  
            else:
                image[y, x] = (255, 255, 255)  

    plt.figure(figsize=(8, 8))
    plt.imshow(image)
    plt.xticks([])
    plt.yticks([])
    plt.show()

if __name__ == "__main__":
    width = int(input("Enter maze width: "))
    height = int(input("Enter maze height: "))
    room_count = int(input("Enter number of rooms: "))
    
    maze, room_grid, descriptions, _ = generate_maze(width, height, room_count)
    
    print("\n **Maze Parameters:**")
    print(f"- Maze Size: {width} x {height}")
    print(f"- Number of Rooms: {room_count}")

    display_maze(maze)

    # group descriptions by room type & color
    descriptions_by_room = {}
    for color, room_type, desc in descriptions:
        key = (color, room_type)
        if key not in descriptions_by_room:
            descriptions_by_room[key] = []
        descriptions_by_room[key].append(desc)

    for (color, room_type), descs in descriptions_by_room.items():
        icon = COLOR_ICONS.get(color, "⬜")
        print(f"\n{icon} {color} ({room_type})")
        for desc in descs:
            print(f"- {desc}")