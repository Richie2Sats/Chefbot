const apiKey = 'VENICE-INFERENCE-KEY-Ef0MBBr2N9lwxzlXQT8LNS-q134y9ZgHFGYsvVl06i'; // Replace this with your actual API key
const apiUrl = 'https://api.venice.ai/api/v1/chat/completions';

const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const chatHistory = document.getElementById('chatHistory');
const clearBtn = document.getElementById('clearBtn');

const systemPrompt = `
You are "ChefBot", an expert culinary assistant with a warm, encouraging personality.

YOUR GOAL:
- Help the user cook delicious meals.
- Provide step-by-step instructions.
- Suggest ingredient substitutions.
- Remember the user's specific preferences and recipes.

MEMORY RULES (CRITICAL):
- The user will tell you about their personal recipes (e.g., "My lasagna uses cottage cheese instead of ricotta").
- You MUST remember these details for future conversations.
- If the user asks "How do I make my lasagna again?", recall the specific ingredients they told you previously.

TONE:
- Professional yet friendly.
- Use appetizing language.
- If a user's idea sounds bad, gently suggest a better alternative rather than just saying no.
`;

let messages = [];

function loadHistory() {
    try {
        const saved = localStorage.getItem('chefChatHistory');
        if (saved) {
            messages = JSON.parse(saved);
            messages.forEach(msg => {
                if (msg.role !== 'system') {
                    appendMessage(msg.role, msg.content);
                }
            });
        } else {
            messages = [{ role: "system", content: systemPrompt }];
        }
    } catch (e) {
        console.error("Error loading history, resetting...", e);
        messages = [{ role: "system", content: systemPrompt }];
        localStorage.removeItem('chefChatHistory');
    }
}

function saveHistory() {
    try {
        localStorage.setItem('chefChatHistory', JSON.stringify(messages));
    } catch (e) {
        console.error("Error saving history", e);
    }
}

function appendMessage(role, text) {
    const div = document.createElement('div');
    div.classList.add('message', role);
    div.textContent = text;
    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

sendBtn.addEventListener('click', async () => {
    const userText = chatInput.value.trim();
    if (!userText) return;

    messages.push({ role: "user", content: userText });
    appendMessage('user', userText);
    chatInput.value = '';
    sendBtn.disabled = true;
    saveHistory();

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': \`Bearer \${apiKey}\`
            },
            body: JSON.stringify({
                model: "llama-3.3-70b",
                messages: messages,
                temperature: 0.7
            })
        });

        const data = await response.json();
        const botReply = data.choices[0].message.content;

        messages.push({ role: "assistant", content: botReply });
        appendMessage('assistant', botReply);
        saveHistory();

    } catch (error) {
        console.error(error);
        appendMessage('assistant', "Sorry, I had trouble connecting to the kitchen. Check your internet connection.");
    } finally {
        sendBtn.disabled = false;
        chatInput.focus();
    }
});

chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendBtn.click();
    }
});

clearBtn.addEventListener('click', () => {
    if(confirm("Are you sure? This will delete all recipe memories.")) {
        localStorage.removeItem('chefChatHistory');
        location.reload();
    }
});

// Initialize
loadHistory();
