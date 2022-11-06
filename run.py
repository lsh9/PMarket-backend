from app import app, db
from app.controller import query_category_by_id_and_limit, insert_fake_data, query_goods_detail

if __name__ == '__main__':
	with app.app_context():
		# 如果对models有修改，则drop_all重新create_all
		db.drop_all()
		db.create_all()
		insert_fake_data()
	app.run(host=app.config['APP_HOST'], port=app.config['APP_PORT'])
	