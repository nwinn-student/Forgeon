const generate_maze = () => {
    let width = 0;
    let height = 0;
    let room_filters = 0;
    let room_num = 0;
    let max_room_size = 0;
    for(let i = 0; i < document.querySelector("#room-filters").querySelectorAll("input").length; i++)
        if(document.querySelector("#room-filters").querySelectorAll("input")[i].checked)
            room_filters |= (1 << i);
    if(document.querySelector("#width").value)
        width = document.querySelector("#width").value
    if(document.querySelector("#height").value)
        height = document.querySelector("#height").value
    if(document.querySelector("#room-num").value)
        room_num = document.querySelector("#room-num").value
    if(document.querySelector("#max-room-size").value)
        max_room_size = document.querySelector("#max-room-size").value
    location.assign(`/maze/${width}/${height}/${Math.floor(Math.random() * 4294967295)}/rf=${room_filters};rnum=${room_num};mrsize=${max_room_size}`);
}