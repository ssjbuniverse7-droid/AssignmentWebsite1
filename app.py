from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Assignment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Database

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)

    # Relationship to scores
    scores = db.relationship('Score', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

class Score(db.Model):
    __tablename__ = "scores"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Score {self.score} (User {self.user_id})>"


# Pages

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signup')
def form():
    return render_template("signup.html")

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/leaderboard')
def leaderboard():

    scores = Score.query.all()

    return render_template('leaderboard.html', scores=scores)

@app.route("/puzzle1")
def puzzle1():
    return render_template('puzzle1.html')

@app.route("/puzzle2")
def puzzle2():
    return render_template('puzzle2.html')

@app.route("/puzzle3")
def puzzle3():
    return render_template('puzzle3.html')

@app.route("/puzzle4")
def puzzle4():
    return render_template('puzzle4.html')

@app.route("/puzzle5")
def puzzle5():
    return render_template('puzzle5.html')

@app.route("/help")
def help():
    return render_template('help.html')

@app.route("/congrats1")
def congrats1():
    return render_template("congrats1.html")

# Helper functions
"""@app.route('/check-user-result', methods=['POST'])
def check_user_result():
    didUserPass = True"""

@app.route('/add-score', methods=['POST'])
def add_score():

    new_score = Score (
        user_id = request.form.get("user_id"),
        score = 1
    )

    db.session.add(new_score)
    db.session.commit()

    return redirect(url_for('congrats1'))

@app.route('/add-username', methods=['POST'])
def add_username():
    print("Adding Username")

    username = request.form.get("username")
    password = request.form.get("pwd")

    user = User(username=username)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('puzzle1'))



if __name__ == "__main__":
    app.run(debug=True)