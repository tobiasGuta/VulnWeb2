from flask import Flask, abort, render_template_string
import hashlib

app = Flask(__name__)

# Simple "database"
USERS = {
    1: {"username": "admin", "email": "admin@vulnapp.local"},
    2: {"username": "alice", "email": "alice@vulnapp.local"},
    3: {"username": "bob", "email": "bob@vulnapp.local"},
    123: {"username": "testuser", "email": "test@vulnapp.local"},
}

def md5_hash_id(user_id):
    return hashlib.md5(str(user_id).encode()).hexdigest()

def get_user_by_hash(hash_id):
    for uid, user in USERS.items():
        if md5_hash_id(uid) == hash_id:
            return uid, user
    return None, None

BASE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>HashedID App</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f0f2f5;
            margin: 0; padding: 0;
        }
        .container {
            width: 70%%;
            margin: 50px auto;
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1, h2 {
            color: #34495e;
        }
        ul { list-style: none; padding: 0; }
        li { margin: 10px 0; }
        a.button {
            display: inline-block;
            margin-top: 20px;
            padding: 8px 16px;
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
def home():
    example_id = 123
    example_hash = md5_hash_id(example_id)
    content = f"""
        <h1>Welcome to HashedID App</h1>
        <p>Access your profile using a URL like:</p>
        <code>/profile/{example_hash}</code>
        <p>Where the hashed ID is the MD5 hash of your numeric ID.</p>
        <p>Example: User ID <b>{example_id}</b> → MD5 hash <b>{example_hash}</b></p>
        <p>Try changing the hash in the URL to access other profiles.</p>
    """
    return BASE_HTML % content

@app.route("/profile/<hash_id>")
def profile(hash_id):
    user_id, user = get_user_by_hash(hash_id)
    if user is None:
        abort(404)

    content = f"""
        <h2>👤 Profile ID: {user_id}</h2>
        <ul>
            <li><b>Username:</b> {user['username']}</li>
            <li><b>Email:</b> {user['email']}</li>
        </ul>
        <a class="button" href="/">Home</a>
    """
    return BASE_HTML % content

if __name__ == "__main__":
    app.run(debug=True)
