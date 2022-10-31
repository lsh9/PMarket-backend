from app.models import db, User
import hashlib


def add_user(data):
	try:
		openid = data['openid']
		nickName = data['nickName']
		avatarUrl = data['avatarUrl']
		gender = data['gender']
		# 没找到openid则创建新用户
		user_obj = db.session.query(User).filter(User.openid == openid).first()
		if not user_obj:
			# 将openid加密，存储为userid
			userid = hashlib.md5(openid.encode('utf-8')).hexdigest()
			db.session.add(User(userid=userid, openid=openid, nickName=nickName, avatarUrl=avatarUrl, gender=gender))
			db.session.commit()
			return userid
		else:
			return user_obj.userid
	except Exception as e:
		db.session.rollback()
		print(e)


def query_user(userid):
	user_obj = db.session.query(User).filter(User.userid == userid).first()
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
		data['userid'] = data['id']
		del data['id']
		db.session.query(User).filter(User.userid == data['userid']).update(data)
		db.session.commit()
		return True
	except Exception as e:
		db.session.rollback()
		print(e)
		return False
