from flask import Blueprint, request, Response, current_app
import hashlib

image_bp = Blueprint("image_bp", __name__)


@image_bp.route('/image/upload/<by>', methods=["POST"])
def upload_img(by):
	try:
		if by not in ['avatar', 'goods']:
			return 'not found', 404
		image_file = request.files.get("image")
		filetype = image_file.filename.rsplit('.')[-1]
		filename = hashlib.md5(str(image_file.stream).encode('utf-8')).hexdigest()
		path = f"images/{by}/"
		filename = filename + "." + filetype
		image_file.save(path + filename)
		url = current_app.config['HTTP_SERVER'] + f"/image/{by}/{filename}"
		return url
	except Exception as e:
		print("ERROR:", e)
		return 'not found', 404


@image_bp.route('/image/<by>/<imageId>', methods=["GET"])
def image(by, imageId):
	with open("images/{}/{}".format(by, imageId), "rb") as f:
		img = f.read()
	return Response(img, mimetype="image")
