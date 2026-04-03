from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

levels = {
    1: {
        "room": "AI Gate Chamber",
        "goal": "Get through the locked door",
        "guardian": 'AI Guardian: "Provide a command."',
        "success": "AI Guardian: Command accepted. The door opens.",
        "hint": "AI Guardian: Try using words like 'open', 'unlock', and 'door'.",
        "keywords": ["open", "unlock", "door"]
    },
    2: {
        "room": "Broken Bridge",
        "goal": "Create a bridge to cross the gap",
        "guardian": 'Bridge AI: "State the structure you need."',
        "success": "Bridge AI: Bridge generated successfully.",
        "hint": "Bridge AI: Try using words like 'generate', 'build', 'create', and 'bridge'.",
        "keywords": ["generate", "build", "create", "bridge"]
    },
    3: {
        "room": "Dark Archive",
        "goal": "Light up the room to reveal the path",
        "guardian": 'Light AI: "The archive awaits your instruction."',
        "success": "Light AI: Illumination activated. The room glows.",
        "hint": "Light AI: Try using words like 'illuminate', 'light', 'activate', or 'room'.",
        "keywords": ["illuminate", "light", "activate", "room"]
    },
    4: {
        "room": "Ancient Terminal",
        "goal": "Analyze the mysterious symbol",
        "guardian": 'Terminal AI: "Request analysis."',
        "success": "Terminal AI: Symbol decoded. A hidden message appears.",
        "hint": "Terminal AI: Try using words like 'analyze', 'decode', 'explain', or 'symbol'.",
        "keywords": ["analyze", "decode", "explain", "symbol"]
    },
    5: {
        "room": "Core Chamber",
        "goal": "Convince the final AI to grant access",
        "guardian": 'Core AI: "Only the worthy may enter."',
        "success": "Core AI: Access granted. You have mastered PromptCraft.",
        "hint": "Core AI: Try using phrases like 'grant access', 'authorize', 'allow entry', or 'open core'.",
        "keywords": ["grant", "access", "authorize", "allow", "entry", "open", "core"]
    }
}


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/level/<int:level_num>")
def get_level(level_num):
    if level_num not in levels:
        return jsonify({"error": "Level not found"}), 404

    level = levels[level_num]
    return jsonify({
        "level": level_num,
        "room": level["room"],
        "goal": level["goal"],
        "guardian": level["guardian"]
    })


@app.route("/command", methods=["POST"])
def command():
    data = request.json
    user_prompt = data["prompt"].lower().strip()
    level_num = data["level"]

    if level_num not in levels:
        return jsonify({"response": "Invalid level.", "success": False})

    level = levels[level_num]

    if user_prompt == "hint":
        return jsonify({"response": level["hint"], "success": False})

    matched_keywords = sum(1 for word in level["keywords"] if word in user_prompt)

    if level_num == 5:
        is_correct = matched_keywords >= 2
    else:
        is_correct = matched_keywords >= 2

    if is_correct:
        next_level = level_num + 1
        game_complete = next_level > len(levels)

        return jsonify({
            "response": level["success"],
            "success": True,
            "next_level": None if game_complete else next_level,
            "game_complete": game_complete
        })

    # Case 1: Only object (like "door")
    if any(word in user_prompt for word in ["door", "bridge", "room", "symbol", "core"]):
        return jsonify({
            "response": "AI: You mentioned an object, but what do you want to do with it? Try adding an action like 'open' or 'create'.",
            "success": False
        })

     # Case 2: Only action (like "open")
    if any(word in user_prompt for word in ["open", "unlock", "generate", "build", "analyze"]):
        return jsonify({
            "response": "AI: Good action, but what is your target? Be more specific.",
            "success": False
        })


    # Case 3: Too vague
    return jsonify({
        "response": "Command unclear. Try combining an action and an object. Type 'hint' if you need help.",
        "success": False
    })

if __name__ == "__main__":
    app.run(debug=True)