from django.test import TestCase, Client
from django.contrib.auth import get_user_model


class MagicLinkTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='mluser', password='pass')
        self.client = Client()

    def test_request_magic_link_and_verify(self):
        # request magic link
        res = self.client.post('/api/accounts/magic/request/', {'username': 'mluser'})
        self.assertEqual(res.status_code, 201)
        token = res.json().get('token')
        self.assertIsNotNone(token)

        # verify magic link
        res2 = self.client.post('/api/accounts/magic/verify/', {'token': token})
        self.assertEqual(res2.status_code, 200)
        data = res2.json()
        self.assertIn('access_token', data)
        self.assertIn('refresh_token', data)

    def test_invalid_magic_token(self):
        res = self.client.post('/api/accounts/magic/verify/', {'token': 'badtoken'})
        self.assertEqual(res.status_code, 400)