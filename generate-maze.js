// Dungeon type presets configuration
const DUNGEON_PRESETS = {
    'tomb': {
        requiredRooms: ['Treasure Room', 'Trap Room', 'Monster Lair'],
        minRooms: 5,
        maxRoomSize: 10
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