"""
Test script for Chefbot functionality
This demonstrates the core features without requiring an actual API key
"""

import os
import sys
import tempfile
from unittest.mock import Mock, patch

# Add the current directory to the path
sys.path.insert(0, '/home/runner/work/Chefbot/Chefbot')

from chefbot import ConversationMemory, VeniceAIClient, Chefbot


def test_conversation_memory():
    """Test the conversation memory functionality."""
    print("Testing Conversation Memory...")
    
    # Create a temporary database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        memory = ConversationMemory(db_path)
        
        # Test adding messages
        memory.add_message('user', 'What is a good recipe for pasta carbonara?')
        memory.add_message('assistant', 'I\'d be happy to share a classic carbonara recipe...')
        memory.add_message('user', 'Can you remind me of the carbonara recipe?')
        
        # Test retrieving recent messages
        recent = memory.get_recent_messages(2)
        assert len(recent) == 2
        assert recent[0]['role'] == 'assistant'
        assert recent[1]['role'] == 'user'
        
        # Test retrieving all messages
        all_msgs = memory.get_all_messages()
        assert len(all_msgs) == 3
        
        # Test clearing history
        memory.clear_history()
        all_msgs = memory.get_all_messages()
        assert len(all_msgs) == 0
        
        print("  ✓ Conversation memory works correctly")
        
    finally:
        # Cleanup
        if os.path.exists(db_path):
            os.remove(db_path)


def test_venice_ai_client():
    """Test the Venice AI client."""
    print("Testing Venice AI Client...")
    
    client = VeniceAIClient('test_api_key')
    
    # Verify initialization
    assert client.api_key == 'test_api_key'
    assert 'Authorization' in client.headers
    assert client.headers['Content-Type'] == 'application/json'
    
    print("  ✓ Venice AI client initializes correctly")


def test_chefbot_integration():
    """Test the Chefbot integration with mocked API."""
    print("Testing Chefbot Integration...")
    
    # Create a temporary database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        # Mock the VeniceAIClient.chat method
        with patch('chefbot.VeniceAIClient.chat') as mock_chat:
            mock_chat.return_value = "I'd be happy to help you with that recipe!"
            
            # Create bot with test database
            bot = Chefbot('test_api_key')
            # Replace the memory with one using our test database
            bot.memory = ConversationMemory(db_path)
            
            # Test chatting
            response = bot.chat('How do I make bread?')
            
            assert response == "I'd be happy to help you with that recipe!"
            
            # Verify message was stored
            messages = bot.memory.get_all_messages()
            assert len(messages) == 2  # user message + assistant response
            assert messages[0]['role'] == 'user'
            assert messages[0]['content'] == 'How do I make bread?'
            assert messages[1]['role'] == 'assistant'
        
        print("  ✓ Chefbot integration works correctly")
        
    finally:
        # Cleanup
        if os.path.exists(db_path):
            os.remove(db_path)


def test_system_prompt():
    """Test that the system prompt is properly configured."""
    print("Testing System Prompt...")
    
    bot = Chefbot('test_api_key')
    
    # Verify system prompt contains key elements
    assert 'professional chef' in bot.SYSTEM_PROMPT.lower()
    assert 'recipes' in bot.SYSTEM_PROMPT.lower()
    assert 'remember' in bot.SYSTEM_PROMPT.lower()
    
    print("  ✓ System prompt is properly configured")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Running Chefbot Tests")
    print("=" * 60)
    print()
    
    try:
        test_conversation_memory()
        test_venice_ai_client()
        test_chefbot_integration()
        test_system_prompt()
        
        print()
        print("=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
