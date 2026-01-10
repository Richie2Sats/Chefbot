// Configuration file for ChefBot
// Copy this file to 'config.js' and replace with your actual API key

const CONFIG = {
    // Venice AI API configuration
    apiKey: 'YOUR_API_KEY_HERE', // Replace with your Venice AI API key
    apiUrl: 'https://api.venice.ai/api/v1/chat/completions',
    model: 'llama-3.3-70b',
    temperature: 0.7,
    
    // Debug settings
    enableLogging: true, // Set to false in production to disable verbose logging
    logApiRequests: true, // Log API request details
    logApiResponses: true // Log API response details
};
