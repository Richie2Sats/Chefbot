// API configuration is now loaded from config.js
// Validate that CONFIG is loaded
if (typeof CONFIG === 'undefined') {
    console.error('ERROR: config.js not loaded. Please create config.js from config.example.js');
    alert('Configuration error: config.js file is missing. Please check the console for details.');
}

// Logger utility for debugging
const logger = {
    log: function(message, data) {
        if (CONFIG.enableLogging) {
            console.log(`[ChefBot] ${message}`, data || '');
        }
    },
    error: function(message, error) {
        console.error(`[ChefBot ERROR] ${message}`, error || '');
    },
    apiRequest: function(url, payload) {
        if (CONFIG.enableLogging && CONFIG.logApiRequests) {
            console.log('[ChefBot API Request]', {
                url: url,
                model: payload.model,
                messageCount: payload.messages.length,
                temperature: payload.temperature
            });
        }
    },
    apiResponse: function(response, data) {
        if (CONFIG.enableLogging && CONFIG.logApiResponses) {
            console.log('[ChefBot API Response]', {
                status: response.status,
                statusText: response.statusText,
                ok: response.ok,
                hasData: !!data
            });
        }
    }
};

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
        logger.log('Loading chat history from localStorage');
        const saved = localStorage.getItem('chefChatHistory');
        if (saved) {
            messages = JSON.parse(saved);
            logger.log('Chat history loaded', { messageCount: messages.length });
            messages.forEach(msg => {
                if (msg.role !== 'system') {
                    appendMessage(msg.role, msg.content);
                }
            });
        } else {
            logger.log('No saved history found, initializing with system prompt');
            messages = [{ role: "system", content: systemPrompt }];
        }
    } catch (e) {
        logger.error("Error loading history, resetting...", e);
        messages = [{ role: "system", content: systemPrompt }];
        localStorage.removeItem('chefChatHistory');
    }
}

function saveHistory() {
    try {
        localStorage.setItem('chefChatHistory', JSON.stringify(messages));
        logger.log('Chat history saved', { messageCount: messages.length });
    } catch (e) {
        logger.error("Error saving history", e);
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

    // Validate configuration
    if (!CONFIG.apiKey || CONFIG.apiKey === 'YOUR_API_KEY_HERE') {
        logger.error('API key not configured');
        appendMessage('assistant', "⚠️ Configuration Error: Please set up your API key in config.js");
        return;
    }

    messages.push({ role: "user", content: userText });
    appendMessage('user', userText);
    chatInput.value = '';
    sendBtn.disabled = true;
    saveHistory();

    const requestPayload = {
        model: CONFIG.model,
        messages: messages,
        temperature: CONFIG.temperature
    };

    try {
        logger.log('Sending message to API');
        logger.apiRequest(CONFIG.apiUrl, requestPayload);

        const response = await fetch(CONFIG.apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${CONFIG.apiKey}`
            },
            body: JSON.stringify(requestPayload)
        });

        logger.apiResponse(response, null);

        // Check if the response is ok (status 200-299)
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            logger.error('API request failed', {
                status: response.status,
                statusText: response.statusText,
                errorData: errorData
            });

            let errorMessage = "Sorry, I had trouble connecting to the kitchen. ";
            
            // Provide specific error messages based on status code
            switch (response.status) {
                case 401:
                    errorMessage += "API key is invalid or expired. Please check your config.js file.";
                    break;
                case 429:
                    errorMessage += "Rate limit exceeded. Please wait a moment and try again.";
                    break;
                case 500:
                case 502:
                case 503:
                    errorMessage += "The API service is temporarily unavailable. Please try again later.";
                    break;
                case 400:
                    errorMessage += "Invalid request format. Please check the API configuration.";
                    break;
                default:
                    errorMessage += `Server error (${response.status}): ${response.statusText}`;
            }
            
            if (errorData.error && errorData.error.message) {
                errorMessage += `\n\nDetails: ${errorData.error.message}`;
            }

            appendMessage('assistant', errorMessage);
            // Remove the failed user message from history
            messages.pop();
            saveHistory();
            return;
        }

        const data = await response.json();
        logger.log('API response received', { hasChoices: !!data.choices });

        // Validate response structure
        if (!data.choices || !data.choices[0] || !data.choices[0].message) {
            logger.error('Invalid API response structure', data);
            appendMessage('assistant', "Sorry, I received an unexpected response from the kitchen. Please try again.");
            messages.pop();
            saveHistory();
            return;
        }

        const botReply = data.choices[0].message.content;
        logger.log('Bot reply received', { length: botReply.length });

        messages.push({ role: "assistant", content: botReply });
        appendMessage('assistant', botReply);
        saveHistory();

    } catch (error) {
        logger.error('Request failed with exception', error);
        
        let errorMessage = "Sorry, I had trouble connecting to the kitchen. ";
        
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            errorMessage += "Network error - please check your internet connection.";
        } else if (error.name === 'AbortError') {
            errorMessage += "Request timed out. Please try again.";
        } else {
            errorMessage += `Error: ${error.message}`;
        }
        
        appendMessage('assistant', errorMessage);
        // Remove the failed user message from history
        messages.pop();
        saveHistory();
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
