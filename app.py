from flask import Flask, request, jsonify
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Initialize the OpenAI client
load_dotenv()
API_KEY = os.getenv("API_KEY")
client = OpenAI(api_key=API_KEY)
assistant_id = "asst_LpgGqNaMQGdwz5Cjrk7q52Nn"
thread_id = "thread_1fVhNglC0T9n3rKj2wdcRfZ5"

# Function to send a message to the assistant
def send_message(content):
    # Send a message in the thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )

    # Run the assistant with the current thread context
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="Please address the user as Jane Doe. The user has a premium account."
    )

    # Check if the run is completed and retrieve assistant response
    if run.status == 'completed':
        message_resp = client.beta.threads.messages.list(thread_id=thread_id)
        messages = message_resp.data if hasattr(message_resp, 'data') else []

        # Collect assistant responses
        assistant_responses = []
        for message in messages:
            if hasattr(message, 'role') and message.role == 'assistant':
                for content_block in message.content:
                    if hasattr(content_block, 'text') and hasattr(content_block.text, 'value'):
                        assistant_responses.append(content_block.text.value)

        return assistant_responses[0] if assistant_responses else "No response."
    return "Error: The request did not complete."

# Flask route to handle the POST request
@app.route("/query", methods=["POST"])
def query():
    user_input = request.json.get("content")
    response = send_message(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True, port=5003)
