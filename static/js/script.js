// Генерация случайного room_id
function generateRoomId() {
    return 'room_' + Math.random().toString(36).substring(2, 15);
}

// Если это первая сессия, создаем новый room_id
let roomId = localStorage.getItem('chatRoomId') || generateRoomId();
localStorage.setItem('chatRoomId', roomId);  // Сохраняем его в localStorage, чтобы сохранялась сессия

// Подключение к WebSocket с room_id
const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
const chatSocket = new WebSocket(
    protocol + window.location.host + '/ws/chat/' + roomId + '/'
);

// Обработчик для загрузки истории сообщений и новых сообщений
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const chatLog = document.getElementById('chat-log');
    chatLog.style.overflowY = 'auto';
    chatLog.style.maxHeight = '400px';
    const newMessage = document.createElement('p');

    // Отображаем сообщение с именем пользователя
    newMessage.innerHTML = `<strong>${data.username}:</strong> ${data.message}`;
    chatLog.appendChild(newMessage);

    requestAnimationFrame(() => {
        const lastMessage = chatLog.lastElementChild;
        lastMessage.scrollIntoView({ behavior: 'smooth', block: 'end' });
    });
    
    // Прокрутка вниз при новом сообщении
    chatLog.scrollTop = chatLog.scrollHeight;
};

// Обработчик закрытия WebSocket
chatSocket.onclose = function(e) {
    console.error('Чат WebSocket закрыт неожиданно');
};

// Отправка сообщения
document.getElementById('chat-message-submit').onclick = function(e) {
    const messageInputDom = document.getElementById('chat-message-input');
    const message = messageInputDom.value;

    // Отправляем сообщение на сервер
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