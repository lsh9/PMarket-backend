from app.models import db, Goods

def add_goods(data):
	try:
		db.session.add(Goods(goodsId = data["goodsId"],
                            name = data["name"],
                            description = data["description"],
                            goodsClass = data["goodsClass"],
                            price = data["price"],
                            state = data["state"],
                            pictureUrl =data["pictureUrl"],
                            contact = data["contact"]
        ))
		db.session.commit()
		return True
	except Exception as e:
		db.session.rollback()
		print(e)
		return False

