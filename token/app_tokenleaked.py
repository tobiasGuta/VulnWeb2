from flask import Flask, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey123'  # for session management

users = {
    "admin@hackme.com": {"password": "supersecure", "role": "admin"},
    "user@hackme.com": {"password": "password123", "role": "user"}
}

reset_tokens = {}

def generate_token(email):
    return f"token-for-{email}"  # ✅ Clean, reusable token

# Common CSS to inject into pages
COMMON_CSS = """
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: #121212;
        color: #eee;
        display: flex;
        justify-content: center;
        align-items: flex-start;
        height: 100vh;
        margin: 0;
        padding: 2rem;
    }
    .container {
        background: #1f1f1f;
        padding: 2rem 3rem;
        border-radius: 10px;
        width: 400px;
        box-shadow: 0 0 10px #00ffccaa;
    }
    h1, h2 {
        color: #00ffcc;
        margin-bottom: 1rem;
    }
    a {
        color: #00ffcc;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    form {
        display: flex;
        flex-direction: column;
    }
    input[type=email], input[type=password], input[type=text] {
        padding: 10px;
        margin-bottom: 1rem;
        border-radius: 5px;
        border: none;
        outline: none;
        font-size: 1rem;
    }
    button {
        background: #00ffcc;
        border: none;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        cursor: pointer;
        transition: background 0.3s ease;
    }
    button:hover {
        background: #00cc99;
    }
    ul {
        padding-left: 1.2rem;
    }
    li {
        margin-bottom: 0.5rem;
    }
    #responseMessage {
        margin-top: 1rem;
        font-weight: bold;
        color: #66ff99;
    }
</style>
"""

@app.route('/')
def home():
    if 'email' in session:
        user = users.get(session['email'])
        if user['role'] == 'admin':
            return COMMON_CSS + f'''
            <div class="container">
                <h1>Welcome Admin!</h1>
                <p>Here is your secret flag: <code>FLAG{{logic_flaw_is_real}}</code></p>
                <a href="/logout">Logout</a>
            </div>
            '''
        else:
            return COMMON_CSS + f'''
            <div class="container">
                <h1>Welcome {session["email"]}!</h1>
                <p>You are logged in as a normal user.</p>
                <a href="/logout">Logout</a>
            </div>
            '''
    return COMMON_CSS + '''
    <div class="container">
        <h1>Welcome to hackme Website</h1>
        <a href="/login">Login</a> | <a href="/reset_password">Reset Password</a>
        <br><br>
        <ul>
            <li>Normal user credentials <strong>user@hackme.com</strong> / <strong>password123</strong></li>
        </ul>
    </div>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return COMMON_CSS + '''
        <div class="container">
            <h2>Login</h2>
            <form method="POST">
                Email: <input name="email" type="email" required />
                Password: <input name="password" type="password" required />
                <button type="submit">Login</button>
            </form>
        </div>
        '''
    email = request.form.get('email')
    password = request.form.get('password')

    user = users.get(email)
    if user and user['password'] == password:
        session['email'] = email
        return redirect(url_for('home'))
    else:
        return COMMON_CSS + '''
        <div class="container">
            <p style="color:#ff5555;">Invalid credentials.</p>
            <a href="/login">Try again</a>
        </div>
        '''

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

@app.route('/reset_password', methods=['GET'])
def reset_password_form():
    return COMMON_CSS + '''
    <div class="container">
        <h2>Reset Password</h2>
        <form id="resetForm">
            Enter your email: <input name="email" type="email" required />
            <button type="submit">Reset</button>
        </form>
        <div id="responseMessage"></div>
        <script>
        document.getElementById('resetForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(e.target);
            const res = await fetch('/reset_password', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            document.getElementById('responseMessage').innerText = data.message;
            // Token is leaked but NOT shown here
        });
        </script>
    </div>
    '''

@app.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.form.get('email')

    if email in users:
        token = generate_token(email)
        reset_tokens[token] = email
        response = {
            "message": "If your email exists, a password reset token has been sent.",
            "reset_token": token  # Visible only via intercept tools
        }
    else:
        response = {
            "message": "If your email exists, a password reset token has been sent."
        }

    return jsonify(response)

@app.route('/confirm_reset', methods=['GET', 'POST'])
def confirm_reset():
    if request.method == 'GET':
        return COMMON_CSS + '''
        <div class="container">
            <h2>Confirm Password Reset</h2>
            <form method="POST">
                Reset Token: <input name="token" type="text" required />
                New Password: <input name="new_password" type="password" required />
                <button type="submit">Confirm Reset</button>
            </form>
        </div>
        '''

    token = request.form.get('token')
    new_password = request.form.get('new_password')

    email = reset_tokens.get(token)
    if not email:
        return COMMON_CSS + '''
        <div class="container">
            <p style="color:#ff5555;">Invalid or expired token.</p>
            <a href="/reset_password">Try again</a>
        </div>
        '''

    users[email]['password'] = new_password
    # del reset_tokens[token]  # 🔁 Reusable token: do not delete it

    return COMMON_CSS + f'''
    <div class="container">
        <p>Password reset successful for <strong>{email}</strong>.</p>
        <a href="/login">Login now</a>
    </div>
    '''

if __name__ == '__main__':
    app.run(debug=True)
