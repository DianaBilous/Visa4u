// Подключение к WebSocket
const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const chatLog = document.getElementById('chat-log');
    const newMessage = document.createElement('p');
    newMessage.textContent = data.message;
    chatLog.appendChild(newMessage);
};

chatSocket.onclose = function(e) {
    console.error('Чат WebSocket закрыт неожиданно');
};

document.getElementById('chat-message-submit').onclick = function(e) {
    const messageInputDom = document.getElementById('chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';  // Очистка поля ввода
};

// Функция для открытия чата
function openChat() {
    document.getElementById("chat-window").style.display = "block";
}

// Функция для закрытия чата
function closeChat() {
    document.getElementById("chat-window").style.display = "none";
}
