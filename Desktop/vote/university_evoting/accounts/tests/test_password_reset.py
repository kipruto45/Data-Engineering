from django.test import TestCase, Client
from django.contrib.auth import get_user_model


class PasswordResetTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='pruser', email='pr@example.com', password='oldpass')
        self.client = Client()

    def test_password_reset_flow_by_username(self):
        res = self.client.post('/api/accounts/password/reset/request/', {'username': 'pruser'})
        self.assertEqual(res.status_code, 201)
        token = res.json().get('token')
        self.assertIsNotNone(token)

        # confirm reset
        res2 = self.client.post('/api/accounts/password/reset/confirm/', {'token': token, 'new_password': 'newpass123'})
        self.assertEqual(res2.status_code, 200)

        # can authenticate with new password
        login = self.client.post('/api/accounts/login/', {'identifier': 'pruser', 'password': 'newpass123'})
        self.assertIn(login.status_code, (200, 201))

    def test_password_reset_flow_by_email(self):
        res = self.client.post('/api/accounts/password/reset/request/', {'username': 'pr@example.com'})
        self.assertEqual(res.status_code, 201)
        token = res.json().get('token')
        self.assertIsNotNone(token)

        res2 = self.client.post('/api/accounts/password/reset/confirm/', {'token': token, 'new_password': 'anotherpass'})
        self.assertEqual(res2.status_code, 200)
