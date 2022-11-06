from flask import Blueprint, request
from app.controller import *
classify_bp = Blueprint("classify_bp", __name__)


@classify_bp.route('/classify')
def classify():  # put application's code here
	return 'classify'

@classify_bp.route('/classify/getGoodsList', methods=["GET"])
def classify_getGoodsList():  # put application's code here
	categoryId = int(request.args.get('categoryId'))
	beginNo = int(request.args.get('beginNo'))
	number = int(request.args.get('number'))
	goods_list = query_category_by_id_and_limit(categoryId, beginNo, number)
	if type(goods_list) == bool:
		return {'code': 1}
	return goods_list
