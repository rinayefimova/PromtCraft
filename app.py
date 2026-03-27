from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

current_level = 1

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/command", methods=["POST"])
def command():

    user_prompt = request.json["prompt"].lower()

    if current_level == 1:

        if "open" in user_prompt or "unlock" in user_prompt:
            response = "AI Guardian: Command accepted. The door opens."
        elif "hint" in user_prompt:
            response = "AI Guardian: Try using 'open' or 'unlock'."
        else:
            response = "AI Guardian: Command unclear."

    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)