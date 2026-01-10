from django.test import TestCase, Client
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from unittest.mock import patch

from elections.models import Election, Position, Candidate
from audit.models import AuditLog


class AuditLoggingTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='auditor', password='pass')
        now = timezone.now()
        self.election = Election.objects.create(name='E3', start_time=now - timedelta(hours=1), end_time=now + timedelta(days=1))
        self.position = Position.objects.create(name='P3', election=self.election)
        self.candidate = Candidate.objects.create(name='C3', position=self.position)
        self.client = Client()

    def test_qr_scan_creates_audit_log(self):
        res = self.client.get(f'/api/voting/qr/scan/{self.candidate.qr_slug}/')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(AuditLog.objects.filter(action='qr.scan').exists())

    def test_qr_confirm_cast_creates_success_audit(self):
        # login and perform confirm post which triggers _do_cast and audit entry
        self.client.login(username='auditor', password='pass')
        with patch('abac.policy.evaluate', return_value=True):
            res = self.client.post(f'/api/voting/qr/confirm/{self.candidate.qr_slug}/')
            # expect redirect to success page
            self.assertIn(res.status_code, (302, 200))

        self.assertTrue(AuditLog.objects.filter(user=self.user, action='qr.cast_success').exists())
