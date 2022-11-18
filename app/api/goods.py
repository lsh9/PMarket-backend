from flask import Blueprint,request
from app.controller import *
goods_bp = Blueprint("goods_bp", __name__)


@goods_bp.route('/goods')
def goods():  # put application's code here
	return 'goods'


@goods_bp.route('/goods/getGoodsId', methods=["GET"])
def goods_getGoodsId():  # put application's code here
	goodsId = request.args.get('goodsId')
	detail = query_goods_detail(goodsId)
	if type(detail) == bool:
		return {'code':1}
	return detail

@goods_bp.route('/goods/publish', methods=["POST"])
def goods_publish():  # put application's code here
	data = request.json
	this_goods = {
		"name" : data["name"],
		"description" : data["description"],
		"category" : int(data["category"]),
		"price" : int(data["price"]),
		"state" : 0,
		"pictureUrl" :data["pictureUrl"],
		"contact" : data["contact"]
	}
	userId = data['userId']
	# print(data)
	# print("User ID ", userId)
	if add_goods(this_goods, userId):
		return {'code': 0}
	return {'code': 1}


@goods_bp.route('/goods/delete', methods=["POST"])
def goods_delete():  # put application's code here
	data = request.json
	if delete_goods(data["goodsId"]):
		return {'code': 0}
	return {'code': 1}
