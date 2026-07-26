from flask import request, jsonify, current_app
from functools import wraps
import jwt
from models import User
from flask import current_app

# Token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        token = token.split(' ')[1]    

        try:
            data = jwt.decode(
                                token,
                                current_app.config['SECRET_KEY'],
                                algorithms=["HS256"]
                            )
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
