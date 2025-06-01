from flask import Flask, request, redirect, session, render_template_string
import uuid

app = Flask(__name__)
app.secret_key = 'dev'

# Simulated in-memory DB
users = {}

# Base template with style
base_style = '''
<!DOCTYPE html>
<html>
<head>
    <title>IDOR Demo</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 0;
        }
        .container {
            width: 90%%;
            max-width: 600px;
            margin: 50px auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
        }
        h1, h2 {
            text-align: center;
            color: #333;
        }
        p, label, input, a {
            font-size: 1rem;
        }
        code {
            background: #eee;
            padding: 2px 4px;
            border-radius: 4px;
        }
        input[type="text"], input[type="submit"] {
            width: 100%%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 6px;
        }
        input[type="submit"] {
            background-color: #007BFF;
            color: white;
            cursor: pointer;
        }
        a {
            color: #007BFF;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .note {
            background: #fffae6;
            border-left: 4px solid #ffc107;
            padding: 10px;
            margin-top: 20px;
            font-size: 0.95rem;
        }
    </style>
</head>
<body>
    <div class="container">
        %s
    </div>
</body>
</html>
'''

register_page = base_style % '''
    <h2>Register</h2>
    <form method="POST">
        <label>Username:</label>
        <input name="username" type="text" required><br>
        <input type="submit" value="Register">
    </form>
    <p><a href="/">Back to home</a></p>
'''

login_page = base_style % '''
    <h2>Login</h2>
    <form method="POST">
        <label>Username:</label>
        <input name="username" type="text" required><br>
        <input type="submit" value="Login">
    </form>
    <p><a href="/">Back to home</a></p>
'''

profile_page = base_style % '''
    <h2>Welcome {{ username }}</h2>
    <p><strong>Your UUID:</strong> <code>{{ user_id }}</code></p>
    <p>View your profile at: <a href="/view/{{ user_id }}">/view/{{ user_id }}</a></p>
    <div class="note">
        <strong>Try it:</strong> Replace the UUID in the URL to check if you can view other users' profiles.
    </div>
    <p><a href="/">Back to home</a></p>
'''

view_page = base_style % '''
    <h2>Profile View</h2>
    <p><strong>Username:</strong> {{ username }}</p>
    <p><strong>User ID:</strong> {{ user_id }}</p>
    <div class="note">
        This page is accessible to <strong>anyone</strong> who knows the UUID — <code>no authorization checks</code> in place!
    </div>
    <p><a href="/">Back to home</a></p>
'''

@app.route('/')
def index():
    return base_style % '''
        <h1>IDOR Demo App</h1>
        <p>This app is <strong>intentionally vulnerable</strong> to demonstrate IDOR with unpredictable UUIDs.</p>
        <p><a href="/register">Register</a> | <a href="/login">Login</a></p>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        user_id = str(uuid.uuid4())
        users[user_id] = {'username': username}
        session['user_id'] = user_id
        return redirect('/profile')
    return render_template_string(register_page)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        for uid, u in users.items():
            if u['username'] == username:
                session['user_id'] = uid
                return redirect('/profile')
        return base_style % '<h2>User not found.</h2><p><a href="/login">Try again</a></p>'
    return render_template_string(login_page)

@app.route('/profile')
def profile():
    uid = session.get('user_id')
    if uid and uid in users:
        return render_template_string(profile_page, username=users[uid]['username'], user_id=uid)
    return redirect('/login')

# 🚨 Classic IDOR bug: No access control on UUIDs
@app.route('/view/<uuid:user_id>')
def view(user_id):
    uid = str(user_id)
    if uid in users:
        return render_template_string(view_page, username=users[uid]['username'], user_id=uid)
    return base_style % '<h2>User not found.</h2><p><a href="/">Back to home</a></p>', 404

if __name__ == '__main__':
    app.run(debug=True)
