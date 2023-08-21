from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__, static_folder='static', template_folder='templates')

# Hardcoded admin user
class AdminUser:
    def __init__(self):
        self.id = 1
        self.username = "admin"
        self.password = "password"  # You might want to change this
        self.authenticated = False

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def check_password(self, password):
        return self.password == password

# Configuration
app.secret_key = 'your_secret_key'

# Initialize extension
login_manager = LoginManager()
login_manager.init_app(app)
admin_user = AdminUser()

@login_manager.user_loader
def load_user(user_id):
    if int(user_id) == admin_user.id:
        return admin_user
    return None

# Routes
@app.route('/')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    return render_template('login.html')

@app.route('/process', methods=['POST'])
def process():
    username = request.form['username']
    password = request.form['password']
    action = request.form['action']

    if action == "Sign In":
        if username == admin_user.username and admin_user.check_password(password):
            admin_user.authenticated = True
            login_user(admin_user)
            return redirect(url_for('main_page'))
        else:
            return render_template('login.html', error='Invalid credentials. Please try again.')
    else:
        return redirect(url_for('login'))

@app.route('/main_page')
@login_required
def main_page():
    return render_template('main_page.html', username=current_user.username)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
