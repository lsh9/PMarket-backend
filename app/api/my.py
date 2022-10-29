from flask import Blueprint, request, current_app
import requests
from app.controller import *


my_bp = Blueprint("my_bp", __name__)


@my_bp.route('/my/login', methods=["POST", "GET"])
def my_login():
	try:
		data = request.json
		js_code = data['code']
		response = requests.get(f"https://api.weixin.qq.com/sns/jscode2session?appid={current_app.config['WX_APP_ID']}&secret={current_app.config['WX_APP_SECRET']}&js_code={js_code}&grant_type=authorization_code")
		wx_data = response.json()
		data['openid'] = wx_data['openid']
		userid = add_user(data)
		return {'code': 0, 'id': userid}
	except Exception as e:
		print(e)
		return {'code': 1}


@my_bp.route('/my/info')
def my_info():
	userid = request.json['id']
	return query_user(userid)


@my_bp.route('/my/edit')
def my_edit():
	data = request.json
	if update_user(data):
		return {'code': 0}
	return {'code': 1}

