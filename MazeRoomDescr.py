import random
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import re

class ShufflingCycle:
    def __init__(self, items):
        self.original_items = list(items)
        self._shuffle()

    def _shuffle(self):
        self.items = deque(self.original_items)
        random.shuffle(self.items)

    def __next__(self):
        if not self.items:
            self._shuffle()
        return self.items.popleft()

def set_rooms_seed(seed):
    random.seed(seed)

WALL = '#'
PATH = '.'
START = 'S'
EXIT = 'E'

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

COLOR_ICONS = {
    "Gold": "🟨", "Brown": "🟧", "Orange": "🟧", "Dark Grey": "⬛",
    "Silver": "⬜", "Pink": "🟪", "Dark Green": "🟩",
    "Blue": "🟦", "Purple": "🟪", "Cyan": "🟦"
}

VOWELS = {'a', 'e', 'i', 'o', 'u'}

SENTENCE_STRUCTURES = deque([
    "You go into a {adjective} chamber. {feature} line the walls, while {sound} fills the air, {action}.",
        "This {adjective} hall is filled with {feature}. The sound of {sound} echoes around you, {action}.",
        "A {adjective} passage stretches before you, adorned with {feature}. The air is thick with {sound}, {action}.",
        "You find yourself in a {adjective} room where {feature} stand ominously. {sound} can be heard, {action}.",
        "An unsettling, {adjective} aura lingers in the air. {feature} surround the room, while {sound} fills the silence, {action}.",
        "As you enter the {adjective} room, {feature} cast eerie shadows along the walls. The presence of {sound} is overwhelming, {action}.",
        "The {adjective} corridor twists ahead, lined with {feature}. A faint echo of {sound} follows you, {action}.",
        "A {adjective} archway looms before you, leading into a space filled with {feature}. In the distance, {sound} resonates, {action}.",
        "The {adjective} chamber hums with energy. {feature} flicker in the dim light as {sound} reverberates through the space, {action}.",
        "You cautiously walk into a {adjective} vault. The floor is littered with {feature}, while {sound} slowly disappears in the distance, {action}.",
        "A {adjective} energy is in the air. {feature} surround the room, while {sound} echos in the distance, {action}.",
        "You quickly step into a {adjective} room. The floor is covered with {feature}, while {sound} grows louder, {action}.",
        "You stumble into a {adjective} room. It contains numerous {feature}, while {sound} follow closely behind you, {action}.",
        "This {adjective} area is hoarded with {feature}. The sound of {sound} stop as you enter, {action}.",
        "You fall into a {adjective} room. It is filled with numerous {feature}. You no longer hear {sound}, {action}.",
        "You hear the sound of {sound} chasing closely behind you. You escape into a {adjective} room containing {feature}, {action}.",
        "As you enter, you see {feature} inside this {adjective} space, {action}. {sound} soften the longer you are in here.",
        "As you walk in, you see {feature} inside this {adjective} area, {action}. {sound} start playing.",
        "As you enter the {adjective} space, you notice {feature}, {action}. {sound} grow louder the longer you are in here.",
        "You follow the sound of {sound} and discover a {adjective} area. It is occupied with {feature}, {action}.",
        "You cautiously walk through the door into a {adjective} room. It is packed with {feature}. In the corner, a speaker is playing {sound}, {action}.",
        "You carelessly stumble into a {adjective} area. After hearing {sound}, the doors lock behind you, {action}.",
        "After falling through a hole, you find yourself in a {adjective} space. You hear {sound} before you notice the {feature} surround you, {action}.",
        "Face to face with a {adjective} door, {sound} being heard behind it.{action}. Upon entering, you first notice the {feature}.",
])

