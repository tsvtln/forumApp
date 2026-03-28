from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from forumApp.posts.models import Post

UserModel = get_user_model()


class TestApprovePostView(TestCase):
    def setUp(self):
        self.user_credentials = {
            'username': 'testUser',
            'email': 'testUser@forumApp.com',
            'password': '21jj@as03#'
        }

        self.user = UserModel.objects.create_user(**self.user_credentials)

        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            approved=False,
            author=self.user,
        )

    def test__approve_valid_post__approves_post_and_redirects_to_index(self):
        self.client.login(
            email=self.user_credentials['email'],
            password=self.user_credentials['password']
        )

        response = self.client.get(reverse(
            'approve', args=[self.post.pk]),
            HTTP_REFERER=reverse('index'),
        )
        self.post.refresh_from_db()

        self.assertTrue(self.post.approved)
        self.assertRedirects(response, reverse('index'))

    def test__approve_invalid_post__raises_DoesNotExists_error(self):
        self.client.login(
            email=self.user_credentials['email'],
            password=self.user_credentials['password']
        )

        with self.assertRaises(self.post.DoesNotExist) as ex:
            response = self.client.get(
                reverse('approve', args=[9999]),
                HTTP__REFERER=reverse('index'),
            )

        self.assertEqual(str(ex.exception), 'Post matching query does not exist.')
