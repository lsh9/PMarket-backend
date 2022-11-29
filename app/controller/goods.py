from app.models import db, Goods, Release, User, Star
from sqlalchemy import or_, and_

# 往tb_goods中添加一条记录data, data是字典
# 同时往release表中插入(goodId,userId)


def add_goods(data, userId):
    try:
        goods = Goods(
            name=data["name"],
            description=data["description"],
            category=data["category"],
            price=data["price"],
            state=data["state"],
            pictureUrl=data["pictureUrl"],
            contact=data["contact"],
        )
        db.session.add(goods)
        db.session.flush()
        goodsId = goods.goodsId

        db.session.add(
            Release(id=goodsId, userId=userId)
        )
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(e)
        return False

# 修改tb_goods中的一条记录data, data中必须有goodsId指明哪个记录
# data中还应该有其他要修改的键值对


def update_goods(data):
    try:
        this_goods = Goods.query.filter_by(goodsId=data['goodsId']).first()
        for k, v in data.items():
            if k == 'name':
                this_goods.name = v
            elif k == 'description':
                this_goods.description = v
            elif k == 'category':
                this_goods.category = v
            elif k == 'price':
                this_goods.price = v
            elif k == 'state':
                this_goods.state = v
            elif k == 'pictureUrl':
                this_goods.pictureUrl = v
            elif k == 'contact':
                this_goods.contact = v
            else:
                continue
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(e)
        return False


def delete_goods(goodsId):
    try:
        goods = Goods.query.get(goodsId)
        release = Release.query.get(goodsId)
        db.session.delete(goods)
        db.session.delete(release)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(e)
        return False

# 从goodsId开始，递减地查询limit个条目
# 若goodsId == -1. 直接时间倒序的前limit个


def query_goods_by_id_and_limit(goodsId,  limit):
    try:
        if goodsId == -1:
            # 时间倒序返回前limit个条目
            goods = Goods.query.order_by(Goods.goodsId.desc()).limit(limit).all()
        else:
            # 从goodsId开始的前limit个条目，即[goodsId-limit+1, goodsId]
            goods = Goods.query.filter(Goods.goodsId <= goodsId).order_by(Goods.goodsId.desc()).limit(limit).all()
        goods_list = [
            {
                "type": 0,
                "goodsId": data.goodsId,
                "name": data.name,
                "description": data.description,
                "category": data.category,
                "price": data.price,
                "state": data.state,
                "pictureUrl": data.pictureUrl,
                "contact": data.contact,
                "releaseTime": str(data.releaseTime)
            }
            for data in goods
        ]

        return goods_list
    except Exception as e:
        db.session.rollback()
        print(e)
        return False

# 返回category指定的类别的商品
# 从goodsId开始，递减地查询limit个条目
# 若goodsId == -1. 直接时间倒序的前limit个


def query_category_by_id_and_limit(category, goodsId, limit):
    try:
        if goodsId == -1:
            # 时间倒序返回前limit个条目
            goods = Goods.query.filter(Goods.category == category).order_by(Goods.goodsId.desc()).limit(limit).all()
        else:
            # 从goodsId开始的前limit个条目，即[goodsId-limit+1, goodsId]
            goods = Goods.query.filter(Goods.category == category, Goods.goodsId <=
                                       goodsId).order_by(Goods.goodsId.desc()).limit(limit).all()
        goods_list = [
            {
                "type": 0,
                "goodsId": data.goodsId,
                "name": data.name,
                "description": data.description,
                "category": data.category,
                "price": data.price,
                "state": data.state,
                "pictureUrl": data.pictureUrl,
                "contact": data.contact,
                "releaseTime": str(data.releaseTime)
            }
            for data in goods
        ]

        return goods_list
    except Exception as e:
        db.session.rollback()
        print(e)
        return False


def query_goods_detail(goodsId):
    try:
        data = Goods.query.filter(Goods.goodsId == goodsId).first()
        goods = {
            "type": 0,
            "goodsId": data.goodsId,
            "name": data.name,
            "description": data.description,
            "category": data.category,
            "price": data.price,
            "state": data.state,
            "pictureUrl": data.pictureUrl,
            "contact": data.contact,
            "releaseTime": str(data.releaseTime)
        }
        userId = Release.query.filter(Release.id == goodsId).first().userId
        user_obj = User.query.filter(User.userid == userId).first()

        user = {
            'id': user_obj.userid,
            'nickName': user_obj.nickName,
            'avatarUrl': user_obj.avatarUrl,
            'gender': user_obj.gender,
            'contact': user_obj.contact,
        }
        return {
            'Goods': goods, 'User': user
        }
    except Exception as e:
        db.session.rollback()
        print(e)
        return False


