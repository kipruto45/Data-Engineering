from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from accounts.models import AuthSession, RevokedAccessToken
import uuid


class RevocationMiddlewareTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="u", password="p")
        self.session = AuthSession.objects.create(user=self.user)
        self.revoked = RevokedAccessToken.objects.create(session=self.session, revoked=True)
        self.client = Client()

    def test_request_with_revoked_token_is_blocked(self):
        token = f"{self.revoked.jti}.abc123"
        r = self.client.get("/api/elections/", HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(r.status_code, 401)

    def test_request_with_non_revoked_token_passes(self):
        rtoken = RevokedAccessToken.objects.create(session=self.session, revoked=False)
        token = f"{rtoken.jti}.abc123"
        r = self.client.get("/api/elections/", HTTP_AUTHORIZATION=f"Bearer {token}")
        # May be 401 from authentication (no backend), but should not be 401 due to revoked token
        self.assertNotEqual(r.status_code, 401)
