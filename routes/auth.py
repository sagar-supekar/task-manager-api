from flask import Blueprint, request, jsonify,current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid
from datetime import datetime, timezone, timedelta
from models import User
from extension import db


auth = Blueprint('auth', __name__)

@auth.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    hashed_password = generate_password_hash(password)  # fix 1

    new_user = User(
        public_id=str(uuid.uuid4()),
        name=name,
        email=email,
        password=hashed_password  # fix 2
    )

    db.session.add(new_user)  # fix 3
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


@auth.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()  # fix 4

    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid email or password'}), 401  # fix 5

    token = jwt.encode(
        {
            'public_id': user.public_id,
            'exp': datetime.now(timezone.utc) + timedelta(hours=1)
        },
        current_app.config['SECRET_KEY'],
        algorithm="HS256"
    )

    return jsonify({'token': token}), 200  # fix 6