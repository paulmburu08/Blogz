import unittest
from app.models import Subscribe,User
from app import db

class SubscribeModelTest(unittest.TestCase):

    def setUp(self):
        self.user_James = User(username = 'James', email = 'james@ms.com')

        self.new_subscriber = Subscribe(email = 'james@ms.com')

    def tearDown(self):
        Subscribe.query.delete()
        User.query.delete()

    def test_save_subscriber(self):
        self.new_subscriber.save_subscriber()
        self.assertTrue(len(Subscribe.query.all())>0)