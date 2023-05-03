from flask import Flask, render_template, request
import openai


app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_key = 'API-KEY'
previous_questions_and_answers = []

# Define the default route to return the index.html file
@app.route("/")
def index():
    return render_template("index.html")

# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    INSTRUCTIONS = "You are a friendly chat bot."

    TEMPERATURE = 0.5
    MAX_TOKENS = 3000
    FREQUENCY_PENALTY = 0
    PRESENCE_PENALTY = 0.6

    # limits how many questions we include in the prompt
    MAX_CONTEXT_QUESTIONS = 10

    # build the messages
    messages = [
        {"role": "system", "content": INSTRUCTIONS},
    ]
    # add the previous questions and answers
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({"role": "user", "content": question})
        messages.append({"role": "assistant", "content": answer})
    # add the new question
    # Get the message from the POST request
    new_question = request.json.get("message")
    messages.append({"role": "user", "content": new_question})

    # Send the message to OpenAI's API and receive the response

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=TEMPERATURE,
    max_tokens=MAX_TOKENS,
    top_p=1,
    frequency_penalty=FREQUENCY_PENALTY,
    presence_penalty=PRESENCE_PENALTY,
    )
    if completion.choices[0].message!=None:
        # add the new question and answer to the list of previous questions and answers
        previous_questions_and_answers.append((new_question, str(completion.choices[0].message.content)))
        return completion.choices[0].message
    else :
        return 'Failed to Generate response!'


if __name__=='__main__':
    app.run()

