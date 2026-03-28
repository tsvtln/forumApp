
from django.contrib.auth import get_user_model
from django.test import TestCase

UserModel = get_user_model()


class TestUserModel(TestCase):
    def test__valid__str__method(self):
        user = UserModel.objects.create_user(
            username='testUser',
            password='01d09wJWJ(@',
            email='testUser@forumApp.com'
        )

        self.assertEqual(
            str(user),
            user.email
        )
