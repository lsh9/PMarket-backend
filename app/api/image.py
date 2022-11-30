from flask import Blueprint, request, Response, current_app
import os
image_bp = Blueprint("image_bp", __name__)


@image_bp.route('/image/upload/<by>', methods=["POST"])
def upload_image(by):
	""" 从微信上传图片，返回可访问图片的url

	:param by: 图片上传的来源：[avatar, goods]
	:return: url字符串
	"""
	try:
		if by not in ['avatar', 'goods']:
			return 'not found', 404
		path = f"images/{by}/"
		# 从微信获取图片
		image_file = request.files.get("image")
		filename = image_file.filename
		last = request.form.get("last")
		# 删除旧图片
		if last and os.path.exists(path + last):
			os.remove(path + last)
		image_file.save(path + filename)
		url = current_app.config['HTTP_SERVER'] + f"/image/{by}/{filename}"
		return url
	except Exception as e:
		print("ERROR:", e)
		return 'not found', 404


@image_bp.route('/image/<by>/<filename>', methods=["GET"])
def download_image(by, filename):
	""" 返回路径image/by/filename的图片
	此路由用于在微信显示图片，也可在网页打开

	:param by: 图片来源：[avatar, goods]
	:param filename: 图片文件名
	:return:图片
	"""
	if by not in ['avatar', 'goods']:
		return 'not found', 404
	with open(f"images/{by}/{filename}", "rb") as f:
		img = f.read()
	return Response(img, mimetype="image")
