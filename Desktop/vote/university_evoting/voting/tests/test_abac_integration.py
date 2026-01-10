from django.test import TestCase, Client
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from unittest.mock import patch

from elections.models import Election, Position, Candidate
from voting.models import VoteToken


class AbacIntegrationTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='voter_abac', password='pass')
        now = timezone.now()
        self.election = Election.objects.create(name='E2', start_time=now - timedelta(hours=1), end_time=now + timedelta(days=1))
        self.position = Position.objects.create(name='P2', election=self.election)
        self.candidate = Candidate.objects.create(name='C2', position=self.position)
        self.client = Client()

    def test_abac_denies_api_cast(self):
        token_obj = VoteToken.objects.create(user=self.user, election=self.election)
        self.client.login(username='voter_abac', password='pass')
        data = {'token': str(token_obj.token), 'position_id': self.position.id, 'candidate_id': self.candidate.id}
        with patch('abac.policy.evaluate', return_value=False):
            res = self.client.post('/api/voting/cast/', data)
            self.assertIn(res.status_code, (400, 403))
        token_obj.refresh_from_db()
        self.assertFalse(token_obj.used)

    def test_abac_allows_api_cast(self):
        token_obj = VoteToken.objects.create(user=self.user, election=self.election)
        self.client.login(username='voter_abac', password='pass')
        data = {'token': str(token_obj.token), 'position_id': self.position.id, 'candidate_id': self.candidate.id}
        with patch('abac.policy.evaluate', return_value=True):
            res = self.client.post('/api/voting/cast/', data)
            self.assertEqual(res.status_code, 201)
        token_obj.refresh_from_db()
        self.assertTrue(token_obj.used)

    def test_abac_denies_qr_cast(self):
        self.client.login(username='voter_abac', password='pass')
        with patch('abac.policy.evaluate', return_value=False):
            res = self.client.get(f'/api/voting/qr/{self.candidate.qr_slug}/')
            self.assertIn(res.status_code, (400, 403))

    def test_abac_allows_qr_cast(self):
        self.client.login(username='voter_abac', password='pass')
        with patch('abac.policy.evaluate', return_value=True):
            res = self.client.get(f'/api/voting/qr/{self.candidate.qr_slug}/')
            self.assertEqual(res.status_code, 201)
