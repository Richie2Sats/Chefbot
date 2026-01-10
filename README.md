# ChefBot - Your Personal Culinary Assistant

A chatbot powered by Venice AI that helps you cook, remember your recipes, and plan meals.

## Features

- 🍳 Get cooking instructions and recipes
- 📝 Remember your personal recipe preferences
- 💡 Get ingredient substitution suggestions
- 🔒 Secure API key management
- 📊 Comprehensive error handling and logging

## Setup Instructions

### 1. Configure API Key

1. Copy the example configuration file:
   ```bash
   cp config.example.js config.js
   ```

2. Open `config.js` and replace `YOUR_API_KEY_HERE` with your Venice AI API key:
   ```javascript
   apiKey: 'your-actual-api-key-here'
   ```

3. **Important**: Never commit `config.js` to version control. It's already in `.gitignore`.

### 2. Get Your API Key

To get a Venice AI API key:
1. Visit [https://venice.ai](https://venice.ai)
2. Create an account or sign in
3. Navigate to API settings
4. Generate a new API key

### 3. Run the Application

Simply open `index.html` in your web browser, or serve it with a local web server:

```bash
# Using Python
python3 -m http.server 8080

# Using Node.js
npx http-server -p 8080

# Then open http://localhost:8080 in your browser
```

## Configuration Options

The `config.js` file includes the following configurable options:

- `apiKey`: Your Venice AI API key (required)
- `apiUrl`: API endpoint URL (default: Venice AI chat completions)
- `model`: AI model to use (default: llama-3.3-70b)
- `temperature`: Response creativity (0.0 - 1.0, default: 0.7)
- `enableLogging`: Enable console logging for debugging (default: true)
- `logApiRequests`: Log API request details (default: true)
- `logApiResponses`: Log API response details (default: true)

## Error Handling

The application includes comprehensive error handling for:

- Invalid or missing API keys
- Network connectivity issues
- API rate limiting (429 errors)
- Server errors (500, 502, 503)
- Invalid requests (400 errors)
- Malformed API responses

All errors are logged to the browser console and display user-friendly messages.

## Logging

When `enableLogging` is enabled in `config.js`, the application logs:
- Chat history loading and saving
- API request details (model, message count, temperature)
- API response status
- Error details for debugging

To disable logging in production, set `enableLogging: false` in `config.js`.

## Privacy & Security

- API keys are stored locally in `config.js` (gitignored)
- Chat history is stored in browser localStorage
- No data is sent to third parties except the Venice AI API
- Clear your chat history anytime with the "Clear Memory" button

## Troubleshooting

### Configuration Error
If you see "Configuration error: config.js file is missing":
1. Make sure you've created `config.js` from `config.example.js`
2. Ensure `config.js` is in the same directory as `index.html`

### API Key Error
If you see "API key is invalid or expired":
1. Verify your API key is correct in `config.js`
2. Check that your API key hasn't expired
3. Ensure the key has proper permissions

### Network Error
If you see "Network error - please check your internet connection":
1. Check your internet connection
2. Verify the API endpoint URL is correct
3. Check browser console for CORS or blocking issues

## License

This project is open source and available for personal and educational use.
