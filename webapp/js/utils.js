function startup_warp(script, id){
    id = "'"+id+"'"
    var btn = '<button type="button" class="btn btn-dark btn-lg" id="back" onclick=click_todefault(' + id + ')>Back</button>'
    return '<div class="container">'+script +'</div>'+ btn //'<div class="vertical-center">'+btn+'</div>'
}
function to_default(id){
    id = "'"+id+"'"
    script = '<button type="button" class="btn btn-warning btn-lg" onclick="click_createroom(' + id + ')">Create Room</button><button type="button" class="btn btn-info btn-lg" onclick="click_findroom(' + id + ')">Find Room</button>'
    return script
}
function find_room(){
    var script = '<label for="inputRoomID" class="col-sm-2 col-form-label">ID</label> <div class="col-sm-10"> <input type="room" class="form-control" id="inputRoom"></div>'
    script = '<form><div class="form-group row">' + script + '</div></form>'
    script = script + '<button type="button" class="btn btn-primary btn-lg" id="back">Enter</button>'
    
    return script
}
function create_room(){
    var script = 'room created!!'
    script = '<div class="container"><a>' + script + '</a></div>'
    return script
}

function click_todefault(id){
    script = to_default(id)
    document.getElementById(id).innerHTML = script;
}
function click_findroom(id){
    script = find_room()
    document.getElementById(id).innerHTML = startup_warp(script, id);
}
function click_createroom(id){
    script = create_room()
    document.getElementById(id).innerHTML = startup_warp(script,id);
}
