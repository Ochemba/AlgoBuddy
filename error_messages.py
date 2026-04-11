# error_messages.py - User-friendly error messages

ERROR_MESSAGES = {
    "no_api_key": """
❌ API Key Not Found!

Please set up your OpenAI API key:
1. Create a .env file in your project folder
2. Add this line: OPENAI_API_KEY=your-key-here
3. Get your key from: https://platform.openai.com/api-keys
""",
    
    "no_internet": """
❌ Cannot Connect to Internet!

Please check:
1. Your internet connection is working
2. You're not behind a firewall blocking OpenAI
3. Try again in a moment
""",
    
    "rate_limit": """
❌ Too Many Requests!

You've made too many API calls too quickly.
Please wait a minute and try again.

Tip: Enable conversation trimming to use fewer tokens!
""",
    
    "invalid_topic": """
❌ Invalid Topic!

Valid topics are:
- loops
- functions  
- lists
- dictionaries
- classes
- files
- strings
- variables

Try one of these!
""",
    
    "server_error": """
❌ OpenAI Server Error!

The AI service is temporarily unavailable.
Please try again in a few minutes.

This is not your fault - it's on OpenAI's side.
"""
}

def get_error_message(error_type, custom_msg=""):
    """Get a user-friendly error message"""
    message = ERROR_MESSAGES.get(error_type, "❌ An error occurred. Please try again.")
    if custom_msg:
        message += f"\n\nDetails: {custom_msg}"
    return message