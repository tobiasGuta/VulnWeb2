from flask import Flask, request, redirect, url_for, render_template_string, abort
import base64
import json

app = Flask(__name__)

# Simulated database
USERS = {
    1: {"username": "admin", "email": "admin@vulnapp.local"},
    2: {"username": "alice", "email": "alice@vulnapp.local"},
    3: {"username": "bob", "email": "bob@vulnapp.local"},
    10: {"username": "hacker", "email": "hacker@vulnapp.local"},
    30: {"username": "testuser", "email": "test@vulnapp.local"},
}

# 🔥 Default user to show on home
DEFAULT_USER_ID = 30

# 🧪 Minimal CSS styling
BASE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>EncodedID App</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f5f5f5;
            margin: 0; padding: 0;
        }
        .container {
            width: 80%%;
            margin: 50px auto;
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1, h2 {
            color: #2c3e50;
        }
        ul { list-style: none; padding: 0; }
        li { margin: 10px 0; }
        a.button {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background: #3498db;
            color: white;
            border-radius: 5px;
            text-decoration: none;
        }
        a.button:hover {
            background: #2980b9;
        }
    </style>
</head>
<body>
    <div class="container">
        %s
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    # 🔁 Redirect to default profile view
    encoded = base64.b64encode(json.dumps({"id": DEFAULT_USER_ID}).encode()).decode()
    return redirect(url_for('profile', encoded_id=encoded))

@app.route("/profile/<encoded_id>")
def profile(encoded_id):
    try:
        # Decode base64 → JSON
        json_data = base64.b64decode(encoded_id).decode("utf-8")
        user_data = json.loads(json_data)

        # Extract ID and fetch user
        user_id = int(user_data["id"])
        user = USERS.get(user_id)

        if not user:
            abort(404)

        content = f'''
            <h1>Welcome to EncodedID App</h1>
            <h2>👤 Profile ID: {user_id}</h2>
            <ul>
                <li><b>Username:</b> {user["username"]}</li>
                <li><b>Email:</b> {user["email"]}</li>
            </ul>
            <a class="button" href="/">Home</a>
        '''
        return BASE_HTML % content

    except Exception as e:
        return BASE_HTML % f"<h1>Error</h1><p>{str(e)}</p><a class='button' href='/'>Go Back</a>", 400

if __name__ == "__main__":
    app.run(debug=True)