def search_goods(keywords, limit=666):
    try:
        result_dict = {}
        for word in keywords:
            goods = Goods.query.filter(or_(Goods.name.contains(
                word), Goods.description.contains(word))).order_by(Goods.goodsId.desc()).all()
            for data in goods:
                result_dict[data.goodsId] = {
                    "type": 0,
                    "goodsId": data.goodsId,
                    "name": data.name,
                    "description": data.description,
                    "category": data.category,
                    "price": data.price,
                    "state": data.state,
                    "pictureUrl": data.pictureUrl,
                    "contact": data.contact,
                    "releaseTime": str(data.releaseTime)
                }

        return [v for v in result_dict.values()][:limit]
    except Exception as e:
        db.session.rollback()
        print(e)
        return False


def show_all():
    goods = Goods.query.all()
    goods_list = [
        {
            "type": 0,
            "goodsId": data.goodsId,
            "name": data.name,
            "description": data.description,
            "category": data.category,
            "price": data.price,
            "state": data.state,
            "pictureUrl": data.pictureUrl,
            "contact": data.contact,
            "releaseTime": str(data.releaseTime)
        }
        for data in goods
    ]
    return goods_list


def insert_fake_data():
    userId_ls = ["openid_2", "openid_3", "openid_1"]
    name_ls = ["一眼顶真", "鉴定为", "一眼定镇"]
    description_ls = ["顶针同款", "顶针代言", "顶针"]
    category_ls = [1, 2, 0]
    price_ls = [21, 32, 2220]
    state_ls = [0, 1, 2]
    pictureUrl_ls = ["https://blog.csdn.net/", "http://dingzhen.com/index/12.jpg", "https://dingzhen.com/index/122.jpg"
                     ]
    contact_ls = ["QQ: 1233443", "vx: dingzhen_ks", "vx:dingzhen_pku"]
    for i in range(10):
        for name, description, category, price, state, pictureUrl, contact, userId in zip(name_ls, description_ls, category_ls, price_ls, state_ls, pictureUrl_ls, contact_ls, userId_ls):
            add_goods(
                {
                    "name": name,
                    "description": description,
                    "category": category,
                    "price": price,
                    "state": state,
                    "pictureUrl": pictureUrl,
                    "contact": contact,
                }, userId
            )


def test_update():
    update_goods(
        {
            "goodsId": 2,
            "name": "燕园顶针"
        }
    )


def add_likes_goods(goodsId, userId):
    # 添加收藏商品
    try:
        db.session.add(
            Star(id=goodsId, userId=userId)
        )
        db.session.commit()
        # for i in Star.query.filter(Star.userId == userId):
        #     print(i.id)
        #     print(i.userId)
        return True
    except Exception as e:
        db.session.rollback()
        print(e)
        return False


def query_likes_goods(userId, goodsId, limit):
    # 获取收藏的商品
    try:
        if goodsId == -1:
            # 时间倒序返回前 limit 个条目
            likes = Star.query.filter(Star.userId == userId).order_by(Star.id.desc()).limit(limit).all()
            likes_goods = []
            for star in likes:
                likes_goods.append(Goods.query.filter(Goods.goodsId == star.id).first())
        else:
            # 从 goodsId 开始的前 limit 个条目，即 [goodsId - limit + 1, goodsId]
            likes = Star.query.filter(Star.userId == userId, Star.id <=
                                      goodsId).order_by(Star.id.desc()).limit(limit).all()
            likes_goods = []
            for star in likes:
                likes_goods.append(Goods.query.filter(Goods.goodsId == star.id).first())
        goods_list = [
            {
                "type": 0,
                "goodsId": data.goodsId,
                "name": data.name,
                "description": data.description,
                "category": data.category,
                "price": data.price,
                "state": data.state,
                "pictureUrl": data.pictureUrl,
                "contact": data.contact,
                "releaseTime": str(data.releaseTime)
            }
            for data in likes_goods
        ]
        # for i in goods_list:
        #     print(i)
        return goods_list
    except Exception as e:
        db.session.rollback()
        print(e)
        return False


def query_release_goods(userId, goodsId, limit):
    # 获取发布的商品
    try:
        if goodsId == -1:
            # 时间倒序返回前 limit 个条目
            release = Release.query.filter(Release.userId == userId).order_by(Release.id.desc()).limit(limit).all()
            release_goods = []
            for item in release:
                release_goods.append(Goods.query.filter(Goods.goodsId == item.id).first())
        else:
            # 从 goodsId 开始的前 limit 个条目，即 [goodsId - limit + 1, goodsId]
            release = Release.query.filter(Release.userId == userId, Release.id <=
                                           goodsId).order_by(Release.id.desc()).limit(limit).all()
            release_goods = []
            for item in release:
                release_goods.append(Goods.query.filter(Goods.goodsId == item.id).first())
        goods_list = [
            {
                "type": 0,
                "goodsId": data.goodsId,
                "name": data.name,
                "description": data.description,
                "category": data.category,
                "price": data.price,
                "state": data.state,
                "pictureUrl": data.pictureUrl,
                "contact": data.contact,
                "releaseTime": str(data.releaseTime)
            }
            for data in release_goods
        ]
        # for i in goods_list:
        #     print(i)
        return goods_list
    except Exception as e:
        db.session.rollback()
        print(e)
        return False