ROOM_COMPONENTS = {
    "Prison Room": {
    "adjectives": ["dark", "damp", "cold", "claustrophobic", "silent",
    "grimy", "decaying", "chained", "windowless", "oppressive","rusted", "musty", "moldy", "stench-filled", "narrow",
    "cursed", "bleak", "foul", "haunting", "gloomy", "dingy",
    "infested", "cracked", "worn-down", "sooty", "dreary",
    "stained", "dismal", "suffocating", "bleeding", "desolate",
    "grim", "bound", "rust-stained", "tight", "unkempt",
    "frigid", "wet", "cobwebbed", "echoing", "lonely"],
        
        "features": ["iron bars", "rusty chains", "flickering torches", "padlocked cells", "old skeletons", "piles of bones", "bloodstained bricks", "torture devices", "skeletal remains", "rotting corpses", "broken mirrors", "cracked stones", "ring of keys", "buckets filled with indistinguishable liquids", "large maggots", "faded journals", 
        "chalk lines", "stained beds", "broken bottles", "venomous millipedes", "rusty instruments", "carved words", "old diaries", "uncompleted wills", "bottles of teeth", "dirty bandages", "medical supplies", "rusty weapons", "skeleton keys", "bottles of wailing moans", "souls trapped in containers", "executioner attire", 
        "weapons hidden in food", "tins of food", "beautiful wicker baskets full of human hearts", "tufts of human hair", "Fifty feet of coiled steel-infused ropes", "corpse-worms that gets smarter with each brain it eats", "prisoner diaries", "tear stained letters", "clothes in surprisingly good condition", "resurrection incantations", 
        "necromancer spells", "books with various torture methods", "gold plated bones", "smiling skulls", "mummification materials", "giant animated skeletons", "prisoner spirits", "skeleton armor", "angry rats", "sleeping bats", "crumbling stone benches",
        "locked cells", "heavy manacles", "moldy straw beds", "ripped uniforms", "engraved prisoner marks","decaying wooden doors", "stone restraints", "barred windows", "skeletal remains", "cracked slates",
        "broken keys", "pools of murky water", "chains nailed to the wall", "scratched tally marks","rusted locks", "dented helmets", "faded banners", "wooden stockades", "barrels of fetid water",
        "incomplete shackles", "nail-scratched walls", "forgotten notes", "mossy steps", "loose bricks","dried blood", "crumbling steps", "tattered cloaks", "old food trays", "latchless cell doors",
        "severed manacles", "stone wash basins", "dust-covered bones", "name carvings", "iron cuffs"],
        
        "sounds": ["rattling chains", "a ghostly moan", "dripping water", "beating hearts", "crying moans", "harmonica tunes", "crackling torches", "scraping metal", "guillotine thuds", "screams of pain", "gusts of wind through cracks", "distant, ghostly moans", "chanting in an unknown language", "phantom breathing", 
        "whispers with no source", "rattling bones", "hissing snakes", "the sounds of skittering across the walls", "heavy breathing", "metal doors opening", "rusty hinges", "axes being sharpened", "grinding cogs and levers", "ropes tightening", "an unhumane screech", "snapping bones", "scratching", "bodies dropping", "chittering insects", 
        "beds creaking", "clanging against cell doors","incessant laughing", "scratching", "many bugs crawling", "faint breathing", "bones dragging along the floor", "bodies dragging on the floor", "thousands of tiny feet skittering", "bats flapping", "insects hissing", "stones shifting", "cries for help", "thunder clacking", 
        "wet coughing", "blood dripping", "flesh stretching", "bones grinding against each other", "door bolts sliding", "locks opening", "cell doors opening", "metal scratching the walls", "lullabies in a dead language", "someone crying softly", "an axe swinging", "someone telling you to run", "desperate prayers", "chains dragging", 
        "chalk scraping surfaces", "counting", "gaurds yelling","muffled cries", "distant footsteps", "keys jingling in the dark","a metallic clank", "doors creaking open", "muffled coughing", "the shuffling of something unseen","moaning from another cell", "a guard’s boot echoing", "the jingle of shackles", "wind whistling through cracks",
        "nails scraping stone", "a faint sob", "coughing from deep within", "stone grinding", "bars being tested","a whisper of despair", "footsteps above", "a rusty hinge swinging", "chains dragging across the floor","heavy breathing", "a harsh command yelled in the distance", "the slosh of water", "quiet weeping","the clink of dropped keys", 
        "a sudden silence", "chains tightening", "a sigh that isn't yours","gravel crunching underfoot", "something shifting in the shadows", "an echo of past screams","rats squeaking through the walls", "metal scraping on metal", "a haunting wail", "the thud of a closing cell" ],
        
        "actions": ["making you feel trapped", "echoing your footsteps eerily", "inviting you in", "sending chills down your spine", "filling the air with unease", "making you feel watched",
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
        "giving the sense that something is hiding nearby", "making you feel lost in time"]
    },
    
    "Treasure Room": {
        "adjectives": ["golden", "sparkling", "shimmering", "opulent", "bright", "iridescent","gold plated", "immeasurable", "priceless", "glittering", "shimmering", "gilded", "radiant", "sparkling", "dazzling", "gleaming", "bejeweled", "lustrous", "chromatic", "flashing", "brilliant", "lavish","luxurious", "exotic", "rare", "majestic", "regal", "bountiful", "ornate", "glorious", "unfathomable", "untouched", "forbidden",
        "enchanted", "cursed", "blessed", "legendary", "forbidden", "ethereal", "mythic", "ancient", "forgotten", "dust-covered", "timeworn", "polished", "blinding", "glimmering", "reflective", "resplendent", "divine", "sacred", "celestial", "noble", "lengendary", "timeless", "buried", "antiquated", "inscribed", "hexed", "tempting", "sinister", "alluring", "untouchable", "jeweled", "beautiful", "magnificent",
        "abundant", "buried","concealed","coveted","wealthy","valuable","twinkling", "grand","heavenly","fabulous", "wonderful", "infinite", "artistic", "mighty", "mysterious", "incomparable", "hidden","glistening","breathtaking","unforgettable", "exquisite","silver", "emerald", "diamond", "indescribable"],
        
        "features": ["chests of gold", "gem-encrusted goblets", "piles of treasure", "heaps of glittering coins", "overflowing jewel boxes", "crowns studded with rubbies", "rings stacked on bones", "chalices dripping with emeralds", "scepters of silver and sapphire", "trinkets scattered across velvet","ancient coins with faded faces", "treasures from lost empires", "silver coins spilling from cracked jars", "foreign currencies unknown to this land", 
        "bloodstained copper tokens", "platinum bars sealed in wax", "bend coins with dragon sigils", "bars of gold", "ornate tiaras once worn by queens", "cystal orbs on gold stands", "stained-glass pendants that shimmer in the dark", "tomes bound in golden leather", "bottles of starlight", "wands with jewel hilts", "golden scrolls wrapped in velvet ribbons", "singing coins that chime when touched", "stone urns brimming with opals", "dragon teeth dipped in gold", 
        "gilded skulls with jeweled eyes", "idol statues worshipped by long-lost cults", "war medals pinned to velvet cloaks", "locked chest glowing faintly", "crystal jars filled with swirling mist", "vials of powdered gemstones","leather pouches filled with gold", "silk pouches filled with pearls", "crystal music boxes that play enchanting lullabies", "thrones carved from gold and bone", "armor suits crusted in diamonds", "bones wearing royal jewelry", "roses made of ruby", 
        "silver harps strung with spider silk", "loose sapphires scattered like pebbles", "mounds of blood-red rubies", "gemstones arranged in elaborated patterns", "amethyst clusters glowing faintly", "black opals shifting colors in the light", "cracked diamonds that hum softly", "star-shaped gems glowing with internal fire", "pearls piled in silver bowls", "golden mirrors that reflect different eras", "golden mirrors that grant wishes", "ornate keys resting on silk pillows", 
        "tapestries threaded with gold leaf", "statues carved from starlight marble", "enchanted hour glasses filled iwth glowing sand", "spellbound lockets whispering secrets", "silver frames holding moving portraits", "worn rings inscribed with forgotten names", "ceremonial staffs taller than man", "ancient relics wrapped in silk linen", "bottomless velvet pouches", "treasure chest with vines wrapped around it", "crystal orbs that show different versions of yourself", 
        "crowns emitting faint whispers", "severed hands holding unknown gems", "gems that pulse like a heartbeat", "scrolls enscribed with gold ink", "potions that turn things into gold", "instruments carved from unicorn bone", "perfumes that increase your charm when worn", "robes woven with actual stars", "cloth that twinkle like stars", "gemstones that show you the future", "gauntlets with mysterious liquids", "shining instruments that play on their own", "stars stored in jars of china", 
        "potions of good fortune", "rainbow pots overgrown with four leaf clovers", "velvet pouches with unlimited space", "double rainbows", "monkey paws", "mosaic genie lamps", "sarcophagi storing vast treasures", "pirate ships filled with treasure", "rabbit feet"],
        
        "sounds": ["coins clinking", "a soft hum of magic", "echoes of wealth", "a faint chime from unseen jewelry", "whispers of greedy wishes", "the creak of a golden chest lid", "rattling gems in glass jars", "a slow metallic slide of treasure shifting", "muffled footsteps on velvet carpet", "the sparkle of magic-infused gold", "distant laughter echoing through the vault", "a harp string plucked by no hand", "tinkling chains draped over ancient crowns", "clattering gems pouring from a broken urn", 
        "soft rustling of silk wrapping artifacts", "a heartbeat-like thrum pulsing from a cursed relic", "sighs of forgotten kings trapped in amulets", "the jingle of enchanted coin pouches", "faint bells tolling with no source", "a swirl of arcane whispers tied to priceless scrolls","golden scales scraping stone", "whispers of ancient curses", "a lock clicking open by itself", "fluttering paper from scrolls rearranging", "magical murmurs within gem clusters", "glass cracking under weight of platinum", 
        "a distant trumpet muffled by time", "the pop of arcane wards", "pages flipping in closed books", "a low growl from inside a chest", "muffled sobbing from a jeweled mask", "clinking bottles of glowing liquid", "tiny footsteps across coin piles", "the hiss of magic suppressing a trap", "echoes of battle cries caught in relics", "a key turning from inside the lock", "the rush of wind inside a sealed vault", "faint crackles from enchanted statues", "a melody trapped inside a gemstone", "a lingering echo of someone saying 'mine'",
        "a single coin spinning endlessly", "velvet rustling under shifting artifacts", "distant chants echoing from jeweled relics", "gentle ringing from enchanted crowns", "a chest breathing slowly", "jewels humming in energy", "glass domes pulsing with magical energy", "a gold chain sliding off a pedestal", "the creak of an overburdened treasure shelf", "a mirror echoing soft voices", "the soft whoosh of arcane runes activating", "dripping molten gold in a far corner", "crystals harmonizing in faint tones", 
        "the squeak of a velvet-lined drawer opening", "a harp playing one sorrowful note", "coins falling from nowhere", "a magical lock snapping shut", "the flap of silk drapes stirring with no wind", "a gemstone laughing faintly", "a whisper saying 'yours...' and fading","scrolls crackling with dormant magic", "a gold-plated music box winding itself", "runes buzzing just beneath perception", "phantom footsteps pacing near the treasure", "dust shifting as if disturbed", "a chorus of faint bells in the distance", 
        "treasure softly murmuring to itself", "a ghostly voice reciting forgotten names", "muffled clinks from under a cloak", "a deep hum from a sealed chest", "the sound of pages turning themselves", "faint wind despite no exit", "shimmering tones vibrating through the air", "a low growl from behind the gold pile", "the groan of ancient wood giving way", "the ding of an invisible cash register", "fingers tapping on gemstone glass", "a warm chuckle from nowhere", "a voice counting coin after coin", "an echo that repeats only your last word",
        "hardy laughs from ancient kings", "soft snores from a dragon"],
        
        "actions": ["enticing you closer", "blinding you with brilliance", "inviting you in", "sending chills down your spine", "filling the air with unease", "making you feel watched",
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
        "giving the sense that something is hiding nearby", "making you feel lost in time"],
    },
    "Trap Room": {
    "adjectives": ["trap-rigged", "decaying", "illusionary", "haunted", "tampered", "rusted", "maze-like", "timeworn", "volatile", "crumbled", "dust-choked", "misleading", "spike-laced", "foul-smelling", "mechanical", "trap-infested", "netted", "gas-leaking", 
    "slippery", "ancient", "chilling", "malicious", "whispering", "eerie", "riddle-bound", "hazardous","brittle", "hollow-sounding", "unreliable", "spring-loaded", "warped", "lever-filled", "threatening", "dim", "smoke-filled", "inconspicuous", "high-risk", 
    "misaligned", "sound-sensitive", "poison-laced", "stealthy", "dim", "shifting", "overcomplicated", "tricky", "bloodstained", "suspicious", "grimy", "cluttered", "echoeing", "suffocating","pitch black","entrapping", "deceitful", "treacherous", "menacing",
    "smoky", "unstable", "brittle", "jagged", "deceptive", "cursed", "trembling", "lopsided", "enigmatic", "electrified", "unsettling", "ticking", " veiled", "forbidden", "murky", "deadly", "luring", "eerie", "damp", "foreboding", "buzzing", "creaky", "fetid", "scorched", 
    "unlit", "confusing", "malformed"],
    
    "features": ["pressure plates", "tripwires", "spike pits", "swinging axes", "falling rocks", "laser beams", "levitating sharks", "piranha tanks", "hell hounds", "glue traps", "spaces ridden with animal traps", "spike pits",
    "collapsing floors", "hidden crossbows", "dart holes in the walls", "illusory pathways", "slippery tiles", "snake pits","blades embedded in the walls", "scorch marks on the floor", "suspicious tiles", "glyphs that pulse faintly","land mines",
    "tilting platforms", "sizzling acid pools", "sudden drop-offs", "magical sigils etched into the stone","invisible trip wires", "faint grooves", "statues with open mouths", "ceiling holes with no purpose", "falling rocks", "swinging logs", "explosive runes",
    "skeletons near doorways", "chained levers", "moving walls", "hidden buttons", "sawdust-covered floors","cage mechanisms", "tension coils beneath panels", "rusted springs poking out", "narrow crawlspaces", "poison gas vent", "blinding flashes", "net snare", 
    "runic warnings", "ominous carvings", "metal grates with no clear use", "small mirrors angled strangely","loose stones", "charred bones", "incomplete puzzle locks", "crushed helmets", "acid sprays", "constricting vines", "caltrops", "blowdart traps",
    "gas explosives", "constricting vines", "toxic fumes", "acid puddles", "bloody cages with nothing in them", "taxidermied creatures", "shot guns"],
    
    "sounds": ["clicking mechanisms", "creaking floors", "a sudden snap", "chains rattling above", "stones grinding underfoot", "many alarm clocks going off", "air horns", "ear bursting sirens",
    "a faint ticking", "gears turning slowly", "metal scraping on stone", "arrows whizzing past", "a trap resetting itself", "chainsaws starting", "trumpets crescendoing the longer you remain", "orchestra music playing dramatically",
    "distant crashing", "spinning cogs", "wood splintering", "grinding walls", "a pressure plate engaging", "glass smashing", "serpents slithering", "metal clanks", "racheting mechanisms", "whirring blades spinning to life",
    "a sharp metallic clang", "whirring blades", "muffled thuds from deep below", "darts firing from hidden holes", "traps triggering", "levers moving", "Jumanji music", "a rumbling growl from beneath the floorboards", "stones cracking",
    "grating pulleys moving unseen weights", "an ominous hiss", "panels shifting beneath your feet", "whispers that stop abruptly", "rocks falling", "water rising", "soft giggles that fade into static"
    "stones falling in the distance", "rope snapping", "ceiling tiles shifting", "traps resetting with a dull thud", "the floor rumbling", "alarms going off", "eerie hums from magical traps",
    "a sudden whoosh of air", "a net springing into place", "levers groaning into motion", "a faint magical pulse", "the groans of the undead","floor tiles sinking slightly", "runic sparks fizzling", "something heavy being dragged", 
    "clicks in rapid succession", "mischieveous howling","dust cascading from the ceiling", "a metallic chime with no source", "a sharp hissing of gas", "the whine of springs under tension", "rapid explosions", "gun fire"],
    
    "actions": ["keeping you on edge", "daring you to move", "inviting you in", "sending chills down your spine", "filling the air with unease", "making you feel watched",
    "urging you to move forward", "making the air feel heavy", "bringing a sense of nostalgia", "whispering unintelligible secrets",
    "creating an eerie tension", "pulling you toward the center", "giving an overwhelming feeling of dread", "making the walls seem alive",
    "distorting the space around you", "tempting you to explore", "pushing you back with an unseen force", "draining the warmth from your body",
    "making your skin tingle", "causing your vision to blur", "making it hard to breathe", "surrounding you with an unseen presence",
    "making your heartbeat race", "clouding your mind", "provoking an unexplained sorrow", "making the floor feel unstable",
    "enveloping you in a strange warmth", "mimicking voices you recognize", "making the air hum with energy", "repeating your footsteps behind you",
    "causing the light to flicker", "making shadows move on their own", "giving off a magnetic pull", "causing a strange ringing in your ears",
    "making time seem to slow down", "erasing the sound of your footsteps", "intensifying your fear", "pressing a weight upon your shoulders",
    "giving you the sensation of falling", "sending a tingling sensation through your body", "making it feel like you are being followed",
    "stirring up hurtful memories", "causing an inexplicable chill", "making you feel both welcomed and threatened", "casting flickering shadows on the walls",
    "leaving a metallic taste in your mouth", "causing your surroundings to vibrate slightly", "creating a forceful energy in the room",
    "tricking your mind into hearing distant voices", "making the ground feel uneven",
    "giving the sense that something is hiding nearby", "making you feel lost in time"]
    },
    
    "Monster Lair": {
    "adjectives": ["smelly", "bloodstained", "menacing", "gory", "shadowy", "vile", "stench-filled", "beastly", "savage", "feral","chaotic", "repugnant", "damp", "noisy", "haunted",
    "torn", "grimy", "brutal", "filthy", "sulfuric","unnerving", "threatening", "claustrophobic", "battered", "scarred", "unholy", "stench-ridden", "wild", "putrid", "inhospitable",
    "foul", "darkened", "abominable", "infested", "ominous","trembling", "aggressive", "inhuman", "slime-coated", "burnt","gnawed", "nestlike", "despoiled", "reeking", "harrowing",
    "predatory", "beast-marked", "crimson-drenched", "unnatural", "choking", "grotesque", "bloodthirsty", "dingy", "repulsive", "elusive", "mythical", "terrifying", "hideous", "monstrous", 
    "evil", "scaly","haunting", "macabre", "otherwordly", "hostile"],
    
    "features": ["bones", "claw marks", "torn fabrics", "blood smears on the walls", "cracked armor", "bite marks", "shedded baskilisk skins", "impish fairies", "chupacabra fangs", "possessed bears", "cursed dolls", "enchanted jackalope antlers","portraits of mythical creatures",
    "half-eaten corpses", "gnawed skulls", "thick claw furrows", "rotting carcasses", "bloodied chains", "broken cages", "alters made from bone and skulls", "large venomous millipedes", "lying goblins", "soul-sucking demons", "emraged werewolves"
    "broken weapons", "deep scratches on stone", "foul bedding", "webbed corners", "matted fur piles", "offerings displayed on a shrine", "rats scattering", "millipedes crawling everywhere", "hungry cannibals", "deceptive skin-walkers",
    "discarded bones", "fresh droppings", "pools of ichor", "displaced rubble", "crushed furniture", "trails of large footprints", "humans in spider cocoons", "radioactive bats", "muscular ogres", "massive gargoyles", "zombie pirates", "weaping ghouls",
    "massive footprints", "gnawed wood beams", "dark stains on the floor", "insect husks", "dried slime trails", "ghosts of past victims", "beds made from bones and hair", "blind angry cyclops", "banshees trapped in mirrors", "frozen dullahans", "blind witches",
    "makeshift nests", "crude markings on walls", "empty eye sockets staring back", "fangs embedded in wood", "evil frost elves", "monsters with no faces", "weeping angels", "famished bengal tigers", "cerberus markings", "dragons armed with diamond scales",
    "moss-covered bones", "dried bloodstains", "mutilated prey", "decayed pelts", "spiked nests", "venom-spitting plants", "hell hounds", "carnivorous fly traps", "hypnotic creatures", "herds of minotaurs", "Kraken tentacles", "ceiling tall snapping turtles",
    "webbing strung across doorways", "barrels of discarded meat", "old battle banners", "gory organs","cages ripped open", "walls scorched by claws", "piles of flesh", "shattered bones and shattered hope", "dismembered limbs", "intelligent martians", 
    "pirate ghost"],
    
    "sounds": ["growling", "heavy breathing", "a low snarl", "bones crunching underfoot", "deep guttural roars", "dragons snoring", "banshee screeches", "witches cackling",
    "claws scraping stone", "incoherent beastly murmurs", "wet chewing noises", "distant howls", "a low, menacing hiss", "werewolves howling", "mouths gnawing on meet", "bones being chewed on"
    "snarling echoes", "flesh tearing", "deep breathing in the dark", "blood-curdling screeching", "the flapping of leathery wings", "hounds barking", "bats screeching", "eerie wails", "strange laughing inside your head", "stomach growls",
    "dripping blood", "the gnashing of teeth", "a rattling growl", "gurgling snarls", "throaty bellows", "siren lullabies", "jaws snapping like cracked wood", "deep, earth-shaking growls", "sniffing getting closer to you", "hooves stampeding"
    "a sudden animalistic shriek", "rapid panting", "labored breathing", "growls in stereo", "a roar shaking the walls", "sharp peircing roars", "echoing laughter from nowhere and everywhere", "something mimicking a human voice", "viking horns being blown",
    "snapping jaws", "predator calls", "clawed footsteps circling you", "a tail thumping the floor", "raspy exhalation", "insects buzzing", "slurping gurgles", "stomach growlings", "someone breathing your ears", "chattering teeth", "chains being dragged against the floor",
    "muffled bestial laughter", "a beast pacing behind the walls", "dirt and bones being displaced", "cave echos repeating snarls", "mirrors shattering", "cages opening", "hyenas laughing", "earth rumbling roars", "muffled screams",
    "a bone cracking pop", "wet snorts", "tension-heavy silence between movements", "insectoid clicking", "predatory purring", "desonate bells", "rapid explosions", "static crackling", "crunching bones", "instruments playing out of tune",
    "whispers saying, 'help me'", "distant screams warning you to run", "clubs banging on the ground", "impish laughter", "thumping noises", "banging against cages", "flesh corroding from acid", "pained sobbing", "prayers spoken in an archaic language"],
    
    "actions": ["sending chills down your spine", "warning you to leave", "inviting you in", "sending chills down your spine", "filling the air with unease", "making you feel watched",
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
    "tricking your mind into hearing distant voices", "making the ground feel uneven", 
    "giving the sense that something is hiding nearby", "making you feel lost in time"]
    },
    
    "Secret Room": {
    "adjectives": ["hidden", "forgotten", "quiet", "mysterious", "undisturbed", "concealed", "sealed",
    "dusty", "dim", "ancient", "hollow", "unmarked", "lost", "abandoned", "crumbling", 
    "shrouded", "neglected", "silent", "secretive", "veiled", "shadowed", "invisible",
    "unseen", "enchanted", "camouflaged", "unused", "cloaked", "relic-filled", "unreachable",
    "unfamiliar", "buried", "cobwebbed", "withered", "softly lit", "trap-ridden", "desolate","sealed-off", "echoing", "hidden-away", "guarded", "forgotten-by-time", "untouched", 
    "haunted", "dormant", "timeless", "vaulted", "lightless", "creaking", "enclosed", "unlit", "narrow", "claustrophobic", "sacred", "overgrown", "hushed", "sealed-off", 
    "outdated", "undisturbed", "low-ceilinged", "hidden-away", "unstable", "enigma-wrapped", "trap ridden", "obscure", "rarely-seen", "dimly concealed","unnaturally still", "underground", 
    "tunnel-fed", "flicker-lit", "labyrinthine", "partially collapsed", "protected", "unwelcome", "secluded", "burrowed", "spellbound",
    "cluttered", "faintly glowing", "barely accessible", "unrecorded", "unreadable"],
    
    "features": ["dusty furniture", "hidden bookshelves", "worn paintings",  "oak bookshelves", "dust-covered artifacts", "faded tapestries", "concealed levers", "secret passageways", "various art supplies",
    "loose floor tiles", "mysterious sigils", "ornate lockboxes", "ancient scrolls", "trapdoor handles", "pheonix ashes", "four leaf clovers", "chest filled with cursed items", "portraits of historical figures",
    "invisible writing", "glowing runes", "creaking wall panels", "worn carpets", "old paintings with shifting eyes", "jars sealed with talisman", "chalices filled with either poisons or remedies", "portraits of people whose eyes watch you"
    "shattered glass domes", "books bound in unfamiliar leather", "silent guardian statues", "dim crystal sconces", "lucky dice", "origami figurines", "hypnotic shrooms", "pincodes to unknown locks", "cookies saying, 'eat me'", "vials saying,'drink me'"
    "a cracked mirror reflecting nothing", "forgotten tomes", "creepy dolls", "unused ink quills", "shrouded furniture", "orbs filled with electricity", "hourglasses that reverse time", "ruby slippers", "rabbit holes", "singing flowers", "gentle giants",  
    "burned-out candles", "unlabeled potions", "a journal with ripped pages", "timeworn relics", "sealed urns", "conches that whispers mermaid secrets", "taxidermied animals that are extinct", "stone statues that look like chess pieces", "broken pocket watches",
    "hollow bricks", "ancient keys", "phantom footprints in the dust", "clocks that tick backward", "suspended lanterns", "papers lined with morse code", "decryption books", "sleeping familiars", "ancient technology", "futuristic technology", "winding watches that manipulate time",
    "unmarked drawers", "faded maps", "a hidden trapdoor under a rug", "runes that glow when touched", "quiet ticking mechanisms", "false-bottom drawers", "etched stone tablets", "half-burned incantation scrolls", "books that hum softly", "sealed envelopes",
    "mirrors with no reflection", "dusty glass bottles with sealed wax", "ornate puzzle boxes", "layers of cobwebs","loose bricks hiding switches", "books that open to hidden compartments", "unfinished rituals drawn in chalk", "ships in bottles", "diagrams of flying machines", "parachute backpacks",
    "ticking mechanical devices", "tiny peepholes in the walls", "journals with coded text", "layers of old wax seals","jars of faded ink", "unusual wall carvings", "portraits with shifting eyes", "floorboards that creak in sequence", "record players",
    "symbols that react to moonlight", "candleholders that twist silently", "inlaid gemstones glowing faintly","tomes bound in scales", "invisible ink revealed under heat", "hidden safes behind wall panels", "phonographs playing ethereal music",
    "paintings that whisper when touched", "locks with unknown symbols", "glowing dust in floor cracks","a box of mismatched keys", "a pile of discarded disguises", "half-carved golem statues", "bottled shadows", "music boxes playing a nostalgic tunes",
    "a shelf labeled 'Do Not Read'", "a cracked crystal ball", "an hourglass running backward", "shelves full of dust but no footprints","a bell that rings without being touched", "a single eye peering from a knothole", "floor tiles that light up when stepped on"],
    
    "sounds": ["creaking wood", "hush of wind", "nothing at all",  "a faint rustle behind the walls", "creaking floorboards", "a whisper that fades too quickly", "dripping from somewhere unseen", "electric buzzing",
    "pages flipping on their own", "old lock clicking shut", "breath that isn't yours", "the shuffle of parchment", "muffled footsteps from above","a sudden hush", "a tick-tock from a hidden clock", "dust falling in silence", "an eerie chord from nowhere", "soft tapping on stone","whispers in a language you don't understand", 
    "a gentle sigh", "a drawer opening slowly", "the scratch of quill on parchment", "rattling hinges","the flicker of a flame with no wind", "a thump beneath the floorboards", "low mechanical winding", "a breeze with no source", "a dull heartbeat-like pulse",
    "faint echoes of footsteps long gone", "a metallic chime", "the hiss of vapor escaping", "distant laughter", "the turn of a hidden gear", "childlike laughter","a hum that builds then disappears","faint chanting", "the flutter of invisible wings", "the creak of an ancient shelf", "a deep breath from the shadows", "orchestra music"
    "the clink of a glass vial", "pages turning rapidly", "a bell that rings without cause", "the clatter of bone on stone", "scratching from behind the walls", "a lock clicking open on its own", "phantom footsteps circling the room", "a quill scratching on invisible parchment",
    "a mirror humming faintly", "an old tune whistled from nowhere", "a sigh that echoes twice", "the snap of a hidden latch","turning pages fluttering", "brief static crackle", "soft wind chimes", "floorboards groaning under invisible weight",
    "glass tapping gently", "quiet grinding noise", "runes vibrating in low frequencies", "a cabinet slamming shut", "invisible furniture falling", "soft snoring", "corny jokes", "knock knock jokes", "windchimes moving without a breeze",
    "the wet squish of something unseen", "whispers returning your words", "clockwork ticking accelerating", "a quiet knock that isn’t repeated", 
    "a distant voice calling your name", "the rustle of a curtain that isn’t there", "stone scraping softly", "the flick of a switch being flipped",
    "a sudden whoosh of displaced air", "the buzz of arcane energy", "a gentle laugh stopping abruptly", "books thumping onto a shelf", "a glass shattering behind you",
    "a metallic rasping", "the dragging of cloth on stone", "a gasp from under the floorboards", "faint breathing in sync with your own",
    "muffled arguing voices", "the hiss of a sealing door", "the delicate jingle of enchanted wind chimes",
    "a deep harmonic tone that fades", "shuffling footsteps that pause when you stop", "a harp string being plucked",
    "a door slowly creaking closed", "the distinct snap of a trap resetting"],
    
    "actions": ["whispering secrets to you", "inviting you to explore", "inviting you in", "sending chills down your spine", "filling the air with unease", "making you feel watched",
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
    "giving the sense that something is hiding nearby", "making you feel lost in time"]
    },
    
    "Armory": {
    "adjectives": ["metallic", "cluttered", "rusty", "gleaming", "war-torn", "dusty", "well-stocked", "organized", "ancient", "battle-worn","reinforced", "dimly-lit", "secure", "steel-lined", "echoing", "narrow", "polished", "weathered", "armored", "sharp-edged",
    "smoke-stained", "functional", "ornate", "brutal-looking", "rigid", "imposing", "blackened", "blood-streaked", "shield-lined", "low-ceilinged","cramped", "spartan", "efficient", "tactical", "hard-edged", "decorated", "cool", "forged", "weighty", "barred",
    "reinforced", "militaristic", "grimy", "fortified", "charred", "heavily-locked", "stone-walled", "drafty", "tarnished", "smoke-filled","ironclad", "well-worn", "tool-lined", "creaking", "trophy-covered", "chiseled", "flint-scarred", "pitted", "clanging", "locked",
    "tight-spaced", "shadow-filled", "weapon-racked", "oak-framed", "steel-forged", "strategic", "ashen", "torch-lit", "reinforced", "gear-strewn", "sword-scarred", "spear-lined", "musty", "leather-scented", "cold", "narrow", "gloomy", "orderly", "impenetrable", "aged",
    "echo-filled", "low-lit", "oak-paneled", "weapon-lined", "cold-forged", "brass-trimmed", "rank-smelling", "disciplinary", "battle-ready", "timeworn","cluttered", "warped", "blade-heavy", "dangerous", "intimidating", "functional", "rigged", "scarred", "heavily-guarded", "rack-filled",
    "uniform", "discipline-focused", "shadowed", "inlaid", "dented", "hulking", "encased", "blacksmith-warmed", "gauntlet-strewn", "obsidian-lined","steel-framed", "iron-floored", "sentry-watched", "well-oiled", "brimmed", "task-oriented", "efficiency-shaped", "measured", "hushed", "patrolled"],
        
    "features": ["racks of weapons", "shields", "headless horsemen in armor", "rusted armor", "chains draped over hooks", "sparring weapons set in orderly rows", "locked chests of explosives", "battered helmets on hooks", "wooden shields", "weightless shields", "diamond shields", "photos of knights long forgotten",
    "practice swords dulled from use", "shield emblems denoting past factions", "netting used for entrapment", "heavy gloves on a bench","anvils stained with soot", "claymore racks near the entrance", "sword polish cloths on tables", "military-grade armor sets on mannequins", "last will and testiment of dead soldiers",
    "iron bars for weapon reinforcement", "combat manuals laid open mid-page", "bucklers leaned beside the door", "hanging flails swaying slightly","stacked crates labeled with runes", "daggers embedded into a practice post", "mounted trophies from battles", "replacement straps and rivets sorted in bins", 
    "arrowheads arranged by size", "visors propped on wooden pegs", "archery targets shredded from impact", "sharpening tools left half-used", "trophy cases filled with enchanted relics", "racks of spiked maces", "glass cases with ancient relics", "walls scorched from past enchantments", "storage crates of chainmail",
    "weapon blueprints pinned to corkboards", "longbows strung and ready", "rows of enchanted quivers", "chalk diagrams drawn on the floor","runed stones embedded into weapon handles", "tower shields propped like barriers", "halberd heads glinting in dim torchlight", "strategy manuals", "beaten down practice dummies", "fencing swords",
    "weapon tags denoting cursed status", "scabbards hanging by the doorway", "metal scraps from failed forges", "a forge pit no longer burning","notes on combat stances tacked to the wall", "weapon parts disassembled for repair", "a ledger of issued weapons", "charcoal sketches of monster anatomy", "flaming swords", "crossbows with infinite arrows",
    "training staves worn smooth with use", "a broken magic weapon in a locked box", "healing salves stored in a corner chest", "protective gear stacked in piles", "gloves marked with arcane symbols", "wall slots for elemental-infused blades", "armor suits made of diamond"],
    
    "sounds": ["clinking metal", "scraping blades", "a distant clang",  "metal clashing against metal", "the scrape of a blade on a whetstone", "a loud clang of dropped armor", "soft creaking of leather straps",
    "chains rattling in the corner", "echoes of distant combat drills", "a warhorn call muffled through stone", "faint hammering from a forge","anvil strikes ringing in rhythm", "weapons clinking as racks shift", "a quiet metallic hum from enchanted blades", "rust flakes falling like soft rain",
    "grunts from a nearby sparring session", "a sword unsheathing with a hiss", "a helmet clanking onto stone", "bootsteps pacing across stone tiles","shields brushing together with a dull thump", "locks clicking on weapon chests", "bows creaking as strings are drawn", "whispers of old battle chants",
    "the snap of a crossbow being cocked", "crackling fire from a nearby forge", "a sword tip dragging across the floor", "metal buckles being fastened","a quiet hiss of steam escaping a pipe", "wooden practice dummies being struck", "the rattle of chainmail being folded", "murmurs of strategy whispered nearby",
    "dull thuds of sparring impacts", "a sudden slam of a heavy chest closing", "the flick of a sharpening stone on steel", "a distant command barked by a drillmaster","armor plates clinking as someone suits up", "soft whirring from magical mechanisms", "a banner rustling in a draft", "hinges squealing on a weapon locker",
    "bellows blowing from a forge station", "arrows sliding into quivers", "a broken blade dropping to the floor", "the echo of your footsteps in the vaulted hall", "swords clashing against chain mail", "gruntings from soldiers", "knights on galloping horses", ],
    
    "actions": ["readying for combat", "echoing ancient battles", "inviting you in", "sending chills down your spine", "filling the air with unease", "making you feel watched",
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
        "giving the sense that something is hiding nearby", "making you feel lost in time"]
    },
    "Library": {
    "adjectives": ["quiet", "dusty", "book-lined", "silent", "intellectual", "dusty", "ancient", "quiet", "dimly-lit", "book-lined", "shadowy", "forgotten", "cluttered", "candle-lit", "mossy","mysterious", "timeworn", "crumbling", "enchanted", "silent", "ink-stained", 
    "gilded", "wood-paneled", "towering", "musty","narrow", "scroll-filled", "cozy", "shelf-packed", "gloomy", "cobwebbed", "leather-bound", "orderly", "scholarly", "forbidden", "whisper-filled", "runed", "deep", "echoing", "arched", "ceiling-high", "pleasant", "quiet", "peaceful", 
    "serene", "dusty", "old", "ancient", "forgotten", "silent", "mysterious", "tall", "ornate", "secret", "hidden", "arcane", "dim", "gloomy", "majestic", "cluttered", "wise","elegant",
    "warm", "cold", "lonely", "empty", "vast", "secretive", "abandoned", "echoing", "private","sacred", "shrouded", "vaulted", "quiet", "timeless", "intact", "sealed", "chilly", "shimmering", "reverent", "weathered", "crumbling", "burned", "smoky", "enchanted", "sacred", 
    "cold", "quiet", "abandoned","grand", "massive", "faded", "intact", "ruined", "peaceful", "dim", "infinite", "timeless", "ornate","endless", "sheltered", "majestic", "lost", "haunted", "gloomy", "relic-filled", "hollow", "enchanted", "sealed",
    "private", "moss-covered", "dust-coated", "tranquil", "noble", "secretive", "silent", "curious", "unknown", "deep"],
    
    "features": ["scrolls", "old tomes","magic infused chess set", "high shelves", "towering bookshelves", "scroll racks", "rolling ladders", "glowing tomes", "cobweb-covered shelves","ancient manuscripts", "dusty scrolls", "cracked reading desks", "magical orbs", "ink-stained desks","spellbound books", "charcoal drawings",
    "flickering candlelight", "arched wooden beams", "ghostly librarians", "runes etched in the walls","whispering pages", "levitating books", "bookshelves that shift when touched", "piles of unread scrolls", "preserved skeletons of scholars", "portraits of classic literary characters", "sliding ladders", "typewriters that predict the future",
    "floating quills", "melted wax puddles", "runic diagrams", "frayed parchment maps", "leather-bound grimoires","scrying mirrors", "book-sized cages", "pages suspended mid-air", "secret compartments", "books that float around the room", "portraits of Dr.Jekyll and Mr.Hyde", "pheonixes in bird cages", "bottles of invisible ink",
    "sealed cabinets", "forgotten corners", "floor mosaics of arcane symbols", "transparent books", "shelves that rearrange themselves", "bookcases carved with sigils", "tables stacked with dusty notes", "quills scratching on their own", "mystical reading lanterns", "books that whisper when opened", "carrier pigeons",
    "scrolls sealed with wax", "ink bottles tipped over", "arcane blueprints spread across tables", "curtained alcoves", "stairs that spiral endlessly upward", "hidden levers in books", "locked tomes glowing faintly", "old chairs with clawed feet", "magical seals on the floor", "owls sleeping on a perch", "stationaries",
    "floating index cards","displaced timepieces ticking backwards", "unmoving spectral patrons", "books vibrating with magical energy", "crates of forbidden literature", "writing that shifts languages","dust clouds that shimmer with enchantment", "secret doors behind shelves", "moonlight cutting through stained glass", 
    "rooftop observatory domes", "piles of ash from burned scrolls","clocks stuck at midnight", "warding glyphs painted on ceiling beams", "magically chilled storage cabinets", "books humming with energy", "rotating shelves activated by chanting", "locked books with a large single demon eye on the cover",
    "dust-covered chandeliers", "celestial charts", "ancient catalogs", "language translation tables", "dim crystal sconces", "ceiling lenghthed columns", "overgrown plants", "tall singing flowers", "baskets filled with magical cloaks", "life-sized chess set "],
    
    "sounds": ["rustling pages", "quill scratches", "book bindings creaking", "soft footsteps on stone", "quills scratching parchment", "a book slamming shut in the distance", "gentle creaking of wooden shelves",
    "whispered voices with no source", "crackling from a candle flame", "faint magical humming", "pages flipping by themselves", "the hiss of old bindings","distant echo of chanting", "a sudden thud of falling books", "ink dripping onto paper", "muffled voices in unknown tongues", "the soft click of a lock turning",
    "glowing glyphs pulsing with sound", "a sigh carried on the wind", "an unseen bell chiming once", "the rustle of a passing ghost", "shelves sliding open slowly","a breathy exhale behind your ear", "a clock ticking impossibly loud", "arcane murmurs from the walls", "the sound of something scribbling in the dark", 
    "silence—too perfect to be natural",  "the flutter of unseen pages", "ghostly humming between aisles", "a chair scraping across stone", "faint murmurs repeating in a loop","the hum of arcane wards", "a feather quill writing on its own", "the faint crackle of static energy", "wind whistling through cracked glass",
    "a long exhale from the shadows", "faint piano notes echoing once", "the ticking of an invisible metronome", "a magical pop as a book vanishes","runes glowing with a deep bass tone", "pages flipping rapidly then stopping", "a soft 'shhh' from nowhere", "old hinges groaning open slowly",
    "the splash of ink in a well", "a low ambient vibration", "the gentle chime of a magical ward", "the sound of whispering in reverse","an echo of your own voice when you're silent", "something dragging across a distant floor", "the soft tearing of ancient paper", "a deep sigh behind the bookshelf", "a rhythmic tap like a librarian’s finger",
    "a book gently sliding out of place", "invisible footsteps pacing slowly", "a soft inhale from somewhere above", "the distant flap of wings","a scratching sound coming from inside the walls", "dripping from a ceiling leak you can’t see", "the low drone of magical energy", "owls hooting"
    "a harp note plucked by no one", "the shriek of bending metal far below", "a breathless whisper saying your name", "an index drawer slamming shut","a bell tolling once and then stopping", "wind stirring parchment with no breeze", "a slow heartbeat pounding from behind the shelves",
    "chalk writing on a blackboard by itself", "the shuffle of paper in a sealed drawer", "a whisper too close to your ear", "shelves shifting with a wooden groan","a gentle breeze carrying the smell of old books", "a thump from the second floor when you're alone", "the crack of a splintering chair leg",
    "a chorus of ghostly scholars debating", "muffled laughter in a language you don’t know", "the flapping of dozens of wings overhead","the final note of a song you've never heard"],
    
    "actions": ["filling you with curiosity", "guiding you to forgotten knowledge", "inviting you in", "sending chills down your spine", "filling the air with unease", "making you feel watched",
        "urging you to move forward", "making the air feel heavy", "bringing a sense of nostalgia", "whispering unintelligible secrets",
        "creating an eerie tension", "pulling you toward the center", "giving an overwhelming feeling of dread", "making the walls seem alive",
        "distorting the space around you", "tempting you to explore", "pushing you back with an unseen force", "draining the warmth from your body",
        "making your skin tingle", "causing your vision to blur", "making it hard to breathe", "surrounding you with an unseen presence",
        "making your heartsharpening sto race", "clouding your mind", "provoking an unexplained sorrow", "making the floor feel unstable",
        "enveloping you in a strange warmth", "mimicking voices you recognize", "making the air hum with energy", "repeating your footsteps behind you",
        "causing the light to flicker", "making shadows move on their own", "giving off a magnetic pull", "causing a strange ringing in your ears",
        "making time seem to slow down", "erasing the sound of your footsteps", "intensifying your fear", "pressing a weight upon your shoulders",
        "giving you the sensation of falling", "sending a tingling sensation through your body", "making it feel like you are being followed",
        "stirring up old memories", "causing an inexplicable chill", "making you feel both welcomed and threatened", "casting flickering shadows on the walls",
        "leaving a metallic taste in your mouth", "causing your surroundings to vibrate slightly", "creating a forceful energy in the room",
        "tricking your mind into hearing distant voices", "making the ground feel uneven", "making you feel strangely at peace",
        "giving the sense that something is hiding nearby", "making you feel lost in time"]
    },
    "Alchemy Lab": {
    "adjectives": ["chemical", "botanical","bubbling", "toxic", "glowing", "mysterious","bubbling", "chemical", "sulfurous", "pungent", "glowing",
    "flickering", "volatile", "mysterious", "toxic", "arcane", "crystalline", "fumy", "boiling", "glassy", "unsettling","cold",
    "chaotic", "odorous", "hazy", "murky", "viscous","sizzling", "explosive", "slippery", "corrosive", "luminescent", "pristine",
    "curious", "unstable", "stained", "steamy", "distilled","frosted", "oozing", "flask-lined", "herbal", "powdery", "cluttered", "sparkling", 
    "radioactive", "bubbling over",  "humid", "etheric", "unstable", "peculiar", "dense","shadow-filled", "metallic", "alchemical", "spark-charged",
    "saturated", "mossy", "glowing green", "pale blue", "scent-heavy", "glass-shattered", "low-lit", "reaction-prone", "transmuted",
    "chalk-dusted", "tincture-laden", "drip-stained", "elemental", "aged","well-worn", "fizzing", "infused", "sealed","wax-sealed", "chalk-ringed", "formula-covered", 
    "smokey", "thick with mystery", "cloudy", "acrid", "volatile", "intense", "seething","bitter", "sticky", "colorful", "viscous","noxious", "chaotic", "opaque", "sizzling", "sharp",
    "drowsy", "soaked", "burning", "electric","grimy", "unnatural", "loamy", "charged", "etheric","stale", "mellow", "tart", "misty", "golden","still", "gentle", "flickery", "unfamiliar",
    "liquidy", "watery", "pale", "crackling", "vibrating",  "frosty", "chalky", "rusty", "moist", "dense","bubbling", "dizzying", "vivid", "unsettling", "quiet",
    "vaporous", "tingling", "foamy", "acidic", "cooling","buzzing", "peculiar", "dull", "ancient", "clean","reactive", "turbid", "weary","ghostly", "serene", "prickly", "hazy", "solid",
    "molten", "floating", "restless", "humid", "twinkling", "mellow", "bright", "brackish", "elastic", "spiraling", "green", "fluorescent", "bioluminescent", "magical", "enchanting"],
        
    "features": ["glass beakers", "pots growing exotic plants" "strange herbs", "boiling flasks", "glass vials", "bubbling cauldrons", "potion bottles", "scrolls of transmutation", "burnt wooden tables",
    "glowing beakers", "mortar and pestle", "mysterious herbs", "stained journals", "runes etched in stone","boiling flasks", "hanging dried plants", "twisting coils", "dripping tubes", "cracked alchemical symbols",
    "corks and stoppers", "overflowing test tubes", "strange powders", "color shifting liquids", "glassy apparatus","floating crystals", "old recipe books", "flickering candles", "enchanted gloves", "charred notes",
    "twinkling orbs", "smoke-stained glass", "sealed jars filled with organs", "drained mana crystals", "copper piping","infusion basins", "weirdly labeled jars", "measuring rods", "singed ceiling tiles", "vapor funnels",
    "metal tongs", "alchemy ovens", "transmutation rings", "unusual residue", "blinking devices", "shattered vials", "fizzing concoctions", "tattered scrolls", "colorful fumes", "brittle crystal shards",
    "ticking glass instruments", "rows of labeled specimens", "cauldrons caked in residue", "arcane diagrams", "melting ingredients","shelves of strange skulls", "sealed crates", "smoky lanterns", "imbued gemstones", "dissected roots",
    "ancient alembics", "dripping alchemical symbols", "locked cupboards", "petrified mushrooms", "stirring rods","rattling bones in jars", "neatly arranged powders", "flasks emitting cold steam", "stacked clay tablets", "elixir-stained aprons",
    "spell-locked cabinets", "magnetized tools", "cooling plates", "ether-infused mirrors", "translucent stones","brittle tongs", "leaky pipes", "chipped reagents", "suspended droplets of potion", "recovery potions", "mana restoring potions",
    "scratched formulas", "jagged beakers", "floating ink pens", "arcane compass", "leather-bound experiments", "health recovery potions", "apothecary tables", "medical supplies", "mysterious pills", "strength recovery potions", "surgical equipment", "stats increase potions", 
    "resurrection spell books", "formaldehyde bottles", "box filled with elements from the periodic table", "hazard masks", "enchanted googles", "poison resistant gloves", "steel-plated apron armor", "sleep potions", "singed parchment scraps", "scrolls sealed with wax", 
    "overflowing mixing bowls", "corked tubes of swirling mist", "smoking cauldrons","jars of blinking eyes", "tiny elemental cores", "levitating potion kits", "vials glowing with runes", "dried amphibians in trays",
    "racks of dusty philters", "preserved insects in resin", "crumbling alchemy charts", "bowls of glowing moss", "trays of silver dust", "rings etched with formulas", "bundled spell tags", "glowing magic circles", "goblets with pulsing liquids", "runes carved into the floor",
    "shelves of unstable elixirs", "blood-streaked instruction books", "hollow-eyed masks", "bubbling spirit jars", "scales tipped with strange weights", "amphorae sealed with wax", "wand racks next to beakers", "pewter basins with herbs", "blackened crucibles", "oily pools around the workspace",
    "unfolded alchemical maps", "shifting sigils on stone", "frosted containers", "clay statues with missing arms", "mystic-lit lanterns", "lattices of infused copper wire", "etched elemental glyphs", "a locked case of forbidden brews", "cracked reagent stones", "alchemical puzzles on the wall", 
    "moving skeleton models", "animated anatomical models of creatures", "magic circles", "indiscernible scribbles", "chalkboards covered in formulas"],
        
    "sounds": ["bubbling liquid", "glass clinking", "hissing fumes", "a faint chemical hiss", "soft fizzing", "metal tools scraping stone","corks popping from flasks", "sputtering flames", "fluid dripping steadily", "vials shaking slightly", "a kettle-like whistle",
    "the crackle of magical energy", "pages turning softly", "an unsettling hum", "tubes vibrating lightly", "steam venting into the air","a sudden alchemical pop", "potion bottles gurgling", "a faint whisper in an unknown tongue", "soft dripping onto parchment", "air swirling in a jar",
    "magical fizzles and sparks", "a heartbeat-like pulsing", "the swirl of reagents in a vial", "chalk scraping against slate", "a cauldron rumbling deeply","glass fracturing under pressure", "strange gurgles from unseen corners", "wind whooshing inside a sealed bottle", "tiny explosions from a lab bench", "a chorus of bubbling reactions",
    "vibrating resonant frequencies", "muffled chanting from an old scroll", "runes humming with power", "unseen insects clicking in jars", "leather straps creaking near chemicals","a whoosh of flame under a beaker", "fluid boiling violently", "crystal chimes from a reagent box", "strange echoes from inside a flask",
    "a soft tone rising in pitch unexpectedly", "a teapot whistling",  "liquid sizzling on metal", "a vial imploding softly", "glowing runes pulsing in rhythm", "a sudden belch of steam", "glass humming with energy","phantom whispers inside a flask", "a low resonant drone", "alchemy symbols shifting audibly", "boiling sludge in a sealed jar", 
    "a flask vibrating ominously"," static crackling near a sigil", "bottles clattering from a shelf", "a sharp snap of magical discharge", "ethereal laughter echoing from a cauldron", "a soft ticking from enchanted gears",
    "oily bubbles surfacing then popping", "muffled growls from a jar", "pipes rattling under pressure", "magical echoes bouncing off walls", "a sudden whoosh of air from nowhere","faint musical tones from glowing herbs", "the fizz of reagents reacting violently", "wet splashes on stone", "a mysterious liquid sloshing rhythmically", "an echoing snap of cold air",
    "the hum of suspended orbs", "grinding metal from an unseen source", "a glass rod resonating like a bell", "bones rattling in a brew", "wind trapped in a beaker spinning", "ghostly chanting from closed jars", "a sudden glug from a sealed bottle", "murmuring voices in no known language", "faint ticking from nowhere", "metallic whispers from a drawer",
    "rattling reagents in glass tubes", "a soft exhale from a mossy vent", "the rustle of dried herbs shifting themselves", "pulses of sound tied to glowing glyphs", "glass spheres rattling quietly","spectral laughter from behind a curtain", "boiling acid in a ceramic pot", "the screech of metal expanding", "air distorting with a hollow sound", "the wheeze of overfilled tubes",
    "a low hiss of boiling beakers", "popcorn-like crackling of powdered elements", "the jingle of enchanted chains", "dripping slime onto hot stone", "the flutter of scrolls in sudden wind", "gravelly tones from a stone tablet", "the groan of enchanted machinery", "bubbling ichor frothing", "soft murmurs from bottled shadows", "ethereal whimpers behind locked cabinets"],
        
    "actions": ["making your eyes water", "intriguing your mind", "inviting you in", "sending chills down your spine", "filling the air with unease", "making you feel watched",
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
        "giving the sense that something is hiding nearby", "making you feel lost in time"]
    },
    "Puzzle Room": {
    "adjectives": ["confusing", "patterned", "mysterious", "clever", "cryptic", "intricate", "confounding", "enigmatic", "arcane",
    "mysterious", "symbol-covered", "puzzling", "ornate","patterned", "calculated", "riddle-filled", "mechanical", "clever",
    "segmented", "labyrinthine", "timed", "structured", "unforgiving", "circular", "ancient", "sealed", "silent", "dimly lit","esoteric", "locked", "trap-lined", "claustrophobic", "angular",
    "glowing", "metal-trimmed", "tile-bound", "coded", "compressed","scripted", "strange", "shifting", "twisting","cryptic", "intricate", "confounding", "arcane", "fun","immersive",
    "mysterious", "symbolic", "puzzling", "complex", "ornate", "patterned", "calculated", "mechanical", "clever", "segmented", "labyrinthine", "timed", "structured", "circular", "ancient", "innovative",
    "sealed", "silent", "dim", "esoteric", "locked","claustrophobic", "angular", "glowing", "coded", "compressed","scripted", "strange", "shifting", "twisting", "eerie","interactive", "thought-provoking",
    "tiled", "dusty", "forbidding", "geometric", "tricky", "confusing", "calculated", "methodical", "obscure","puzzling","mechanical", "mindbending", "thoughful", "deceptive", "intelligent",
    "glimmering", "hidden", "sharp", "surreal", "ancient", "large", "small", "odd", "symmetrical", "great", "frustrating","interesting","difficult","unsolved","comlicated", "intriguing","intricate",
    "philosophical", "psychological", "strange", "indiscernible","metaphysical","challenging", "vast","perplexing","unsolvable","time-consuming", "enormous", "difficult","competive","thrilling","addictive",
    "brutal", "intense","stimulating", "enriching","puzzling"],
        
    "features": ["runes", "tiles", "switches", "stone tiles etched with symbols", "rotating statues", "glowing runes","sliding floor panels", "lever arrays", "pressure plates","locked pedestals", "rotating rings", 
    "switch mechanisms","murky mirrors", "glimmering glyphs", "numbered columns","sequence panels", "magic-locked doors", "glowing floor patterns","puzzle boxes", "riddle-inscribed walls", "color-coded crystals",
    "floating platforms", "mysterious keyholes", "buttons","shifting walls", "magic sigil grids", "ancient dials","glowing floor tiles", "rotating puzzle discs", "rune-marked pillars","frozen grandfather clock", "morse code sheets", 
    "rubix cubes","engraved stone blocks", "light-refracting crystals", "motion-sensitive plates","statues with movable arms", "interlocking gears", "orb pedestals","patterned mosaics", "whispering inscriptions", "numbered locks",
    "hidden compartments", "mirror arrays", "pendulum triggers","voice-activated switches", "floating puzzle pieces", "beautiful kaleidoscopes","hidden pressure pads","water flow channels", "elemental panels", "time-sensitive switches",
    "golden hourglasses", "hovering cubes", "color-changing stones", "teleportation circles", "color-coded lights", "rotating ceiling tiles", "tiles that play music notes", "gemstone slots", "ticking bombs", "shape-shifting walls", "statues with missing pieces",
    "chess set missing pieces", "sliding slots", "set of levers", "illusionary doorways","shifting mosaic patterns", "identical set of statues","biometric locks", "sundial mechanisms", "mysterious counting devices", "light up tiles", "shelves with cryptic scrolls",
    "a pile of keys", "a line of keyholes", "puzzle cubes wiht shifting patterns", "stone faces with movable mouths", "invisible puzzle grids", "books that whisper riddles", "levers", "locked safes", "scrolls inscribed with invisible ink", "uncompleted magic circles"],
        
    "sounds": ["gears turning", "tiles clicking", "mechanical whirrs", "clicking gears", "a soft hum of magic", "whirring mechanisms", "metal sliding into place","tiles shifting", "runes glowing with a pulse", "a faint ticking", "stones grinding together",
    "magical chimes", "echoes of a riddle being whispered", "crystal resonating softly","water dripping rhythmically", "distant clanking", "a subtle magical vibration","intermittent clicks", "arcane pulses", "glass tinkling faintly", "an echoing thunk",
    "clockwork ticking", "a hush that intensifies", "mischievious laughter","a sudden mechanical snap", "glowing runes pulsing with sound", "stone doors rumbling shut","magical wind swirling in place", "ethereal whispers forming words", 
    "clicks echoing from unseen walls","metal locking into place", "a magical bell chiming once", "a deep magical hum building up","suction-like hissing", "magical threads vibrating", "runes softly crackling","a jolt of arcane static", "a voiceless riddle echoing", 
    "a faint rumble beneath your feet","crystals ringing in harmony", "the rush of shifting air", "soft rhythmic beeping","faint chanting in an unknown language", "a brief magical pop", "grandfather clock chiming", "scraping stone panels", "arcane murmurs just beyond comprehension", "a harp string vibrating without touch",
    "soft footfalls that aren’t your own", "a clock chiming with no visible source", "an invisible voice counting down","gears locking into alignment", "a magical current fizzing through the air", "a coded tone repeating every few seconds",
    "clicks synchronizing like a rhythm", "a whispered riddle repeating in a loop", "air rushing through hidden vents","invisible locks snapping shut", "the echo of a puzzle being solved", "an illusionary breeze brushing your ear","the floor humming beneath your boots", "a rune fizzling out", 
    "fragments of speech assembling into clues","crystal rods resonating together", "a shimmer of invisible energy breaking"],
    
    "actions": ["daring you to solve them", "twisting your logic", "inviting you in", "sending chills down your spine", "filling the air with unease", "making you feel watched",
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
        "giving the sense that something is hiding nearby", "making you feel lost in time"]
    },
    "Magic Chamber": {
    "adjectives": ["arcane", "ethereal", "glowing", "charged", "mystical", "glimmering", "enchanted", "mystical",
    "radiant", "whispering", "floating", "runed", "sparkling","charged", "hallowed", "twinkling", "resonant", "pulsating",
    "veiled", "shifting", "astral", "illuminated", "humming","bejeweled", "empowered", "twilight-lit", "transcendent", "brilliant",
    "dimensional", "veined", "invisible", "enfolded", "celestial", "mirrored", "timeless", "hexed", "fluxing", "luminescent",
    "chromatic", "sigil-bound", "warded", "phantasmal", "eldritch", "otherworldly", "mystifying", "glowing", "spellbound",
    "glistening", "floating", "dim-lit", "vibrating", "sacred","crystal-lined", "murmuring", "aura-filled", "resplendent", "humming",
    "silken", "bewitched", "mythic", "infinite", "gaseous","dreamlike", "enshrouded", "unearthly", "oracular", "arcing","celestial", 
    "elementally tinged", "pale-lit", "translucent", "shimmering", "flickering", "bound", "ancient", "echoing", "haunted",
    "sigil-etched", "rune-lit", "sparkling", "color-shifting", "veil-wrapped", "witchy", "bright", "iridescent", "colorful","questionable",
    "astral","pulsing","dreamlike", "surreal","rare", "divine", "twinkling", "cosmic", "magical","intangible", "forgotten","ghostly", "luminous",
    "transcendent", "unfathomable", "serene", "secret","powerful","sinister","devious", "tricky", "alluring", "charming", "glamorous", "exciting",
    "fascinating","wicked", "supernatural"],
        
    "features": ["floating symbols", "glowing glyphs", "magic circles", "glowing runes", "floating crystals", "hovering spellbooks", "arcane circles", "enchanted candles",
    "levitating orbs", "mystic sigils", "wisps of light", "pulsing glyphs", "shimmering veils","ancient relics", "drifting scrolls", "luminescent fog", "runes etched in stone", "floating staircases",
    "mirror-like portals", "crystal altars", "astral projections", "orbital diagrams", "flickering starlight","bound grimoires", "pools of glowing water", "phantom hands", "celestial markings", "a glowing summoning circle",
    "ethereal vines", "illusionary walls", "gravity-defying artifacts", "sparkling dust", "talking statues","radiant beams of light", "spinning arcane devices", "color-shifting tiles", "invisible platforms", "suspended scrolls",
    "whirling particles", "motes of mana", "floating chains", "singing crystals", "magical mirrors", "runes pulsing with energy", "bookshelves that rearrange themselves", "a hovering crystal heart", ""
    "rings of floating stones", "sigils carved into obsidian", "wisps trapped in glass jars","a pool reflecting unknown stars", "chains suspended midair", "a magical hourglass with falling stardust", "potions that increase a stat by 1"
    "a glowing floor mosaic", "a chandelier made of floating gems", "phantoms whispering to walls","shelves of bottled dreams", "mystic energy flowing through the air", "a circle of unlit candles", 
    "a globe of swirling mist", "pillars engraved with forgotten languages", "light that bends unnaturally","pages that turn themselves", "an orb suspended between pillars", "a harp playing itself",
    "shards of a broken dimension", "a mirror that doesn’t reflect", "a staircase leading nowhere","a rune-inscribed stone table", "a portal that pulses with light", "phantom symbols shifting across the floor",
    "a pedestal with a single levitating coin", "paintings that move slightly", "a breeze with no source","arcane banners fluttering in stillness", "shelves with books chained shut", "flickering magical torches",
    "a cracked wall radiating energy", "arcane roots growing from the ceiling", "ceiling stars that respond to touch","shadows that move independently", "floor tiles glowing beneath each step", "a hovering ring of spell components",
    "magic-infused cobwebs", "weather entrapped in globes", "a crystal prism spinning slowly in midair", "arcane tattoos glowing on the walls", "invisibility cloaks", "torches with eternal flames", "wild shape spells"
    "books that flip pages when you approach", "floor tiles arranged in celestial constellations","a staff levitating upright", "flames frozen in place", "a cauldron stirring itself",
    "a spiral staircase that appears and disappears", "a barrier of translucent light","floating rings orbiting a black orb", "ancient bones held together by energy", "love potions", "doppleganger spells",
    "a constellation projected across the ceiling", "sand swirling in a suspended globe","floor markings that shift when walked on", "ghostly eyes watching from the corners",
    "a floating hourglass counting backward", "a single feather hovering in silence","a bookstand glowing with faint blue light", "curtains made of woven stars", ""
    "circular sigils rotating just above the floor", "a locked door with no handle","walls that ripple like water", "a ghostly staircase leading upward into mist",
    "an orb that glows brighter as you approach", "a lantern filled with bottled lightning","a dome of force sealing off part of the room", "an open spellbook inscribed with living ink",
    "a carpet embroidered with ever-shifting runes", "a chain of pearls orbiting a glowing gem","a swirling portal the size of a coin", "books floating in a slow orbit", 
    "glass orbs crackling with contained storms", "a mural that animates when touched","a rune circle hovering one inch off the ground", "a whispering flame atop a staff",
    "liquid light dripping from cracks in the walls", "a mirror that shows a different version of yourself","a ceiling of swirling clouds", "stairs that reform themselves as you move"],
        
    "sounds": ["magical humming", "whispers of spells", "a burst of energy", "a low arcane hum", "whispers in an unknown tongue", "a gentle crackling of magical energy",
    "the soft chime of floating crystals", "pages rustling without wind", "an echo of distant chanting",
    "pulsing magical energy", "soft harmonic vibrations", "a tinkling like wind chimes",
    "a rush of invisible currents", "a melodic tone from nowhere", "crackles of unstable magic",
    "distant laughter fading in and out", "the echo of a closing spellbook", "murmured voices looping endlessly",
    "arcane sparks flickering", "phantom footsteps circling", "a bell toll with no source",
    "the static hiss of latent energy", "soft ticking from unseen mechanisms",
    "the murmur of shifting glyphs", "faint heartbeats in the walls", "a spectral sigh",
    "glowing runes clicking into place", "the flutter of ethereal wings",
    "a dripping echo with no water", "reverberating magical tones", "a spell being softly recited",
    "the hum of a levitating orb", "unseen gears grinding slowly", "light whispering as it moves",
    "the sudden whoosh of teleportation", "a pulse of light synchronized with sound",
    "the rattle of ghostly chains", "a distant magical explosion", "a harp note suspended in time",
    "glowing glyphs flickering with sound", "a breeze sweeping arcane dust", "a magical bubble popping",
    "mystic energy humming like static", "a clock ticking backward", "an ethereal choir humming softly", "a rune locking into place with a satisfying click",
    "a deep vibration echoing from below", "glistening particles chiming as they swirl",
    "a soft breeze whispering forgotten names", "the flickering beat of magical fire",
    "a low droning pulse from the walls", "the hiss of spectral steam vents",
    "a single note stretching endlessly", "the harmonic clang of enchanted metal",
    "the popping of energy bubbles", "voices whispering from beneath the floor",
    "a magical glyph sizzling into existence", "a wave of silence crashing over the room",
    "bells ringing from distant planes", "a harmonic wave pulsing outward",
    "a fizzing noise from glowing potions", "an echoing hum bouncing between walls",
    "a tone resonating with your heartbeat", "sparkles of energy crackling like fireflies",
    "shifting sands grinding in rhythm", "the creaking of a portal slowly closing",
    "tiny magical gears spinning in the air", "a phantom string plucked gently",
    "low booms from distant wizardry", "magical ink swirling with sound",
    "a faint magical pulse syncing with the light", "dust dancing to an inaudible rhythm",
    "energy strands snapping like taut wires", "an incantation whispered in reverse",
    "the hum of dimensional friction", "glowing orbs thumping like drumbeats",
    "a melody played on invisible instruments", "sigils locking into radiant formations",
    "a voice echoing your own words", "crystal tones cascading like a waterfall",
    "the breath of an unseen entity", "a sudden gasp of magical pressure releasing",
    "a beautiful siren song", "a shifting echo that never fades",  "a radiant hum growing louder and softer", "a swirl of wind circling the ceiling",
    "celestial bells echoing with each step", "a whisper mimicking your thoughts",
    "crystalline wind dancing between sigils", "a faint ticking like a magical clock",
    "the shimmer of protective wards", "a ghostly chant repeating a lost spell",
    "a loud snap of a barrier being formed", "the sizzling pulse of unstable enchantments",
    "glowing runes fizzing in midair", "soft knocks with no apparent source",
    "a resonant gong vibrating in your chest", "whirling particles making harp-like sounds",
    "soft murmurs in forgotten languages", "pulses of energy creating deep vibrations",
    "chimes suspended in zero gravity", "a soft thrum syncing with magical light",
    "the warble of a dimensional fold", "an arcane storm howling in miniature",
    "shifting harmonics that feel sentient", "disjointed laughter cut off suddenly",
    "the hum of levitating crystals in orbit", "phantom chains dragging in reverse",
    "a spell winding itself into the air", "the buzz of residual incantation",
    "a ritual drumbeat echoing below", "the clash of elements in magical stasis",
    "a reverberation pulsing with arcane rhythm", "a radiant vibration shaking the floor slightly",
    "intermittent flashes with snapping sounds", "a magical crackle dancing like lightning",
    "celestial harp strings plucked by wind", "a whisper forming intelligible syllables",
    "a looped voice trapped in the chamber", "static mist fizzing with mana",
    "the lull of magical sleep washing over", "the sigh of a dying spell",
    "a glowing barrier humming steadily", "invisible wings fluttering past your ear"],
        
    "actions": ["empowering your soul", "tingling your senses", "inviting you in", "sending chills down your spine", "filling the air with unease", "making you feel watched",
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
        "giving the sense that something is hiding nearby", "making you feel lost in time"]
    }
}
ROOM_COMPONENT_CYCLES = {}

