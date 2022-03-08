from flask import (
    Blueprint, 
    make_response, 
    render_template, 
    request
)
from datetime import timedelta
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required
)
from passlib.hash import pbkdf2_sha256

from models.user import User

from utils.errors import DBConnectionException, MailException, MissingParameterException
from utils.custom_enums import Status

user = Blueprint('user',__name__, url_prefix='/')

USER_ALREADY_EXISTS = "A user with the username {} already exists."
EMAIL_ALREADY_EXISTS = "A user with the email {} already exists."
INVALID_CREDENTIALS = "Invalid credentials!"
PASSWORD_NOT_MATCH = "Passwords are not matching"
NOT_CONFIRMED_ERROR = "You have not confirmed registration, Kindly check your email <{}>."
USER_NOT_FOUND = "User not found."
USER_CONFIRMED = "User is confirmed."
FAILED_TO_CREATE = "Internal Server Error."
SUCCESS_REGISTER_MESSAGE = " Account created successfully.\n An email with an activation link has been sent to your email address.\n Kindly check and confirm it."

@user.route("/signup", methods=['POST'])
def register():
    try:
        data = request.get_json()
        if "username" not in data.keys():
            raise MissingParameterException("username")
        elif "password" not in data.keys():
            raise MissingParameterException("password")
        elif "confirm_password" not in data.keys():
            raise MissingParameterException("confirm password")
    except MissingParameterException as miss:
        return {
            "msg":miss.message
        }, 401

    if data["password"] != data["confirm_password"]:
        return {
            "msg":PASSWORD_NOT_MATCH
        }

    try:   
        if User.find_by_name(data["username"]):
            return {
                "msg":USER_ALREADY_EXISTS.format(data["username"])
            }, 400
        if User.find_by_email(data["email"]):
            return {
                "msg":EMAIL_ALREADY_EXISTS.format(data['email'])
            }
    except DBConnectionException as e:
        return {"msg":e.message}, 500

    user = User(name=data["username"],email= data["email"], password=pbkdf2_sha256.hash(data['password']))
    try:
        user.save_to_db()
        user = User.find_by_name(data["username"])
        #user.send_confirmation_mail()
        return {
            "msg":SUCCESS_REGISTER_MESSAGE,
            "data":user.get_json()
        }, 201
    except DBConnectionException as e:
        return {"msg":e.message}, 500
    except MailException as m:
        return {"msg":e.message}, 500


@user.route("/login",methods=['POST'],)
def login():
    try:
        data = request.get_json()
        if "username" not in data.keys():
            raise MissingParameterException("username")
        elif "password" not in data.keys():
            raise MissingParameterException("password")
    except MissingParameterException as miss:
        return {
            "msg":miss.message
        }, 401

    try:
        user = User.find_by_name(name=data['username'])
    except DBConnectionException as e:
        return {"msg":e.message}

    if user and pbkdf2_sha256.verify(data["password"], user.password):
        if user.activated:
            access_token = create_access_token(
                identity=user.id,
                fresh=True,
                expires_delta=timedelta(minutes=15)
            )
            refresh_token = create_refresh_token(
                identity=user.id,
                expires_delta=timedelta(days=5)
            )
            return {
                "access_token":access_token,
                "refresh_token":refresh_token
            }, 200
        return {"msg":NOT_CONFIRMED_ERROR.format(user.email)}, 400
    return {"msg":INVALID_CREDENTIALS}, 401

@user.route("/token-refresh", methods=['POST'])
@jwt_required(refresh=True)
def token_refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(
        identity=current_user,
        fresh=False
    )
    return {
        "access_token":new_token
    }, 200


@user.route("/forgot-password", methods=['POST'])
def forgot_password():
    return {"msg":"forgot-password"}

@user.route("/reset-password", methods=['POST'])
def reset_password():
    return {"msg":"reset-password"}

@user.route("/user_conf/<string:user_id>")
def user_confirm(user_id):
    user = User.find_by_id(user_id)
    if user is None:
        return {"message": USER_NOT_FOUND}, 404
    
    user.activated = True
    user.save_to_db()
    headers = {"Content-Type":"text/html"}
    return make_response(
        render_template(
            "confirmation_page.html", 
            email= user.username
        ),
        200, headers)