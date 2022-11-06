from flask import Blueprint, request, Response, current_app
import hashlib

image_bp = Blueprint("image_bp", __name__)


@image_bp.route('/image/upload/<by>', methods=["POST"])
def upload_img(by):
	if by == 'avatar':
		pass
	elif by == 'goods':
		pass
	else:
		return None
	data = request.json
	image_BYTE = data.get('image')
	path = f"images/{by}/"
	imageId = hashlib.md5(str(image_BYTE).encode('utf-8')).hexdigest()
	with open(path + imageId, "wb") as f:
		f.write(image_BYTE)
	url = current_app.config['HTTP_SERVER'] + f"/image/{by}/{imageId}"
	return url


@image_bp.route('/image/<imageId>', methods=["GET"])
def image(imageId):
	with open("images/{}".format(imageId), "rb") as f:
		img = f.read()
	return Response(img, mimetype="image")
