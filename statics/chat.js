let chatSocket = null;
let currentRoomName = null;
const username = document.getElementById('username').value;

document.getElementById('join-room').addEventListener('click', joinRoom);

function joinRoom() {
    const roomName = document.getElementById('room-name').value;
    if (roomName) {
        const url = `wss://line0013-501003cf1db4.herokuapp.com/ws/chat/${roomName}/`;
        console.log('Join Room', url);
        chatSocket = new WebSocket(url);
        console.log(username);
        currentRoomName = roomName;
        console.log('Chat Socket:', chatSocket, 'Room:', currentRoomName);
        initChatSocket();
        addRoomToList(roomName);
    }
}

function initChatSocket() {
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log('Data:', data, 'Room:', currentRoomName);
        if (data.type === 'chat') {
            console.log('Message:', data.message);
            console.log('Room:', currentRoomName);
            addMessage(data.message, data.user);
        }
    };

    document.getElementById('form').addEventListener('submit', function(e) {
        e.preventDefault();
        sendMessage();
    });
}

function addRoomToList(roomName) {
    const roomDiv = document.getElementById('rooms');
    roomDiv.insertAdjacentHTML('beforeend', `
        <div id="room_${roomName}">
            <p>${roomName}</p>
        </div>
    `);

    // 追加した部屋の要素を取得
    let newRoomElement = document.getElementById(`room_${roomName}`);

    // クリックイベントリスナーを追加
    newRoomElement.addEventListener('click', function() {
        changeRoom(roomName);
    });

    // 全ての chat_talks クラスを持つ要素を取得し、非表示にする
    allclose();

    // 新たなチャットルームを表示する
    const roomChat = document.getElementById('talkroom');
    roomChat.insertAdjacentHTML(
        'beforeend',
        `<div id="Room_${roomName}" class="chat_talks">
            <h2>Room: ${roomName}</h2>
            <div id="messages_${roomName}" class="messages"></div>
        </div>`
    );
}

function addMessage(message, username) {
    if ( `${message}` != '')  {
        const messagesDiv = document.getElementById(`messages_${currentRoomName}`);
        messagesDiv.insertAdjacentHTML('beforeend', `<div><p>${username}:${message}</p></div>`);
    }
}

function sendMessage() {
    const form = document.getElementById('form');
    const formData = new FormData(form);
    const message = formData.get('message');
    console.log('Send Message:', message, 'Room:', currentRoomName);
    chatSocket.send(JSON.stringify({'message': message, 'room': currentRoomName , 'user': username}));
    form.reset();
}

function allclose() {
    let chatTalksElements = document.querySelectorAll('.chat_talks');
    chatTalksElements.forEach(element => {
        element.style.display = 'none';
    });
}

function changeRoom(roomName) {
    allclose();
    currentRoomName = roomName;
    let roomElement = document.getElementById(`Room_${roomName}`);
    roomElement.style.display = 'block';
}