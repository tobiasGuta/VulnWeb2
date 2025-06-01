from flask import Flask, request, session, redirect, url_for, render_template_string
import random
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace this in prod

# Fake user DB
users = {
    'user': {'password': 'userpass', 'role': 'user'},
    'admin': {'password': 'adminpass', 'role': 'admin'}
}

otp_store = {}
login_attempts = {}
otp_attempts = {}

# Configs
MAX_LOGIN_ATTEMPTS = 5
LOGIN_TIMEOUT = 300  # 5 min lockout

MAX_OTP_ATTEMPTS = 3
OTP_TIMEOUT = 60  # 1 min lockout

# HTML templates + styles
base_style = '''
<style>
  body {
    background: #121212;
    color: #eee;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
  }
  .container {
    background: #1f1f1f;
    padding: 2.5rem 3rem;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.7);
    width: 340px;
    text-align: center;
  }
  h2 {
    margin-bottom: 2rem;
    color: #00d8ff;
    text-transform: uppercase;
    letter-spacing: 1.5px;
  }
  input[type="text"],
  input[type="password"],
  input[type="number"] {
    width: 100%;
    padding: 0.75rem 1rem;
    margin-bottom: 1.3rem;
    border-radius: 8px;
    border: 2px solid #2b2b2b;
    background: #222;
    color: #eee;
    font-size: 1rem;
    transition: border-color 0.3s ease, background-color 0.3s ease;
    font-family: inherit;
    box-sizing: border-box;
  }
  input[type="text"]:focus,
  input[type="password"]:focus,
  input[type="number"]:focus {
    outline: none;
    border-color: #00d8ff;
    background: #1a1a1a;
  }
  input[type="submit"] {
    width: 100%;
    padding: 0.75rem 0;
    background: #00d8ff;
    color: #121212;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    font-size: 1.1rem;
    cursor: pointer;
    transition: background-color 0.25s ease;
    font-family: inherit;
    box-sizing: border-box;
  }
  input[type="submit"]:hover {
    background: #009ecc;
  }
  label {
    font-size: 0.9rem;
    color: #aaa;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 10px;
    user-select: none;
  }
  input[type="checkbox"] {
    width: 16px;
    height: 16px;
    cursor: pointer;
  }
</style>
'''

login_page = base_style + '''
<div class="container">
  <h2>Login</h2>
  <form method="POST">
    <input name="username" type="text" placeholder="Username" required autocomplete="username">
    <input name="password" type="password" placeholder="Password" required autocomplete="current-password">
    <input type="submit" value="Login">
  </form>
</div>
'''

otp_page = base_style + '''
<div class="container">
  <h2>Enter OTP</h2>
  <form method="POST">
    <input name="otp" type="number" placeholder="OTP" required autocomplete="one-time-code" inputmode="numeric" pattern="[0-9]*">
    <label><input name="remember_device" type="checkbox"> Remember this device</label>
    <input type="submit" value="Verify">
  </form>
</div>
'''

dashboard_page = base_style + '''
<div class="container">
  <h2>Welcome, {{username}}!</h2>
  <p>Role: {{role}}</p>
</div>
'''

def is_locked(user_dict, max_attempts, timeout):
    now = time.time()
    if user_dict.get('count', 0) >= max_attempts:
        if now - user_dict.get('last_attempt', 0) < timeout:
            return True
        else:
            user_dict['count'] = 0  # Reset after timeout
    return False

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)

        if username not in login_attempts:
            login_attempts[username] = {'count': 0, 'last_attempt': 0}

        if is_locked(login_attempts[username], MAX_LOGIN_ATTEMPTS, LOGIN_TIMEOUT):
            return "Too many login attempts. Wait 5 minutes.", 429

        if user and user['password'] == password:
            session['username'] = username
            session['role'] = user['role']

            if session.get('trusted_device'):
                session['authenticated'] = True
                return redirect(url_for('dashboard'))

            otp = str(random.randint(100, 999))
            otp_store[username] = otp
            otp_attempts[username] = {'count': 0, 'last_attempt': 0}
            print(f"[DEBUG] OTP for {username}: {otp}")  # Remove in prod
            return redirect(url_for('otp'))
        else:
            login_attempts[username]['count'] += 1
            login_attempts[username]['last_attempt'] = time.time()
            return "Invalid login", 401

    return render_template_string(login_page)

@app.route('/otp', methods=['GET', 'POST'])
def otp():
    username = session.get('username')
    if not username or username not in otp_store:
        return redirect(url_for('login'))

    if username not in otp_attempts:
        otp_attempts[username] = {'count': 0, 'last_attempt': 0}

    if request.method == 'POST':
        current_time = time.time()

        otp_input = request.form.get('otp', '').strip()
        remember_device = request.form.get('remember_device') == 'on'

        # Check rate limit ONLY if remember_device is ON
        if remember_device and is_locked(otp_attempts[username], MAX_OTP_ATTEMPTS, OTP_TIMEOUT):
            return "Too many OTP attempts. Try again in 60 seconds.", 429

        if not otp_input:
            return "Missing OTP", 400

        if otp_input == otp_store.get(username):
            session['authenticated'] = True
            if remember_device:
                session['trusted_device'] = True

            otp_store.pop(username, None)
            otp_attempts.pop(username, None)
            return redirect(url_for('dashboard'))
        else:
            # Increase fail count ONLY if remember_device is ON
            if remember_device:
                otp_attempts[username]['count'] += 1
                otp_attempts[username]['last_attempt'] = current_time

            # If remember_device empty, no fail count increment (unlimited tries)
            return "Invalid OTP", 401

    return render_template_string(otp_page)

@app.route('/dashboard')
def dashboard():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    return render_template_string(dashboard_page, username=session['username'], role=session['role'])

if __name__ == '__main__':
    app.run(debug=True)
