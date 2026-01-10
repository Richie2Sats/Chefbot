# Quick Start Guide

Get Chefbot up and running in 5 minutes!

## Prerequisites

- Python 3.7 or higher
- A Venice AI API key (get one at https://venice.ai/)
- Internet connection

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Richie2Sats/Chefbot.git
cd Chefbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `requests` - for API communication
- `python-dotenv` - for environment variable management

### 3. Configure Your API Key

Create a `.env` file:

```bash
cp .env.example .env
```

Edit the `.env` file and add your Venice AI API key:

```
VENICE_AI_API_KEY=your_actual_venice_api_key_here
```

**How to get a Venice AI API key:**
1. Go to https://venice.ai/
2. Sign up for an account
3. Navigate to the API section
4. Generate an API key
5. Copy the key to your `.env` file

### 4. Run Chefbot

```bash
python chefbot.py
```

You should see:

```
============================================================
🍳 Welcome to Chefbot - Your Professional Chef Assistant! 🍳
============================================================

I'm your professional chef assistant, here to help with recipes,
cooking techniques, and culinary questions!

Commands:
  - Type your message to chat
  - Type 'clear' to clear conversation history
  - Type 'quit' or 'exit' to end the session

------------------------------------------------------------

You: 
```

## First Conversation

Try asking Chefbot a question:

```
You: What's a simple recipe for chocolate chip cookies?

Chef: I'd be happy to share a classic chocolate chip cookie recipe...
```

## Tips

- **Ask follow-up questions**: The bot remembers your conversation
- **Save recipes**: Tell the bot about your favorite recipes
- **Get advice**: Ask about techniques, substitutions, or troubleshooting

## Common Commands

- **Regular chat**: Just type and press Enter
- **clear**: Clear the conversation history
- **quit** or **exit**: Close the application

## Troubleshooting

**Problem**: "VENICE_AI_API_KEY not found"
- **Solution**: Make sure you created the `.env` file with your API key

**Problem**: Connection errors
- **Solution**: Check your internet connection and API key validity

**Problem**: Module not found
- **Solution**: Run `pip install -r requirements.txt`

## What's Next?

- Read [EXAMPLES.md](EXAMPLES.md) for conversation examples
- Check [ARCHITECTURE.md](ARCHITECTURE.md) to understand how it works
- Explore the [README.md](README.md) for full documentation

## Need Help?

- Check the documentation in this repository
- Open an issue on GitHub
- Review the code in `chefbot.py`

Happy cooking! 🍳
