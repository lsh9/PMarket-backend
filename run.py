from app import app, db


if __name__ == '__main__':
	with app.app_context():
		# 如果对models有修改，则drop_all重新create_all
		# db.drop_all()
		db.create_all()
	app.run(host=app.config['APP_HOST'], port=app.config['APP_PORT'])
	