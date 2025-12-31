from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.utils import timezone
from elections.models import Election, Position
from accounts.models import Profile


class PositionAPITests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="normal", password="pass")
        Profile.objects.create(user=self.user, role="student", status=Profile.STATUS_ACTIVE)
        self.admin = User.objects.create_user(username="admin", password="pass")
        Profile.objects.create(user=self.admin, role="admin", status=Profile.STATUS_ACTIVE)
        self.client = APIClient()
        now = timezone.now()
        self.election = Election.objects.create(name="Test", start_time=now, end_time=now + timezone.timedelta(hours=1), is_published=True)
        Position.objects.create(election=self.election, name="President")

    def test_list_positions_requires_auth(self):
        r = self.client.get(f"/api/elections/{self.election.id}/positions/")
        # depending on auth backend CSRF behavior this may be 401 or 403
        self.assertIn(r.status_code, (401, 403))
        self.client.login(username="normal", password="pass")
        r2 = self.client.get(f"/api/elections/{self.election.id}/positions/")
        self.assertEqual(r2.status_code, 200)
        self.assertTrue(len(r2.data) >= 1)

    def test_create_requires_admin(self):
        self.client.login(username="normal", password="pass")
        r = self.client.post(f"/api/elections/{self.election.id}/positions/", {"name": "VP"}, format="json")
        self.assertEqual(r.status_code, 403)
        self.client.logout()
        self.client.login(username="admin", password="pass")
        r2 = self.client.post(f"/api/elections/{self.election.id}/positions/", {"name": "VP"}, format="json")
        self.assertEqual(r2.status_code, 201)
        pid = r2.data.get("id")
        # update via admin
        r3 = self.client.put(f"/api/elections/{self.election.id}/positions/{pid}/", {"name": "VP Updated"}, format="json")
        self.assertEqual(r3.status_code, 200)
        self.assertEqual(r3.data.get("name"), "VP Updated")
        # delete
        r4 = self.client.delete(f"/api/elections/{self.election.id}/positions/{pid}/")
        self.assertEqual(r4.status_code, 204)
