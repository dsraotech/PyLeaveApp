from flask import Flask, request, redirect, url_for, session, render_template,jsonify
from flask_ldap3_login import LDAP3LoginManager, AuthenticationResponseStatus
import ldap3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure key

# LDAP Configuration
app.config['LDAP_HOST'] = 'ldap://192.168.0.9'
app.config['LDAP_BASE_DN'] = 'ou=users,DC=EFFTRONICS,DC=LOCAL'
app.config['LDAP_BIND_USER'] = 'cn=dsubbarao,DC=EFFTRONICS,DC=LOCAL'
app.config['LDAP_BIND_PASSWORD'] = 'Dsrao@111'

# Initialize LDAP Manager
ldap_manager = LDAP3LoginManager(app)
# ldap_manager.init_config({
#     'LDAP_HOST': LDAP_HOST,
#     'LDAP_BASE_DN': LDAP_BASE_DN,
#     'LDAP_BIND_USER': LDAP_BIND_USER,
#     'LDAP_BIND_PASSWORD': LDAP_BIND_PASSWORD,
#     'LDAP_USER_OBJECT_FILTER': '(sAMAccountName=%(username)s)'  # Adjust filter as per your LDAP schema
# })
def search_user(username):
    # Set up the server and connection
    server = ldap3.Server(app.config['LDAP_HOST'], get_info=ldap3.ALL)
    conn = ldap3.Connection(
        server,
        user=app.config['LDAP_BIND_USER'],
        password=app.config['LDAP_BIND_PASSWORD'],
        auto_bind=True
    )

    # Define the search filter and attributes to retrieve
    search_filter = f"(&(objectClass=person)(sAMAccountName={username}))"
    search_attributes = ['cn', 'memberOf']

    # Perform the search
    conn.search(
        search_base=app.config['LDAP_BASE_DN'],
        search_filter=search_filter,
        attributes=search_attributes
    )

    # Retrieve and return the user entry
    if conn.entries:
        user_entry = conn.entries[0]
        return user_entry.entry_to_json()
    else:
        return None

@app.route('/search_user/<username>', methods=['GET'])
def get_user(username):
    user_info = search_user(username)
    if user_info:
        return jsonify(user_info), 200
    else:
        return jsonify({"error": "User not found"}), 404

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
