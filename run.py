from app import app, db


if __name__ == '__main__':
	with app.app_context():
		db.drop_all()
		db.create_all()
	app.run(host=app.config['APP_HOST'], port=app.config['APP_PORT'])
	