# Natural Language Phone Book Application
A phone book application that interprets natural language commands using OpenAI's LLM
A digital phone book application that allows users to manage contacts using natural language commands. The application uses OpenAI's GPT-3.5 language model to interpret user commands and perform appropriate actions on the contacts database.

## Features
- **Natural Language Understanding**: Use everyday language to manage your contacts instead of specific commands
- **Contact Management**:
  - Add new contacts with name and phone number
  - Retrieve contact information by name
  - Search for contacts by phone number
  - Update existing contact phone numbers
  - Delete contacts from the phone book
  - View all contacts in the phone book
- **Intuitive Interface**: Clean and simple web-based interface built with Gradio
- **Example Commands**: Pre-populated example prompts to help users get started
- **Unique Contact Management**: Prevents duplicate contact names in the phone book

## Technical Details
- **Web Framework**: Gradio for the user interface
- **Database**: SQLite for contact storage
- **Natural Language Processing**: OpenAI GPT-3.5 Turbo for command interpretation
- **Environment Management**: dotenv for API key management

### Technology Choices
- **Gradio**: Selected for its simplicity in creating web interfaces for ML applications with minimal code. Perfect for this interview task as it allows focusing on core functionality rather than frontend development.
- **SQLite**: Chosen for its lightweight, serverless nature that requires no configuration while still providing a robust SQL interface. Ideal for this simple application where a full database server would be overkill.

## Installation
1. Clone this repository:
   ```
   git clone https://github.com/malwinabelczewska/Phonebook-app.git
   cd Phonebook-app
   ```
2. Create a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```
   You can obtain an API key at [OpenAI's platform](https://platform.openai.com/).

## Usage
1. Run the application:
   ```
   python app.py
   ```
2. Open your browser and navigate to the URL shown in the terminal (typically http://127.0.0.1:7860)
3. Enter commands using natural language. Examples:
   - "Add John to my phone book with number 123456789"
   - "What is the phone number for John?"
   - "Who's number is 123456789?"
   - "Update John's number to 987654321"
   - "Show me the full phone book"
   - "Delete contact for John"

## How It Works
1. When a user enters a command, it's sent to the OpenAI API with a system prompt that defines the expected response format.
2. The LLM interprets the command and returns a structured JSON response containing:
   - The intended action (add, get, list, update, delete)
   - The contact name (if applicable)
   - The phone number (if applicable)
   - A confidence score
3. The application then executes the appropriate database operation based on the interpreted command.
4. If the confidence score is too low, the application asks for clarification.

## Database Structure
The application uses a simple SQLite database with a single `contacts` table:
- `name`: Contact name (primary key)
- `phone`: Phone number

This design ensures each contact name is unique in the database, preventing duplicate entries.

## Development Notes
As someone with limited experience in application development, I utilized AI assistance (including Claude and similar tools) to help with code design, implementation, and problem-solving. This approach allowed me to create a functional application while learning more about Python web development, database interactions, and integration with AI services.
