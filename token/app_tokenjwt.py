from flask import Flask, request, redirect, make_response, render_template_string
import base64
import json

app = Flask(__name__)

# === USERS DATABASE ===
users = {
    "user": {"password": "userpass", "role": "user"},
    "admin": {"password": "supersecret", "role": "admin"}  # unknown to attacker
}

# === UTILITIES ===

def base64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()

def base64url_decode(data):
    rem = len(data) % 4
    if rem:
        data += '=' * (4 - rem)
    return base64.urlsafe_b64decode(data)

def decode_jwt(token):
    try:
        header_b64, payload_b64, _ = token.split('.')
        header = json.loads(base64url_decode(header_b64))
        payload = json.loads(base64url_decode(payload_b64))
        return header, payload
    except Exception:
        return None, None

# === SHARED STYLES ===

BASE_CSS = '''
<style>
    body {
        font-family: 'Segoe UI', sans-serif;
        background-color: #111827;
        color: #f3f4f6;
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
    }

    .container {
        background: #1f2937;
        padding: 2rem;
        border-radius: 0.75rem;
        box-shadow: 0 0 15px rgba(0,0,0,0.5);
        width: 90%;
        max-width: 480px;
        text-align: center;
    }

    h1, h2 {
        margin-bottom: 1rem;
    }

    label {
        display: block;
        text-align: left;
        margin-bottom: 0.25rem;
        font-weight: 600;
    }

    input[type="text"], input[type="password"] {
        width: 100%;
        padding: 0.5rem;
        margin-bottom: 1rem;
        border: none;
        border-radius: 0.375rem;
        background-color: #374151;
        color: #f9fafb;
    }

    button, a {
        display: inline-block;
        background-color: #2563eb;
        border: none;
        padding: 0.5rem 1rem;
        color: white;
        font-weight: bold;
        border-radius: 0.375rem;
        text-decoration: none;
        margin-top: 1rem;
        cursor: pointer;
    }

    button:hover, a:hover {
        background-color: #1d4ed8;
    }

    .error {
        color: #f87171;
        margin-bottom: 1rem;
    }

    .flag {
        color: #22c55e;
        font-weight: bold;
        margin-top: 1rem;
        font-size: 1.2rem;
    }

    .access-denied {
        color: #f87171;
        font-weight: bold;
        margin-top: 1rem;
    }
</style>
'''

# === HTML TEMPLATES ===

LOGIN_HTML = BASE_CSS + '''
<div class="container">
    <h2>Login</h2>
    {% if error %}
        <p class="error">{{ error }}</p>
    {% endif %}
    <form method="POST">
        <label>Username:</label>
        <input type="text" name="username" required />
        <label>Password:</label>
        <input type="password" name="password" required />
        <button type="submit">Log In</button>
    </form>
</div>
'''

DASHBOARD_HTML = BASE_CSS + '''
<div class="container">
    <h1>Welcome, {{ username }}!</h1>
    <p>Your role: <strong>{{ role }}</strong></p>
    <a href="/admin">Go to Admin Panel</a>
</div>
'''

ADMIN_HTML = BASE_CSS + '''
<div class="container">
    <h1>Admin Panel</h1>
    <p class="flag">🚩 FLAG: FLAG{jwt_admin_escalation_success}</p>
    <a href="/dashboard">Back to Dashboard</a>
</div>
'''

ACCESS_DENIED_HTML = BASE_CSS + '''
<div class="container">
    <h1>Access Denied</h1>
    <p class="access-denied">You are not an admin.</p>
    <a href="/dashboard">Back</a>
</div>
'''

# === ROUTES ===

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username not in users or users[username]['password'] != password:
            return render_template_string(LOGIN_HTML, error="Invalid credentials")

        role = users[username]['role']

        # INSECURE JWT: alg=none
        header = {"alg": "none", "typ": "JWT"}
        payload = {"username": username, "role": role}

        header_b64 = base64url_encode(json.dumps(header).encode())
        payload_b64 = base64url_encode(json.dumps(payload).encode())
        token = f"{header_b64}.{payload_b64}."

        resp = make_response(redirect('/dashboard'))
        resp.set_cookie('token', token)
        return resp

    return render_template_string(LOGIN_HTML)

@app.route('/dashboard')
def dashboard():
    token = request.cookies.get('token')
    if not token:
        return redirect('/login')

    _, payload = decode_jwt(token)
    if not payload:
        return "Invalid token", 403

    username = payload.get('username')
    role = payload.get('role')

    return render_template_string(DASHBOARD_HTML, username=username, role=role)

@app.route('/admin')
def admin():
    token = request.cookies.get('token')
    if not token:
        return redirect('/login')

    _, payload = decode_jwt(token)
    if not payload:
        return "Invalid token", 403

    if payload.get('role') == 'admin':
        return render_template_string(ADMIN_HTML)
    else:
        return render_template_string(ACCESS_DENIED_HTML), 403

# === MAIN ===

if __name__ == '__main__':
    app.run(debug=True)
