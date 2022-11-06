from flask import Blueprint, request, Response, current_app
import hashlib
import base64
image_bp = Blueprint("image_bp", __name__)


@image_bp.route('/image/upload/<by>', methods=["POST"])
def upload_img(by):
	try:
		if by not in ['avatar', 'goods']:
			return {'code': 1}

		image_BYTE = base64.b64decode(request.form.get("image"))
		path = f"images/{by}/"
		imageId = hashlib.md5(str(image_BYTE).encode('utf-8')).hexdigest()
		with open(path + imageId, "wb") as f:
			f.write(image_BYTE)
		url = current_app.config['HTTP_SERVER'] + f"/image/{by}/{imageId}"
		return {'url': url}
	except Exception as e:
		print("ERROR:", e)
		return {'code': 1}


@image_bp.route('/image/<by>/<imageId>', methods=["GET"])
def image(by, imageId):
	with open("images/{}/{}".format(by, imageId), "rb") as f:
		img = f.read()
	return Response(img, mimetype="image")
