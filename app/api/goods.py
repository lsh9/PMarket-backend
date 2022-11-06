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
	userId = data['userId']
	if add_goods(data, userId):
		return {'code': 0}
	return {'code': 1}
