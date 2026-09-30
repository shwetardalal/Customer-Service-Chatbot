const chatMessages = document.querySelector('#chatMessages');
const chatForm = document.querySelector('#chatForm');
const messageInput = document.querySelector('#messageInput');
const sendButton = document.querySelector('#sendButton');
const clearButton = document.querySelector('#clearChat');
const welcomeMessage = "Hi there! 👋 Welcome to Northstar. I'm your support assistant—what can I help you with today?";

function currentTime() {
    return new Intl.DateTimeFormat([], { hour: 'numeric', minute: '2-digit' }).format(new Date());
}

function addMessage(text, sender) {
    const row = document.createElement('article');
    row.className = `message-row ${sender}-row`;
    const avatar = document.createElement('div');
    avatar.className = `message-avatar ${sender === 'user' ? 'user-avatar' : ''}`;
    avatar.setAttribute('aria-hidden', 'true');
    avatar.textContent = sender === 'user' ? 'Y' : 'N';
    const content = document.createElement('div');
    content.className = 'message-content';
    const bubble = document.createElement('div');
    bubble.className = `message-bubble ${sender === 'user' ? 'user-bubble' : 'bot-bubble'}`;
    const paragraph = document.createElement('p');
    paragraph.textContent = text;
    bubble.append(paragraph);
    const time = document.createElement('time');
    time.className = 'message-time';
    time.dateTime = new Date().toISOString();
    time.textContent = currentTime();
    content.append(bubble, time);
    row.append(avatar, content);
    chatMessages.append(row);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return row;
}

function showTypingIndicator() {
    const row = document.createElement('article');
    row.className = 'message-row bot-row typing-row';
    row.setAttribute('aria-label', 'Assistant is typing');
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = 'N';
    avatar.setAttribute('aria-hidden', 'true');
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble bot-bubble';
    bubble.innerHTML = '<div class="typing-indicator" aria-hidden="true"><span></span><span></span><span></span></div>';
    row.append(avatar, bubble);
    chatMessages.append(row);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return row;
}

async function sendMessage(text) {
    const message = text.trim();
    if (!message || sendButton.disabled) return;

    addMessage(message, 'user');
    messageInput.value = '';
    messageInput.style.height = 'auto';
    sendButton.disabled = true;
    const typingRow = showTypingIndicator();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message }),
        });
        const data = await response.json();
        typingRow.remove();
        if (!response.ok) throw new Error(data.error || 'The message could not be sent.');
        addMessage(data.reply, 'bot');
    } catch (error) {
        typingRow.remove();
        addMessage(error.message || 'Connection error. Please try again.', 'bot');
    } finally {
        sendButton.disabled = false;
        messageInput.focus();
    }
}

chatForm.addEventListener('submit', (event) => {
    event.preventDefault();
    sendMessage(messageInput.value);
});

messageInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        chatForm.requestSubmit();
    }
});

messageInput.addEventListener('input', () => {
    messageInput.style.height = 'auto';
    messageInput.style.height = `${Math.min(messageInput.scrollHeight, 100)}px`;
});

document.querySelectorAll('.suggestion-chip').forEach((chip) => {
    chip.addEventListener('click', () => {
        const suggestions = {
            'Track an order': 'How can I track my order?',
            'View pricing': 'What are your prices?',
            'Talk to support': 'How can I contact customer support?',
        };
        sendMessage(suggestions[chip.firstChild.textContent.trim()]);
    });
});

clearButton.addEventListener('click', () => {
    chatMessages.replaceChildren();
    const divider = document.createElement('div');
    divider.className = 'day-divider';
    const today = document.createElement('span');
    today.textContent = 'Today';
    divider.append(today);
    chatMessages.append(divider);
    addMessage(welcomeMessage, 'bot');
    messageInput.focus();
});
