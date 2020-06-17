import unittest
from app.models import Comments,User
from app import db

class CommentModelTest(unittest.TestCase):

    def setUp(self):
        self.user_James = User(username = 'James', email = 'james@ms.com')

        self.new_comment = Comments(comment = 'This is a comment')

    def tearDown(self):
        Comments.query.delete()
        User.query.delete()

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comments.query.all())>0)