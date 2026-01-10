"""
Chefbot - A Professional Chef AI Assistant with Conversation Memory

This module provides a chatbot powered by Venice AI that acts as a professional chef,
helping with recipes, cooking techniques, and culinary questions while maintaining
conversation history.
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import List, Dict, Optional
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ConversationMemory:
    """Manages conversation history using SQLite database."""
    
    def __init__(self, db_path: str = "chefbot_conversations.db"):
        """Initialize the conversation memory with a SQLite database.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history.
        
        Args:
            role: The role of the message sender (user or assistant)
            content: The message content
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO conversations (timestamp, role, content) VALUES (?, ?, ?)",
            (timestamp, role, content)
        )
        
        conn.commit()
        conn.close()
    
    def get_recent_messages(self, limit: int = 10) -> List[Dict[str, str]]:
        """Retrieve recent messages from conversation history.
        
        Args:
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of message dictionaries with role and content
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT role, content FROM conversations ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        
        messages = [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]
        messages.reverse()  # Return in chronological order
        
        conn.close()
        return messages
    
    def get_all_messages(self) -> List[Dict[str, str]]:
        """Retrieve all messages from conversation history.
        
        Returns:
            List of all message dictionaries with role and content
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT role, content FROM conversations ORDER BY id ASC")
        messages = [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]
        
        conn.close()
        return messages
    
    def clear_history(self):
        """Clear all conversation history."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM conversations")
        
        conn.commit()
        conn.close()


class VeniceAIClient:
    """Client for interacting with Venice AI API."""
    
    def __init__(self, api_key: str, base_url: str = "https://api.venice.ai/api/v1"):
        """Initialize the Venice AI client.
        
        Args:
            api_key: Venice AI API key
            base_url: Base URL for Venice AI API
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def chat(self, messages: List[Dict[str, str]], model: str = "llama-3.3-70b") -> Optional[str]:
        """Send a chat request to Venice AI.
        
        Args:
            messages: List of message dictionaries with role and content
            model: Model to use for the chat
            
        Returns:
            The assistant's response or None if request fails
        """
        url = f"{self.base_url}/chat/completions"
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data["choices"][0]["message"]["content"]
        
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Venice AI: {e}")
            return None


class Chefbot:
    """Main chatbot class for the professional chef assistant."""
    
    SYSTEM_PROMPT = """You are a professional chef with decades of experience in culinary arts. 
You are helping someone keep track of recipes and providing cooking assistance. Your expertise includes:

- International cuisines and cooking techniques
- Recipe development and adaptation
- Ingredient substitutions and dietary accommodations
- Cooking tips, tricks, and troubleshooting
- Food safety and storage recommendations
- Kitchen equipment and tool usage
- Meal planning and preparation strategies

You are warm, encouraging, and patient. You provide clear, detailed instructions when needed.
You remember previous conversations and can reference recipes or techniques discussed earlier.
When users share recipes, you remember them and can recall them later.
You provide measurements in both metric and imperial units when relevant.

Always be helpful, friendly, and professional in your responses."""
    
    def __init__(self, api_key: str, context_window: int = 10):
        """Initialize the Chefbot.
        
        Args:
            api_key: Venice AI API key
            context_window: Number of recent messages to include in context
        """
        self.client = VeniceAIClient(api_key)
        self.memory = ConversationMemory()
        self.context_window = context_window
    
    def chat(self, user_message: str) -> str:
        """Process a user message and return the bot's response.
        
        Args:
            user_message: The user's input message
            
        Returns:
            The bot's response
        """
        # Add user message to memory
        self.memory.add_message("user", user_message)
        
        # Build message list with system prompt and recent context
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        
        # Add recent conversation history for context
        recent_messages = self.memory.get_recent_messages(self.context_window)
        messages.extend(recent_messages)
        
        # Get response from Venice AI
        response = self.client.chat(messages)
        
        if response:
            # Add assistant response to memory
            self.memory.add_message("assistant", response)
            return response
        else:
            return "I apologize, but I'm having trouble connecting right now. Please try again."
    
    def clear_memory(self):
        """Clear all conversation history."""
        self.memory.clear_history()
        print("Conversation history cleared.")


def main():
    """Main function to run the Chefbot CLI."""
    print("=" * 60)
    print("🍳 Welcome to Chefbot - Your Professional Chef Assistant! 🍳")
    print("=" * 60)
    print()
    
    # Get API key from environment
    api_key = os.getenv("VENICE_AI_API_KEY")
    
    if not api_key:
        print("❌ Error: VENICE_AI_API_KEY not found in environment variables.")
        print()
        print("Please create a .env file with your Venice AI API key:")
        print("VENICE_AI_API_KEY=your_api_key_here")
        print()
        print("Or set it as an environment variable:")
        print("export VENICE_AI_API_KEY=your_api_key_here")
        return
    
    # Initialize the chatbot
    bot = Chefbot(api_key)
    
    print("I'm your professional chef assistant, here to help with recipes,")
    print("cooking techniques, and culinary questions!")
    print()
    print("Commands:")
    print("  - Type your message to chat")
    print("  - Type 'clear' to clear conversation history")
    print("  - Type 'quit' or 'exit' to end the session")
    print()
    print("-" * 60)
    print()
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Check for commands
            if user_input.lower() in ["quit", "exit"]:
                print()
                print("👋 Thank you for using Chefbot! Happy cooking!")
                break
            
            if user_input.lower() == "clear":
                bot.clear_memory()
                continue
            
            # Get bot response
            print()
            print("Chef: ", end="", flush=True)
            response = bot.chat(user_input)
            print(response)
            print()
            print("-" * 60)
            print()
        
        except KeyboardInterrupt:
            print()
            print()
            print("👋 Thank you for using Chefbot! Happy cooking!")
            break
        
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            print("Please try again.")
            print()


if __name__ == "__main__":
    main()
