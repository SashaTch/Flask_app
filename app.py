from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from models import db, User

app = Flask(__name__, static_folder='static', template_folder='templates')

#configuration
db_user=os.getenv('POSTGRES_USER')
db_password=os.getenv('POSTGRES_PASSWORD')
app.secret_key = 'your_secret_key' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@AppDB:5432/pypetdb'.format(db_user, db_password)

#initialize extension
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#routes
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
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            return render_template('login.html', error='Invalid credentials. Please try again.')
        login_user(user)
        return redirect(url_for('main_page'))

    elif action == "Sign Up":
        if User.query.filter_by(username=username).first() is not None:
            return render_template('login.html', error='Username already exists.')
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main_page'))

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
    with app.app_context():
        db.create_all() #used only in development level
    app.run(host='0.0.0.0', port=5000, debug=True)
