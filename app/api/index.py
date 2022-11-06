from flask import Blueprint,request
from app.controller import *

index_bp = Blueprint("index_bp", __name__)


@index_bp.route('/index')
def index():  # put application's code here
	return 'index'


# 获取beginNo开始的时间倒序的number个商品信息
@index_bp.route('/index/getGoods', methods=["GET"])
def index_getGoods():  
	beginNo = int(request.args.get('beginNo'))
	number = int(request.args.get('number'))
	goods_list = query_goods_by_id_and_limit(beginNo, number)
	# print(goods_list)
	if type(goods_list) == bool:
		return {'code': 1}
	return goods_list