from flask import Flask, request, redirect, url_for, session, render_template
from flask_ldap3_login import LDAP3LoginManager, AuthenticationResponseStatus

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure key

# LDAP Configuration
app.config['LDAP_HOST'] = 'ldap://EFFTRONICS.LOCAL'
app.config['LDAP_BASE_DN'] = 'ou=users,DC=EFFTRONICS,DC=LOCAL'
app.config['LDAP_BIND_USER'] = 'cn=sms,DC=EFFTRONICS,DC=LOCAL'
app.config['LDAP_BIND_PASSWORD'] = 'Efftronics@123'

# Initialize LDAP Manager
ldap_manager = LDAP3LoginManager(app)
# ldap_manager.init_config({
#     'LDAP_HOST': LDAP_HOST,
#     'LDAP_BASE_DN': LDAP_BASE_DN,
#     'LDAP_BIND_USER': LDAP_BIND_USER,
#     'LDAP_BIND_PASSWORD': LDAP_BIND_PASSWORD,
#     'LDAP_USER_OBJECT_FILTER': '(sAMAccountName=%(username)s)'  # Adjust filter as per your LDAP schema
# })

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = ldap_manager.authenticate(username, password)

        if response.status == AuthenticationResponseStatus.success:
            # Authentication successful, store user info in session if needed
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('loginldap.html', error='Invalid credentials')

    return render_template('loginldap.html')

# Protected route example
@app.route('/index')
def index():
    if 'username' in session:
        return f'Hello, {session["username"]}! This is a protected route.'
    else:
        return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
