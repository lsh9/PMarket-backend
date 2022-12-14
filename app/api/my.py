from flask import Blueprint, request, current_app
import requests
from app.controller import *


my_bp = Blueprint("my_bp", __name__)


@my_bp.route('/my/login', methods=["POST"])
def my_login():
	try:
		data = request.json
		js_code = data['code']
		# 从wx接口获取openid
		response = requests.get(f"https://api.weixin.qq.com/sns/jscode2session?appid={current_app.config['WX_APP_ID']}&secret={current_app.config['WX_APP_SECRET']}&js_code={js_code}&grant_type=authorization_code")
		wx_data = response.json()
		data['openid'] = wx_data['openid']
		userid = query_userid_by_openid(data['openid'])
		if not userid:
			userid = add_user(data)
		return {'code': 0, 'id': userid}
	except Exception as e:
		print(e)
		return {'code': 1}


@my_bp.route('/my/info', methods=["GET"])
def my_info():
	userid = request.args.get('id')
	return query_user(userid)


@my_bp.route('/my/edit', methods=["POST"])
def my_edit():
	data = request.json
	if update_user(data):
		return {'code': 0}
	return {'code': 1}

