import gradio as gr
import sqlite3
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Database Operations
def add_contact(name, phone):
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
    conn.commit()
    conn.close()
    return f"Added {name} with phone number {phone}"

def get_contact(name):
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    cursor.execute('SELECT phone FROM contacts WHERE name LIKE ?', (f"%{name}%",))
    result = cursor.fetchone()
    conn.close()
    if result:
        return f"{name}'s phone number is {result[0]}"
    else:
        return f"No contact found for {name}"

def get_all_contacts():
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, phone FROM contacts')
    contacts = cursor.fetchall()
    conn.close()

    if contacts:
        result = "Phone Book:\n"
        for name, phone in contacts:
            result += f"{name}: {phone}\n"
        return result
    else:
        return "Phone book is empty"

def update_contact(name, phone):
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE contacts SET phone = ? WHERE name LIKE ?', (phone, f"%{name}%"))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()

    if rows_affected > 0:
        return f"Updated {name}'s phone number to {phone}"
    else:
        return f"No contact found for {name}"

def delete_contact(name):
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE name LIKE ?', (f"%{name}%",))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()

    if rows_affected > 0:
        return f"Deleted contact for {name}"
    else:
        return f"No contact found for {name}"
def get_contact_by_phone(phone):
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM contacts WHERE phone LIKE ?', (f"%{phone}%",))
    result = cursor.fetchone()
    conn.close()
    if result:
        return f"The number {phone} belongs to {result[0]}"
    else:
        return f"No contact found with phone number {phone}"
# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# LLM-based command interpreter
def process_command_with_llm(command):
    # Define the system prompt to set the context for the LLM
    system_prompt = """
    You are a phone book assistant that helps users manage their contacts.
    Your task is to interpret user commands and extract the necessary information.
    Always respond in JSON format with the following structure:
    {
        "action": "add" | "get" | "get_by_phone" | "list" | "update" | "delete" | "unknown",
        "name": "extracted name" or null if not applicable,
        "phone": "extracted phone number" or null if not applicable,
        "confidence": a value between 0 and 1 indicating your confidence in the interpretation
    }
    """

    # Make API call to OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": command}
            ],
            response_format={"type": "json_object"}
        )

        # Extract the JSON response
        result = response.choices[0].message.content
        import json
        parsed_result = json.loads(result)

        # Execute the appropriate action based on the LLM's interpretation
        action = parsed_result.get("action", "unknown")
        name = parsed_result.get("name")
        phone = parsed_result.get("phone")
        confidence = parsed_result.get("confidence", 0)

        # If confidence is too low, ask for clarification
        if confidence < 0.7:
            return "I'm not entirely sure what you want to do. Could you please rephrase your command?"

        # Execute the appropriate database operation
        if action == "add" and name and phone:
            return add_contact(name, phone)
        elif action == "get" and name:
            return get_contact(name)
        elif action == "list":
            return get_all_contacts()
        elif action == "update" and name and phone:
            return update_contact(name, phone)
        elif action == "delete" and name:
            return delete_contact(name)
        elif action == "get_by_phone" and phone:
            return get_contact_by_phone(phone)
        else:
            return "I couldn't understand that command. Please try again."

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Gradio Interface
def create_interface():
    with gr.Blocks(title="Phone Book App with LLM") as app:
        gr.Markdown("# Phone Book App")
        gr.Markdown("Use natural language to manage your contacts")

        with gr.Row():
            with gr.Column():
                command_input = gr.Textbox(label="Enter your command", placeholder="e.g., Add John with number 123456789")
                submit_btn = gr.Button("Submit")

            with gr.Column():
                output = gr.Textbox(label="Result")
                show_all_btn = gr.Button("Show All Contacts")

        # Example prompts
        gr.Examples(
            examples=[
                "Add to my phone book John. His phone number is 123456789.",
                "Please add a record for Joanna with the number 222333444.",
                "What is the phone number for Joanna?",
                "Show me full phone book",
                "Update John's number to 987654321",
                "Delete contact for Joanna",
                "I need to change Maria's phone to 555123456",
                "Who's number is 222333444?",
                "Remove Alex from my contacts"
            ],
            inputs=command_input
        )

        # Event handlers
        submit_btn.click(process_command_with_llm, inputs=command_input, outputs=output)
        show_all_btn.click(lambda: get_all_contacts(), outputs=output)

    return app

# Main function
def main():
    init_db()
    app = create_interface()
    app.launch()

if __name__ == "__main__":
    main()
