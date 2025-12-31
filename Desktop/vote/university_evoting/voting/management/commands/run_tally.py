from django.core.management.base import BaseCommand
from elections.models import Election
from voting.tally import simple_tally
from voting.crypto import sign_with_tally_private
import json


class Command(BaseCommand):
    help = "Run tally for an election and print JSON results (signed)"

    def add_arguments(self, parser):
        parser.add_argument("election_id", type=int)

    def handle(self, *args, **options):
        eid = options["election_id"]
        election = Election.objects.get(id=eid)
        results = simple_tally(election)
        payload = json.dumps({"election": election.id, "results": results})
        signature = None
        try:
            signature = sign_with_tally_private(payload.encode("utf-8"))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Signing not available: {e}"))
        output = {"payload": results, "signature": signature}
        self.stdout.write(json.dumps(output))
