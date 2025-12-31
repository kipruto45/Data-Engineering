from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from elections.models import Election, Position, Candidate
from voting.models import EncryptedVote
from voting.tally import simple_tally
from voting.crypto import generate_rsa_keypair, tally_private_key_path, tally_public_key_path, sign_with_tally_private, verify_with_tally_public


class TallyFlowTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="voter1", password="testpass")
        now = timezone.now()
        self.election = Election.objects.create(
            name="Tally Election",
            start_time=now - timezone.timedelta(hours=1),
            end_time=now + timezone.timedelta(hours=1),
            is_published=True,
        )
        self.position = Position.objects.create(election=self.election, name="President")
        self.cand_a = Candidate.objects.create(position=self.position, name="Alice", approved=True)
        self.cand_b = Candidate.objects.create(position=self.position, name="Bob", approved=True)

    def test_simple_tally_counts(self):
        # create encrypted votes (payloads can be any strings)
        EncryptedVote.objects.create(election=self.election, position=self.position, candidate=self.cand_a, encrypted_payload="a1")
        EncryptedVote.objects.create(election=self.election, position=self.position, candidate=self.cand_a, encrypted_payload="a2")
        EncryptedVote.objects.create(election=self.election, position=self.position, candidate=self.cand_b, encrypted_payload="b1")

        results = simple_tally(self.election)
        self.assertEqual(results.get(self.cand_a.id), 2)
        self.assertEqual(results.get(self.cand_b.id), 1)

    def test_tally_signature(self):
        # generate keys then sign payload
        generate_rsa_keypair(private_path=None, public_path=None)
        generate_rsa_keypair(private_path=tally_private_key_path(), public_path=tally_public_key_path())
        EncryptedVote.objects.create(election=self.election, position=self.position, candidate=self.cand_a, encrypted_payload="a1")
        results = simple_tally(self.election)
        payload = str(results).encode("utf-8")
        sig = sign_with_tally_private(payload)
        self.assertTrue(verify_with_tally_public(payload, sig))