def format_sentence(sentence):
    sentence = re.sub(r"\b(A|An)\s+(\w+)", lambda m: "An " + m.group(2) if m.group(2)[0].lower() in VOWELS else "A " + m.group(2), sentence)
    sentence = re.sub(r"([.!?])([A-Za-z])", r"\1 \2", sentence)
    sentence = re.sub(r"([.!?])\s*([a-z])", lambda m: f"{m.group(1)} {m.group(2).upper()}", sentence)
    return sentence[0].upper() + sentence[1:] if sentence else sentence

def generate_room_description(room_type):
    components = ROOM_COMPONENTS.get(room_type)
    if not components:
        return "A room with indistinct features."

    # Initialize cycles once per room_type
    if room_type not in ROOM_COMPONENT_CYCLES:
        ROOM_COMPONENT_CYCLES[room_type] = {
            "adjectives": ShufflingCycle(components["adjectives"]),
            "features": ShufflingCycle(components["features"]),
            "sounds": ShufflingCycle(components["sounds"]),
            "actions": ShufflingCycle(components["actions"]),
        }

    cycles = ROOM_COMPONENT_CYCLES[room_type]

    structure = SENTENCE_STRUCTURES.popleft()
    SENTENCE_STRUCTURES.append(structure)

    desc = structure.format(
        adjective=next(cycles["adjectives"]),
        feature=next(cycles["features"]),
        sound=next(cycles["sounds"]),
        action=next(cycles["actions"])
    )

    return format_sentence(desc)



