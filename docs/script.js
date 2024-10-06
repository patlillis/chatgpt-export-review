// Load the JSON file and handle search
document.getElementById('search').addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const keyword = formData.get('keyword').toLowerCase()

    fetch('conversations.json')
        .then(response => response.json())
        .then(data => searchConversations(keyword, data))
        .catch(error => console.error('Error loading JSON:', error));
});

function searchConversations(keyword, data) {
    // Find matching messages.
    const results = [];
    for (const conversation of data) {
        const title = conversation.title || 'No Title';
        const messages = conversation.mapping ?? {};

        for (const [msgId, { message: messageData }] of Object.entries(messages)) {
            if (messageData?.content != null) {
                const messageParts = messageData.content.parts ?? [];
                const filteredParts = messageParts
                    .filter(part => typeof part === 'string')
                    .map(part => part.toLowerCase())
                    .filter(part => part.includes(keyword))
                    .map(part => ({
                        title,
                        message: part,
                        conversationId: conversation.id,
                        messageId: msgId
                    }));
                results.push(...filteredParts);
            }
        }
    }

    // Clear previous results.
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    // Display results
    resultsDiv.innerHTML = '<h2>Results</h2>';

    if (results.length > 0) {
        for (const result of results) {
            const conversationUrl = `https://chatgpt.com/chat/${result.conversationId}`;
            const resultDiv = document.createElement('div');
            resultDiv.classList.add('result');
            resultDiv.innerHTML += `
                <h3>${result.title}</h3>
                <p>${result.message}</p>
                <small>Conversation ID: ${result.conversationId}, Message ID: ${result.messageId}</small>
                <br>
                <a href="${conversationUrl}" target="_blank">Open Conversation</a>`;
            resultsDiv.appendChild(resultDiv);
        }
    } else {
        resultsDiv.innerHTML += `<p>No results found.</p>`;
    }
}
