from flask import Blueprint, request
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
        return {'code': 1}
    return detail


@goods_bp.route('/goods/publish', methods=["POST"])
def goods_publish():  # put application's code here
    data = request.json
    this_goods = {
        "name": data["name"],
        "description": data["description"],
        "category": int(data["category"]),
        "price": int(data["price"]),
        "state": 0,
        "pictureUrl": data["pictureUrl"],
        "contact": data["contact"]
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


# 添加用户收藏
@goods_bp.route('/goods/addLikesGoods', methods=["POST"])
def goods_addLikesGoods():
    NOTINLIKES = 1  # 之前未被收藏过
    INLIKES = 2  # 之前被收藏过
    data = request.json
    goodsId = int(data['goodsId'])
    userId = data['id']
    # print(data)
    # print("User ID ", userId)
    judge = add_likes_goods(goodsId, userId)
    if judge == NOTINLIKES:
        return {'code': 0}
    elif judge == INLIKES:
        return {'code': 2}
    else:
        return {'code': 1}


# 请求得到用户收藏的商品列表
@goods_bp.route('/goods/getLikesGoods', methods=["GET"])
def goods_getLikesGoods():
    userid = request.args.get('id')  # 用户 id
    beginNo = int(request.args.get('beginNo'))  # 一个 int，代表当前请求的第一个商品号，-1 为最新
    number = int(request.args.get('number'))  # 一个 int，代表请求的商品数
    goods_list = query_likes_goods(userid, beginNo, number)
    if type(goods_list) == bool:
        return {'code': 1}
    return goods_list


# 请求得到用户发布的商品列表
@goods_bp.route('/goods/getReleaseGoods', methods=["GET"])
def goods_getReleaseGoods():
    userid = request.args.get('id')  # 用户 id
    beginNo = int(request.args.get('beginNo'))  # 一个 int，代表当前请求的第一个商品号，-1 为最新
    number = int(request.args.get('number'))  # 一个 int，代表请求的商品数
    goods_list = query_release_goods(userid, beginNo, number)
    if type(goods_list) == bool:
        return {'code': 1}
    return goods_list
