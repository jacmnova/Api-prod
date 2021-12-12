from datetime import datetime, timedelta

from flask import Blueprint, request
from function_jwt import write_token, validate_token, write_token_web
from flask import jsonify
import users


routes_auth = Blueprint("routes_auth", __name__)


@routes_auth.route("/api/login/mobile", methods=["POST"])
def loginMobile():
    data = request.get_json()
    print(data)
    login = users.verify_user(data['username'], data['password'])
    if login:
        days = 1
        if data["session"] == True:
            days = 30

        data = users.get_data_user(data['username'])
        print(data)
        token = str(write_token(data, days)).split("'")[1]
        validate_token(token)
        return jsonify({
            'token': str(write_token(data, days)).split("'")[1],
            'data': data,
            'name': data['name'],
            'username': data['username'],
            'access_token': token,
            'refresh_token': '',
            'roles': data['role_user'],
            'avatar': '',
            'tempPassword': data['temp_password'],
            'isDoctor': data['isDoctor'],
            'doctor': data['doctor_id'],
            'terms': data['terms_condition']
        })
    else:
        response = jsonify({"message": "User not found"})
        response.status_code = 401
        return response


@routes_auth.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    login = users.verify_user(data['username'], data['password'])
    if login:
        minutes = 10
        data = users.get_data_user(data['username'])
        now = datetime.now()
        exp = now + timedelta(days=0, minutes=minutes)
        token = str(write_token_web(data)).split("'")[1]
        # print(validate_token(token, True))
        return jsonify({
            'token': token,
            'data': data,
            'name': data['name'],
            'username': data['username'],
            'access_token': token,
            'refresh_token': '',
            'roles': data['role_user'],
            'avatar': '',
            'tempPassword': data['temp_password'],
            'isDoctor': data['isDoctor'],
            'doctor': data['doctor_id'],
            'terms': data['terms_condition'],
            'expSession': exp
        })
    else:
        response = jsonify({"message": "User not found"})
        response.status_code = 401
        return response

@routes_auth.route("/api/login/updatePassword", methods=['POST'])
def updatePassword():
    token = request.headers["Authorization"].split(" ")[1]
    users.update_password(request.json, token)
    return jsonify({'update': True})

@routes_auth.route("/api/login/terms", methods=['post'])
def terms():
    token = request.headers
    print(token)
    token = request.headers["Authorization"].split(" ")[1]
    users.terms(request.json, token)
    return jsonify({'update': True})

@routes_auth.route("/users/save",  methods=["POST"])
def register():
    users.save_user(request.get_json())
    return jsonify({'detail': True})

@routes_auth.route("/users/get")
def get_users():
    payload = users.get_user()
    return jsonify(payload)

@routes_auth.route("/api/user/getInfoUserById", methods=["POST"])
def get_info_user_by_id():
    info = request.json
    payload = users.get_user_info(info)
    return

@routes_auth.route("/users/resend/<id>")
def resend(id):
    users.resend_pass(id)
    return jsonify({'resend': True})

@routes_auth.route("/users/sendIos/<id>")
def sendIos(id):
    users.sendIos_code(id)
    return jsonify({'resend': True})

@routes_auth.route("/users/delete/<id>", methods=["DELETE"])
def delete_user(id):
    users.delete_user(id)
    return jsonify({'delete': True})




