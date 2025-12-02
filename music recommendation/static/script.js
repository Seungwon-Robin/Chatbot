document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const userMessage = userInput.value.trim();
        if (userMessage === '') return;

        // Display user's message
        addMessage(userMessage, 'user');
        userInput.value = '';

        // Show loading indicator
        const loadingIndicator = addMessage('', 'bot', true);

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            });

            // Remove loading indicator
            loadingIndicator.remove();

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            const botMessage = data.response || '죄송합니다. 답변을 생성하는 데 실패했습니다.';
            
            // Display bot's response
            addMessage(botMessage, 'bot');

        } catch (error) {
            console.error('Error:', error);
            // Remove loading indicator on error as well
            if(loadingIndicator) loadingIndicator.remove();
            addMessage('죄송합니다. 서버와 통신 중 오류가 발생했습니다.', 'bot');
        }
    });

    function addMessage(message, sender, isLoading = false) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);

        const p = document.createElement('p');

        if (isLoading) {
            p.classList.add('loading');
            p.innerHTML = '<span></span><span></span><span></span>';
        } else {
            // Replace newlines with <br> for proper display
            p.innerHTML = message.replace(/\n/g, '<br>');
        }
        
        messageElement.appendChild(p);
        chatBox.appendChild(messageElement);

        // Scroll to the bottom
        chatBox.scrollTop = chatBox.scrollHeight;

        return messageElement; // Return for potential modification (e.g., removing loading indicator)
    }
});