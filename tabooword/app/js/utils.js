let result = []
let idx = 0

function initPlayer(data) {//call init_engine api
    const names = data[0]
    const avatars = data[1]
    console.log('name=', names, 'avatars=', avatars)
    if (names.length==0|avatars.length==0){
      alert("Please add your character to start the game.")
      return False
    }
    
    const response = fetch('http://127.0.0.1:5000/init_engine', {
      method: 'POST',
      body: JSON.stringify({
        'names': names,
        "avatars": avatars,
        "words": true,
      }),
      headers: {
        'Content-Type': 'application/json',
      }
    })
    .then((response) => {
      console.log('API init_engine', response.status, response.statusText)
      if(response.status==200){
        alert("Success! Let's start the game")
        window.location.href ='word.html'
      }
      else{
        txt = "Something wrong! \nError status: "+response.status+ "\nMessage: "+response.statusText
        alert(txt)
      }
    }
    )
  }
function addWord() { //call add api
    const word = document.getElementById("wordInput").value
    if (word==''){
      return False
    }
    console.log("get word: ", word)
    const response = fetch('http://127.0.0.1:5000/add', {
      method: 'POST',
      body: JSON.stringify({
        'word': word
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json()
    .then(data => ({status: response.status, body: data})
      )
    ).then(obj=>{
      console.log("API add", obj)
      updateWordStatus()
      if(obj["status"]==200){
        document.getElementById("wordForm").innerHTML = '<input type="name" size="30" style="height: 50px;" class="form-control" id="wordInput" placeholder="Enter your taboo word">'
      }
      else{
        alert(obj["body"]["message"])
      }
      
    })
  }

function resetWord() { //call reset_word api
  const response = fetch('http://127.0.0.1:5000/reset_word')
  .then((response) => {
    console.log("API reset_word", response.status, response.statusText)
    updateWordStatus()
    document.getElementById("wordForm").innerHTML = '<input type="name" size="30" style="height: 50px;" class="form-control" id="wordInput" placeholder="Enter your taboo word">'})
}
function updateWordStatus() { //call check_status api
  const response = fetch('http://127.0.0.1:5000/check_status')
  .then(response => response.json()
  .then(data => ({status: response.status, body: data})
    )
  ).then(obj=>{
    console.log('API check_status',obj)
    document.getElementById("word_status").innerHTML = '<p style="font-size: 50px"> <strong>' + obj["body"]["num_word"] + "</strong> word" + '</p>'
    
  })
}

function randomWord(){ //call random api
  const div = document.getElementById("result");
  div.innerHTML = '<div class="loader"></div>'
  const response = fetch('http://127.0.0.1:5000/random')
  .then(response => response.json()
  .then(data => ({status: response.status, body: data})
    )
  ).then(obj=>{
    console.log('API random', obj)
    updateWordStatus()
    if(obj["status"]==200){
      document.getElementById("wordForm").innerHTML = '<input type="name" size="30" style="height: 50px;" class="form-control" id="wordInput" placeholder="Enter your taboo word">'

      genQrcode(obj["body"]["player"])
    }
    else{
      div.innerHTML = ''
      alert(obj["body"]["message"])
    }
    
  })
}

function genQrcode(data){ //generate QRCode
  result = data
  console.log('Create QRcode data=',result, 'idx=',idx)
  const div = document.getElementById("result");
  div.innerHTML = ''
  const template = document.getElementById("qrTemplate");
  const instance = template.content.cloneNode(true);
  instance.getElementById("playerTitle").innerHTML = result[idx]["name"];
  new QRCode(instance.getElementById("qrcode"), result[idx]["url"]);
  div.append(instance)
}
function changeQRRight(){ //get right QR code
  idx +=1
  if (idx==result.length){
    idx=0;
  }
  console.log('data=',result, "idx=", idx)
  document.getElementById("qrcode").innerHTML=''
  document.getElementById("playerTitle").innerHTML = result[idx]["name"];
  new QRCode(document.getElementById("qrcode"), result[idx]["url"]);

}

function changeQRLeft(){ //get left QR code
  idx -=1
  if (idx<0){
    idx=result.length-1;
  }
  console.log('data=',result, "idx=", idx)
  document.getElementById("qrcode").innerHTML=''
  document.getElementById("playerTitle").innerHTML = result[idx]["name"];
  new QRCode(document.getElementById("qrcode"), result[idx]["url"]);

}