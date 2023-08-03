from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__, static_folder='static', template_folder='templates')

#app.secret_key = 'your_secret_key' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'  # For demonstration purposes. You should choose a secure persistent storage.

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_page.html'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login_submit():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            return render_template('login.html', error='Invalid credentials. Please try again.')

        login_user(user)
        return redirect(url_for('main_page.html'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first() is not None:
            return render_template('register.html', error='Username already exists.')

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/main_page')
@login_required
def main_page():
    return render_template('main_page.html', username=current_user.username)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    db.create_all()  # Creates database tables. Not suitable for a production environment.
    app.run(host='0.0.0.0', port=5000, debug=True)
