from flask import request, jsonify, Blueprint 
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models.users import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    username = request.json.get("username")
    password = request.json.get("password")

    user = User.query.filter_by(username = username).one_or_none()

    if user is not None:
        return jsonify(message='username exist')

    hashed_password = generate_password_hash(password)

    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify(message='user created')

@auth.route('/login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = User.query.filter_by(username = username).one_or_none()

    if user is not None and check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        response =jsonify(message='success', access_token=access_token)
        return response, 200
    else:
        return jsonify(message='login failed'), 401


