from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from accounts.models import Profile, AuthSession, RefreshToken
from audit.models import AuditLog


class RefreshTokenRotationTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="alice", password="password")
        Profile.objects.create(user=self.user, role="student", status=Profile.STATUS_ACTIVE)
        self.client = APIClient()

    def test_login_and_refresh_rotate(self):
        resp = self.client.post("/api/auth/login/", {"identifier": "alice", "password": "password"}, format="json")
        self.assertEqual(resp.status_code, 200)
        refresh = resp.data.get("refresh_token")
        self.assertIsNotNone(refresh)
        # use refresh to get new tokens
        r2 = self.client.post("/api/auth/refresh/", {"refresh_token": refresh}, format="json")
        self.assertEqual(r2.status_code, 200)
        new_refresh = r2.data.get("refresh_token")
        self.assertIsNotNone(new_refresh)
        # old token should now be rotated; another use of old should revoke sessions
        r3 = self.client.post("/api/auth/refresh/", {"refresh_token": refresh}, format="json")
        self.assertEqual(r3.status_code, 401)
        # sessions revoked
        self.assertTrue(AuthSession.objects.filter(user=self.user, revoked=True).exists())
        # audit logged
        self.assertTrue(AuditLog.objects.filter(user=self.user, action="refresh_token_reuse_detected").exists())

    def test_invalid_secret_revokes_session(self):
        resp = self.client.post("/api/auth/login/", {"identifier": "alice", "password": "password"}, format="json")
        refresh = resp.data.get("refresh_token")
        # tamper with secret
        tampered = refresh.split('.')[0] + '.tamperedsecret'
        r = self.client.post("/api/auth/refresh/", {"refresh_token": tampered}, format="json")
        self.assertEqual(r.status_code, 401)
        self.assertTrue(AuthSession.objects.filter(user=self.user, revoked=True).exists())
        # audit logged
        self.assertTrue(AuditLog.objects.filter(user=self.user, action="invalid_refresh_token").exists())
