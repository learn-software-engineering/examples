# AI Chatbot Application

A simple web-based chatbot that can answer questions about artificial intelligence using OpenAI's API.

## Overview

This project creates a user-friendly web interface where users can chat with an AI assistant specialized in artificial intelligence topics. The application uses Flask for the backend, plain JavaScript for the frontend, and OpenAI's GPT model to generate intelligent responses.

## Features

- Real-time chat interface
- Conversation memory within a session
- Ability to clear conversation history
- Visual indicators for user and AI messages
- "AI is thinking" status indicator
- Responsive design

## Project Structure

```
my-ai-chatbot/
├── app.py                 # Main Flask application
├── wsgi.py                # WSGI entry point for production servers
├── .env                   # Environment variables configuration
├── requirements.txt       # Python dependencies
└── templates/
    └── index.html         # Chat interface HTML/CSS/JS
```

## Installation

1. Clone the repository or download the code
2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up your OpenAI API key:
   - Obtain an API key from [OpenAI's platform](https://platform.openai.com/api-keys)
   - Update the `.env` file with your API key:
     ```
     OPENAI_API_KEY=your_actual_api_key_here
     ```

## Usage

### Development Mode

Run the application locally:

```
python app.py
```

This will start the server in debug mode on `http://127.0.0.1:5000`.

### Production Mode

For production deployment, use a WSGI server like Gunicorn:

```
gunicorn wsgi:app
```

## How It Works

### Backend (app.py)

1. **Server Setup**: Initializes a Flask server and connects to the OpenAI API.
2. **Routes**:
   - `/`: Renders the chat interface
   - `/chat`: Processes messages, sends them to OpenAI, and returns AI responses
   - `/clear`: Resets the conversation history
3. **Conversation Management**: Maintains context by storing the conversation history.

### Frontend (index.html)

1. **User Interface**: Provides a chat window with message input field and buttons.
2. **JavaScript Functionality**:
   - Captures user input
   - Sends requests to the backend API
   - Displays messages in the chat window
   - Shows/hides the "AI is thinking" indicator
   - Handles the "Clear Conversation" functionality

### OpenAI Integration

The application uses OpenAI's `gpt-4o-mini` model with a custom system prompt that defines the chatbot's personality and area of expertise. Each conversation maintains its history to provide context for more relevant responses.

## Customization

### Changing the AI's Personality

To modify how the AI responds, edit the `SYSTEM_PROMPT` variable in `app.py`. For example:

```python
SYSTEM_PROMPT = """
You are an AI expert specializing in machine learning research.
Provide detailed technical explanations and include references when possible.
"""
```

### Adjusting Response Length

To change how verbose the AI's responses are, modify the `max_tokens` parameter in the OpenAI API call:

```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    max_tokens=300  # Increase for longer responses
)
```

### Changing the Model

To use a different OpenAI model, change the `model` parameter:

```python
response = client.chat.completions.create(
    model="gpt-4o",  # More capable but more expensive
    messages=messages,
    max_tokens=150
)
```

## Security Considerations

- Keep your API key secure and never commit it directly to your code repository
- Consider implementing rate limiting to prevent abuse
- For production, add proper authentication mechanisms

## Limitations

- The free tier of OpenAI API has usage limits
- The chatbot's knowledge is limited to what the AI model was trained on
- Without additional context, the AI may not have information about very recent developments

## License

This project is open source and available for personal and educational use.

## Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Powered by [OpenAI API](https://platform.openai.com/)
- Uses [python-dotenv](https://github.com/theskumar/python-dotenv) for environment management
