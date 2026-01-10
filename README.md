# Chefbot 🍳

A professional chef AI assistant powered by Venice AI that remembers all conversations, making it the perfect recipe keeper and cooking companion.

## Features

- **Professional Chef Expertise**: Get expert advice on cooking techniques, recipes, and culinary questions
- **Conversation Memory**: All conversations are stored in a local SQLite database, so the chef remembers previous recipes and discussions
- **Recipe Keeper**: Share and save recipes that the bot will remember for future reference
- **Venice AI Powered**: Uses Venice AI's advanced language models for intelligent, contextual responses
- **Easy CLI Interface**: Simple command-line interface for natural conversation
- **Dietary Accommodations**: Get help with ingredient substitutions and dietary requirements

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Richie2Sats/Chefbot.git
   cd Chefbot
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Venice AI API key**:
   
   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file and add your Venice AI API key:
   ```
   VENICE_AI_API_KEY=your_actual_api_key_here
   ```
   
   To get a Venice AI API key, visit [Venice AI](https://venice.ai/) and sign up for an account.

## Usage

Run the chatbot:

```bash
python chefbot.py
```

### Commands

- **Chat**: Simply type your message and press Enter to chat with the chef
- **clear**: Clear the conversation history
- **quit** or **exit**: End the session

### Example Conversations

```
You: Hi! I'm looking for a good pasta recipe.

Chef: Hello! I'd be happy to help you with a pasta recipe. Let me share a classic 
and delicious recipe...

You: Can you remind me of that pasta recipe we discussed?

Chef: Of course! Earlier we talked about the classic pasta recipe with...
```

## How It Works

### Conversation Memory

Chefbot uses a SQLite database (`chefbot_conversations.db`) to store all conversations. This means:

- The chef remembers recipes you've shared
- You can reference previous discussions
- The conversation history persists between sessions
- You can clear history anytime with the `clear` command

### Venice AI Integration

The bot uses Venice AI's API to:

- Generate intelligent, contextual responses
- Understand cooking-related queries
- Provide professional chef-level advice
- Maintain conversation context

### Architecture

The application consists of three main components:

1. **ConversationMemory**: Manages SQLite database for storing conversation history
2. **VeniceAIClient**: Handles API communication with Venice AI
3. **Chefbot**: Main chatbot logic that combines memory and AI responses

## Configuration

You can customize the bot's behavior in `chefbot.py`:

- **context_window**: Number of recent messages to include (default: 10)
- **model**: Venice AI model to use (default: "llama-3.3-70b")
- **temperature**: Response creativity (default: 0.7)
- **max_tokens**: Maximum response length (default: 2000)

## Requirements

- Python 3.7 or higher
- Venice AI API key
- Internet connection for API calls

## Privacy & Data

- All conversation data is stored locally in the SQLite database
- No data is shared except with Venice AI for generating responses
- You can delete the `chefbot_conversations.db` file to remove all history

## Troubleshooting

**Error: VENICE_AI_API_KEY not found**
- Make sure you've created a `.env` file with your API key
- Check that the `.env` file is in the same directory as `chefbot.py`

**Connection errors**
- Verify your internet connection
- Check that your Venice AI API key is valid
- Ensure you haven't exceeded your API rate limits

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Credits

Powered by [Venice AI](https://venice.ai/)