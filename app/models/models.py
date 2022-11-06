from app.models import db
from datetime import datetime

class Test(db.Model):
	__tablename__ = "tb_test"
	id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
	text = db.Column(db.Text, nullable=True)


class User(db.Model):
	__tablename__ = "tb_user"
	userid = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
	openid = db.Column(db.String(255), nullable=False, unique=True)
	nickName = db.Column(db.String(255), nullable=False)
	avatarUrl = db.Column(db.String(255), nullable=False)
	gender = db.Column(db.Integer, nullable=True)
	contact = db.Column(db.String(255), nullable=True)
	pass

# 暂时不用这个了，请忽视
class Message(db.Model):
	__tablename__ = "tb_message"
	msgId = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	description = db.Column(db.String(255), nullable=False)
	contact = db.Column(db.String(255), nullable=False)
	pictureUrl = db.Column(db.String(255), nullable=False)
	msgClass = db.Column(db.Integer, nullable=False)
	pass


class Goods(db.Model):
	__tablename__ = "tb_goods"
	goodsId = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)

	name = db.Column(db.String(255), nullable=False)
	description = db.Column(db.String(1023), nullable=False)
	category = db.Column(db.Integer, nullable=False)  # 商品小类别
	price = db.Column(db.Integer, nullable=False)
	state = db.Column(db.Integer, nullable=False)  # 商品状态（0有货，1已有人要，2已售出）

	pictureUrl = db.Column(db.String(255), nullable=False)
	contact = db.Column(db.String(255), nullable=False)

	releaseTime = db.Column(db.DateTime, default=datetime.now, nullable = False, index = True)
	pass

class Release(db.Model):
	__tablename__ = "tb_release"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	userId = db.Column(db.Integer, nullable=False)
	pass


class Star(db.Model):
	__tablename__ = "tb_star"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	userId = db.Column(db.Integer, nullable=False)
	pass
