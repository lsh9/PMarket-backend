from app.models import db, User


def add_user(data):
	try:
		nickName = data['nickName']
		avatarUrl = data['avatarUrl']
		gender = data['gender']
		# 没找到openid则创建新用户
		if not db.session.query(User.openid == data['openid']).first():
			db.session.add(User(openid=data['openid'], nickName=nickName, avatarUrl=avatarUrl, gender=gender))
			db.session.commit()
		user_obj = db.session.query(User.openid == data['openid']).first()
		return user_obj.userid
	except Exception as e:
		db.session.rollback()
		print(e)


def query_user(userid):
	user_obj = db.session.query(User.userid == userid).first()
	user = {
		'id': user_obj.userid,
		'nickName': user_obj.nickName,
		'avatarUrl': user_obj.avatarUrl,
		'gender': user_obj.gender,
		'contact': user_obj.contact,
	}
	return user


def update_user(data):
	try:
		db.session.filter(User.userid == data['id']).update(data)
		db.session.commit()
		return True
	except Exception as e:
		db.session.rollback()
		print(e)
		return False
