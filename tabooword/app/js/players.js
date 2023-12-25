var numPlayer=0

function createPlayer(){
    numPlayer = numPlayer+1
    const div = document.getElementById("character")
    const template = document.getElementById("player_template")
    const instance = template.content.cloneNode(true);
    const player = "Player"+numPlayer.toString()
    instance.id=player
    instance.getElementById('player').id=player
    console.log("Create New player=",instance.id)

    // Player Title
    const titleElement = instance.getElementById('playerTitle');
    titleElement.id = player+"Title";
    titleElement.innerHTML=player
    // Player image id
    const imgElement = instance.getElementById('playerImg');
    imgElement.id = player+"Img";
    // Button
    instance.getElementById("playerLeft").onclick= function() { changeImageLeft(player+"Img") }
    instance.getElementById("playerRight").onclick= function() { changeImageRight(player+"Img") }
    // Player Name
    const nameElement = instance.getElementById('playerName')
    nameElement.id = player+"Name"
    div.append(instance)
    document.getElementById("button_footer").scrollIntoView();
  }
function deletePlayer(){
    document.getElementById("Player"+numPlayer.toString()).remove()
    numPlayer = numPlayer-1
    document.getElementById("Player"+numPlayer.toString()).scrollIntoView();
}
function changeImageLeft(id){//change character image to left
    var maxFile=16
    var img = document.getElementById(id);
    var current_file = Number(img.src.split('.')[0].split('/')[4])
    current_file = current_file-1
    if (current_file<=0) {
        current_file = maxFile
    } 

    let fileNum = current_file.toLocaleString('en-US', {
        minimumIntegerDigits: 2,
        useGrouping: false
    })
    img.src="figure/"+fileNum+".png";
    console.log("Left image=", img.src)
    return false;
}
function changeImageRight(id){//change character image to right
    var maxFile=16
    var img = document.getElementById(id);
    var current_file = Number(img.src.split('.')[0].split('/')[4])
    current_file = current_file+1
    if (current_file>maxFile) {
        current_file = 1
    } 

    let fileNum = current_file.toLocaleString('en-US', {
        minimumIntegerDigits: 2,
        useGrouping: false
    })
    img.src="figure/"+fileNum+".png";
    console.log("Left image=", img.src)
    return false;
}
function submitPlayer(id){ // get player information
    const players = document.getElementById(id);
    var names=[]
    var avatars=[]
    for (const child of players.children) {
        var player = child.id
        var avatar = document.getElementById(player+"Img").src
        var name = document.getElementById(player+"Name").value
        avatar = avatar.split('/')
        avatars.push(avatar[avatar.length-1])
        names.push(name)
        console.log('avatars=',avatars,'names=',names)
      }
    return [names, avatars]
}