import os
import unittest

from config import basedir
from app import app, db
from app.models import User

class TestCase(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
		self.app = app.test_client()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_avatar(self):
		u = User(nickname='toolzark', email='toolzark@gmail.com')
		avatar = u.avatar(128)
		expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
		assert avatar[0:len(expected)] == expected

	def test_make_unique_nickname(self):
		u = User(nickname='toolzark', email='toolzark@gmail.com')
		db.session.add(u)
		db.session.commit()
		nickname = User.make_unique_nickname('toolzark')
		assert nickname != 'toolzark'
		u = User(nickname=nickname, email='piapalen@gmail.com')
		db.session.add(u)
		db.session.commit()
		nickname2 = User.make_unique_nickname('toolzark')
		assert nickname2 != 'toolzark'
		assert nickname2 != nickname

if __name__ == '__main__':
	unittest.main()