def generate_maze(width, height, room_count, seed=None):
    if seed is None:
        seed = random.random()
        print(f"Generated New Seed: {seed} - Use this to regenerate the same maze!")
    else:
        print(f"Using Provided Seed: {seed} - This will generate the same maze.")

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
    room_types = list(ROOM_TYPES.keys())
    random.shuffle(room_types)
    height, width = len(maze), len(maze[0])

    def is_valid_room(x, y):
        return room_grid[y][x] is None and maze[y][x] == PATH

    if count >= len(room_types):
        selected_rooms = room_types[:] + random.choices(room_types, k=count - len(room_types))
    elif count >= 7:
        selected_rooms = room_types[:count]
    else:
        selected_rooms = random.choices(room_types, k=count)

    placed_rooms = 0
    for room_type in selected_rooms:
        for _ in range(100):
            x = random.randint(1, width - 2)
            y = random.randint(1, height - 2)
            if is_valid_room(x, y):
                room_grid[y][x] = room_type
                maze[y][x] = room_type
                desc_list.append((ROOM_TYPES[room_type]['color'], room_type, generate_room_description(room_type)))
                placed_rooms += 1
                break

    if placed_rooms < count:
        print(f"Warning: Only {placed_rooms} rooms placed out of {count}. Maze might be too small.")

def display_maze(maze):
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
                image[y, x] = ROOM_TYPES[maze[y][x]]['rgb']
            else:
                image[y, x] = (255, 255, 255)

    plt.close('all')
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
    print("\n Maze Parameters:")
    print(f"- Maze Size: {width} x {height}")
    print(f"- Number of Rooms: {room_count}")

    display_maze(maze)

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

"""

"""