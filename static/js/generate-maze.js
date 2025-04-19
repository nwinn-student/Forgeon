// Dungeon type presets configuration
const DUNGEON_PRESETS = {

    'Tomb': {
        requiredRooms: ['Treasure Room', 'Trap Room', 'Secret Room'],
        minRooms: 5,
        maxRoomSize: 10,
        mazeWidth: 30,
        mazeHeigth: 30
    },

    'Labyrinth': {
        requiredRooms: ['Treasure Room', 'Trap Room', 'Monster Lair', 'Library', 'Puzzle Room'],
        minRooms: 5,
        maxRoomSize: 10,
        mazeWidth: 30,
        mazeHeigth: 30
    },

    'Trick-Or-Treat': {
        requiredRooms: ['Treasure Room', 'Trap Room'],
        minRooms: 2,
        maxRoomSize: 10,
        mazeWidth: 30,
        mazeHeigth: 30
    },

    'Wizard Tower': {
        requiredRooms: ['Treasure Room', 'Secret Room', 'Library', 'Alchemy Lab', 'Magic Chamber'],
        minRooms: 5,
        maxRoomSize: 10,
        mazeWidth: 30,
        mazeHeigth: 30
    },

    'Stronghold': {
        requiredRooms: ['Treasure Room', 'Armory', 'Prison Room', 'Secret Room'],
        minRooms: 5,
        maxRoomSize: 10,
        mazeWidth: 30,
        mazeHeigth: 30
    }
    // Add more presets here
};

// Function to handle dungeon preset selection
function handleDungeonPreset(presetValue) {
    if (!presetValue) return;
    
    const preset = DUNGEON_PRESETS[presetValue];
    if (!preset) return;

    // Set minimum number of rooms
    const roomNumInput = document.querySelector("#room-num");
    roomNumInput.value = Math.max(preset.minRooms, roomNumInput.value || 0);
    
    // Set max room size
    const maxRoomSizeInput = document.querySelector("#max-room-size");
    maxRoomSizeInput.value = preset.maxRoomSize;

    // Set maze width
    const mazeWidth = document.querySelector("#width");
    mazeWidth.value = preset.mazeWidth;

    // Set maze height
    const mazeHeigth = document.querySelector("#height");
    mazeHeigth.value = preset.mazeHeigth;

    // Uncheck all room types first
    document.querySelectorAll('.room-type-checkbox').forEach(checkbox => {
        const label = checkbox.nextElementSibling.textContent;
        checkbox.checked = preset.requiredRooms.includes(label);
    });
}

// Add event listeners for dungeon presets
document.querySelectorAll('.dungeon-preset').forEach(radio => {
    radio.addEventListener('change', (e) => handleDungeonPreset(e.target.value));
});

const generate_maze = () => {
    let width = 0;
    let height = 0;
    let room_filters = 0;
    let room_num = 0;
    let max_room_size = 0;
    
    // Get selected room types
    document.querySelectorAll('.room-type-checkbox').forEach((checkbox, i) => {
        if(checkbox.checked) {
            room_filters |= (1 << i);
        }
    });

    // Get other parameters
    if(document.querySelector("#width").value)
        width = document.querySelector("#width").value;
    if(document.querySelector("#height").value)
        height = document.querySelector("#height").value;
    if(document.querySelector("#room-num").value)
        room_num = document.querySelector("#room-num").value;
    if(document.querySelector("#max-room-size").value)
        max_room_size = document.querySelector("#max-room-size").value;

    // Generate the maze
    location.assign(`/maze/${width}/${height}/${Math.floor(Math.random() * 4294967295)}/rf=${room_filters};rnum=${room_num};mrsize=${max_room_size}`);
}