from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__, static_folder='static', template_folder='templates')

app.secret_key = 'your_secret_key'  # Replace with a secret key for session management

# Login route
@app.route('/')
def login():
    if 'username' in session:
        # If the user is already logged in, redirect to the profile page
        return redirect(url_for('main_page'))
    else:
        # If the user is not logged in, render the login template
        return render_template('login.html')

# Login form submission route
@app.route('/login', methods=['POST'])
def login_submit():
    username = request.form['username']
    password = request.form['password']
    
    # Perform authentication check (dummy check, replace with your actual authentication logic)
    if username == 'admin' and password == 'password':
        session['username'] = username
        return redirect(url_for('main_page'))
    else:
        return render_template('login.html', error='Invalid credentials. Please try again.')
        
# Main_page route
@app.route('/main_page')
def profile():
    if 'username' in session:
        # If the user is logged in, render the profile template
        username = session['username']
        return render_template('profile.html', username=username)
    else:
        # If the user is not logged in, redirect to the login page
        return redirect(url_for('login'))
# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

