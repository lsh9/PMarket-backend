from app.models import db, Goods

# 往tb_goods中添加一条记录data, data是字典
def add_goods(data):
	try:
		db.session.add(Goods(
                            name = data["name"],
                            description = data["description"],
                            goodsClass = data["goodsClass"],
                            price = data["price"],
                            state = data["state"],
                            pictureUrl =data["pictureUrl"],
                            contact = data["contact"],
        ))
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
		for k,v in data.items():
			if k == 'name':
				this_goods.name = v;
			elif k == 'description':
				this_goods.description = v;
			elif k == 'goodsClass':
				this_goods.goodsClass = v;
			elif k == 'price':
				this_goods.price = v;
			elif k == 'state':
				this_goods.state = v;
			elif k == 'pictureUrl':
				this_goods.pictureUrl =v;
			elif k == 'contact':
				this_goods.contact =v;
			else:
				continue;
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
				"goodsId" : data.goodsId,
                "name" : data.name,
				"description": data.description,
				"goodsClass" : data.goodsClass,
				"price" : data.price,
				"state" : data.state,
				"pictureUrl" :data.pictureUrl,
				"contact" : data.contact,
				"releaseTime":str(data.releaseTime)
			}
			for data in goods
		]
		
		return goods_list
	except Exception as e:
		db.session.rollback()
		print(e)
		return False

def insert_fake_data():
	name_ls = ["一眼顶真","鉴定为","一眼定镇"]
	description_ls =["顶针同款","顶针代言","顶针"]
	goodsClass_ls=[1,2,0]
	price_ls=[21.2,32.12,20]
	state_ls=[0,1,2]
	pictureUrl_ls=["https://blog.csdn.net/"
				,"http://dingzhen.com/index/12.jpg"
				,"https://dingzhen.com/index/122.jpg"
		]
	contact_ls=["QQ: 1233443","vx: dingzhen_ks","vx:dingzhen_pku"]
	for name, description, goodsClass, price, state, pictureUrl, contact in zip(name_ls, description_ls,goodsClass_ls,price_ls, state_ls, pictureUrl_ls, contact_ls):
		add_goods(
			{
                "name" : name,
				"description": description,
				"goodsClass" : goodsClass,
				"price" : price,
				"state" : state,
				"pictureUrl" :pictureUrl,
				"contact" : contact,
			}
		)
def test_update():
	update_goods(
		{
			"goodsId": 2,
			"name" : "燕园顶针"
		}
	)