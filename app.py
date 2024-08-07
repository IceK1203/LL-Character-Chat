from flask import Flask, render_template, request, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key

# Function to request AI response
def reqMes(message, apikey):
    url = "https://api.legacylabs.dev/v1/chat"
    params = {
        "message": message,
        "api_key": apikey
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get('message')
        else:
            if response.status_code == 400: 
                return "Oopsie, your message is a bit too long buddy..."
            return f"Error: Received status code {response.status_code}. Message: {response.text}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def chat():
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        user_input = request.form.get("message")
        api_key = request.form.get("api_key")

        # Debugging: Print the input values
        print(f"User input: {user_input}")
        print(f"API key: {api_key}")

        ai_response = reqMes(user_input, api_key)
        
        # Append user and AI messages to chat history
        session["chat_history"].append({"role": "User", "message": user_input})
        session["chat_history"].append({"role": "AI", "message": ai_response})
        
        # Debugging: Print chat history after appending
        print(f"Updated chat history: {session['chat_history']}")

        # Make sure session changes are saved
        session.modified = True

        return redirect(url_for("chat"))

    # Debugging: Print the chat history to ensure it's being passed correctly
    print(f"Chat history at render: {session['chat_history']}")

    return render_template("chat.html", chat_history=session["chat_history"])

@app.route("/clear")
def clear_chat():
    session.pop("chat_history", None)
    return redirect(url_for("chat"))

if __name__ == "__main__":
    app.run(debug=True)
