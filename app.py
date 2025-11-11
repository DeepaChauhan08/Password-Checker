from flask import Flask, render_template, request
import re

app = Flask(__name__)

def check_password_strength(password):
    criteria = {
        "length": len(password) >= 8,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "number": bool(re.search(r"[0-9]", password)),
        "special": bool(re.search(r"[@$!%*?&#]", password))
    }

    score = sum(criteria.values())

    if score == 5:
        level = "Very Strong 💪"
        color = "green"
    elif score == 4:
        level = "Strong ✅"
        color = "blue"
    elif score == 3:
        level = "Medium ⚠️"
        color = "#e6b800"
    elif score == 2:
        level = "Weak ❌"
        color = "orange"
    else:
        level = "Very Weak 🚫"
        color = "red"

    suggestions = []
    if not criteria["length"]:
        suggestions.append("Use at least 8 characters.")
    if not criteria["uppercase"]:
        suggestions.append("Add at least one uppercase letter (A–Z).")
    if not criteria["lowercase"]:
        suggestions.append("Add at least one lowercase letter (a–z).")
    if not criteria["number"]:
        suggestions.append("Include at least one number (0–9).")
    if not criteria["special"]:
        suggestions.append("Add one special symbol like @, #, $, %, or &.")

    return score, criteria, level, color, suggestions

@app.route("/", methods=["GET", "POST"])
def index():
    strength = None
    criteria = {}
    suggestions = []
    level = None
    color = None
    password = ""

    if request.method == "POST":
        password = request.form["password"]
        strength, criteria, level, color, suggestions = check_password_strength(password)

    return render_template("index.html",
                           strength=strength,
                           criteria=criteria,
                           level=level,
                           color=color,
                           suggestions=suggestions,
                           password=password)

if __name__ == "__main__":
    app.run(debug=True)
