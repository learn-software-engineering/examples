import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv

"""
Main application file for the AI Chatbot.
This file sets up a Flask web server that hosts a simple chatbot interface.
The chatbot uses OpenAI's API to generate responses to user queries.
"""

# Load environment variables from .env file
# This allows us to keep sensitive information like API keys out of the code
load_dotenv()

# Initialize Flask app - this creates the web application
app = Flask(__name__)

# Initialize OpenAI client with API key from environment variables
# The API key is needed to authenticate requests to OpenAI's services
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the chatbot's personality and capabilities through a system prompt
# This prompt instructs the AI on how to behave and respond to queries
SYSTEM_PROMPT = """
You are a helpful AI assistant designed to answer questions about artificial intelligence.
You are friendly, informative, and concise in your responses.
"""

# Initialize an empty list to store the conversation history
# This allows the AI to remember previous interactions within a session
conversation_history = []


@app.route('/')
def index():
    """
    Route handler for the home page.

    Returns:
        HTML template: Renders the chat interface
    """
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """
    Route handler for chat functionality.
    Receives user messages, sends them to OpenAI API, and returns AI responses.

    Returns:
        JSON: Contains AI response or error message
    """
    # Extract user message from request data
    data = request.json
    user_message = data.get('message', '')

    # Add user message to conversation history for context
    conversation_history.append({"role": "user", "content": user_message})

    # Prepare messages for API call by combining system prompt with conversation history
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + \
        conversation_history

    try:
        # Call the OpenAI API to generate a response
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Specify which model to use
            messages=messages,    # Provide conversation context
            max_tokens=150        # Limit response length
        )

        # Extract the AI's response text from the API result
        ai_message = response.choices[0].message.content

        # Add AI response to conversation history for future context
        conversation_history.append(
            {"role": "assistant", "content": ai_message})

        # Return the AI response to the frontend
        return jsonify({"response": ai_message})

    except Exception as e:
        # Handle any errors that occur during the API call
        return jsonify({"error": str(e)}), 500


@app.route('/clear', methods=['POST'])
def clear():
    """
    Route handler to clear conversation history.

    Returns:
        JSON: Status message confirming the action
    """
    global conversation_history
    conversation_history = []  # Reset the conversation history
    return jsonify({"status": "cleared"})


if __name__ == '__main__':
    # Run the Flask app in debug mode when executed directly
    # Debug mode allows for automatic reloading when code changes
    app.run(debug=True)
