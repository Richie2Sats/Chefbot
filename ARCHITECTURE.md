# Chefbot Architecture

This document describes the technical architecture of Chefbot.

## Overview

Chefbot is a professional chef chatbot application that uses Venice AI's language models to provide culinary assistance while maintaining conversation history in a local SQLite database.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                      User Interface                      │
│                    (CLI - chefbot.py)                   │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ↓
┌─────────────────────────────────────────────────────────┐
│                      Chefbot Class                       │
│  • Orchestrates conversation flow                       │
│  • Manages context window                               │
│  • Combines memory + AI responses                       │
└──────────────┬──────────────────────┬───────────────────┘
               │                      │
               ↓                      ↓
┌──────────────────────┐    ┌────────────────────────────┐
│ ConversationMemory   │    │    VeniceAIClient          │
│                      │    │                            │
│ • Store messages     │    │ • HTTP API requests        │
│ • Retrieve history   │    │ • Response parsing         │
│ • Clear history      │    │ • Error handling           │
└──────────┬───────────┘    └────────────┬───────────────┘
           │                             │
           ↓                             ↓
┌──────────────────────┐    ┌────────────────────────────┐
│   SQLite Database    │    │      Venice AI API         │
│ chefbot_convos.db    │    │   (api.venice.ai)          │
└──────────────────────┘    └────────────────────────────┘
```

## Components

### 1. User Interface (CLI)

**File**: `chefbot.py` (main function)

The CLI provides a simple command-line interface for users to interact with the chatbot.

**Features**:
- Welcome message and instructions
- Input loop for user messages
- Command handling (quit, exit, clear)
- Error handling and graceful shutdown

### 2. Chefbot Class

**File**: `chefbot.py`

The main orchestrator that combines conversation memory and AI responses.

**Responsibilities**:
- Process user messages
- Maintain conversation context
- Build message history for API calls
- Store responses in memory
- Manage system prompt

**Key Methods**:
- `chat(user_message)`: Process a user message and return response
- `clear_memory()`: Clear conversation history

**Configuration**:
- `SYSTEM_PROMPT`: Professional chef persona and instructions
- `context_window`: Number of recent messages to include (default: 10)

### 3. ConversationMemory Class

**File**: `chefbot.py`

Manages persistent conversation storage using SQLite.

**Database Schema**:
```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    role TEXT NOT NULL,          -- 'user' or 'assistant'
    content TEXT NOT NULL         -- message content
)
```

**Key Methods**:
- `add_message(role, content)`: Store a new message
- `get_recent_messages(limit)`: Retrieve recent N messages
- `get_all_messages()`: Retrieve entire conversation history
- `clear_history()`: Delete all messages

**Features**:
- Automatic database initialization
- Chronological message ordering
- ISO timestamp tracking

### 4. VeniceAIClient Class

**File**: `chefbot.py`

Handles communication with the Venice AI API.

**API Endpoint**: `https://api.venice.ai/api/v1/chat/completions`

**Key Methods**:
- `chat(messages, model)`: Send chat request and get response

**Request Format**:
```json
{
  "model": "llama-3.3-70b",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "temperature": 0.7,
  "max_tokens": 2000
}
```

**Features**:
- Bearer token authentication
- Configurable model selection
- Timeout handling (30 seconds)
- Error handling and logging

## Data Flow

### User Message Flow

1. **User Input**: User types a message in the CLI
2. **Store User Message**: Message is stored in SQLite database
3. **Build Context**: Recent messages are retrieved from database
4. **Prepare Request**: System prompt + context messages are combined
5. **API Call**: Request is sent to Venice AI
6. **Receive Response**: AI response is received and parsed
7. **Store Response**: Assistant response is stored in database
8. **Display**: Response is shown to the user

### Message Context Window

The chatbot maintains a context window of the most recent messages:

```
System Prompt (always included)
  ↓
Message N-10 (oldest in window)
Message N-9
...
Message N-1
Message N (current user message)
  ↓
Sent to Venice AI API
```

## Configuration

### Environment Variables

- `VENICE_AI_API_KEY`: Required API key for Venice AI

### Configuration File

`.env` file format:
```
VENICE_AI_API_KEY=your_api_key_here
```

### Customizable Parameters

In `chefbot.py`:
- `context_window`: Number of recent messages (default: 10)
- `model`: Venice AI model name (default: "llama-3.3-70b")
- `temperature`: Response creativity (default: 0.7)
- `max_tokens`: Maximum response length (default: 2000)
- `SYSTEM_PROMPT`: Chef persona and instructions

## Security Features

1. **No Hardcoded Secrets**: API key from environment variables only
2. **SQL Injection Protection**: Parameterized queries throughout
3. **Timeout Protection**: 30-second timeout on API requests
4. **Error Handling**: Graceful handling of API and database errors
5. **Git Ignore**: Sensitive files excluded (.env, .db files)

## Dependencies

- `requests`: HTTP client for Venice AI API
- `python-dotenv`: Environment variable management
- `sqlite3`: Built-in Python database (no external dependency)

## Testing

Test suite in `test_chefbot.py`:

1. **ConversationMemory Tests**: Database operations
2. **VeniceAIClient Tests**: Client initialization
3. **Integration Tests**: Full chatbot flow (mocked API)
4. **System Prompt Tests**: Configuration validation

## Performance Considerations

- **Database**: SQLite is efficient for single-user applications
- **Context Window**: Limits memory usage and API token consumption
- **API Timeout**: Prevents hanging on slow connections
- **Local Storage**: No external dependencies for persistence

## Future Enhancements

Potential improvements:
- Multi-user support with user IDs
- Export conversation history
- Recipe search and filtering
- Image support for dish photos
- Voice input/output
- Web interface
- Recipe database integration
- Nutritional information lookup

## Troubleshooting

Common issues and solutions:

1. **API Key Not Found**: Create `.env` file with valid key
2. **Connection Errors**: Check internet connection and API status
3. **Database Locked**: Close other instances of the application
4. **Import Errors**: Run `pip install -r requirements.txt`

## Resources

- Venice AI Documentation: https://venice.ai/
- SQLite Documentation: https://sqlite.org/
- Requests Library: https://requests.readthedocs.io/
