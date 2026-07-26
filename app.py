from flask import Flask, jsonify, request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from extension import db
from flask import render_template


app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)

from routes.auth import auth
from routes.tasks import tasks

app.register_blueprint(auth)
app.register_blueprint(tasks)

@app.route('/login')
def ui():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')    


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)