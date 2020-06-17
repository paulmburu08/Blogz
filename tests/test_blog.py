import unittest
from app.models import Blog,User
from app import db

class BlogModelTest(unittest.TestCase):

    def setUp(self):
        self.user_James = User(username = 'James', email = 'james@ms.com')

        self.new_blog = Blog(title = 'TEST', blog = 'This is a test',category = 'sports')

    def tearDown(self):
        Blog.query.delete()
        User.query.delete()

    def test_save_comment(self):
        self.new_blog.save_blog()
        self.assertTrue(len(Blog.query.all())>0)