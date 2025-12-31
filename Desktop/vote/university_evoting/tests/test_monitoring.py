from django.test import TestCase, Client


class MonitoringTests(TestCase):
    def test_metrics_endpoint_available(self):
        c = Client()
        r = c.get("/metrics/")
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"no prometheus_client", r.content) or self.assertTrue(r.content)
