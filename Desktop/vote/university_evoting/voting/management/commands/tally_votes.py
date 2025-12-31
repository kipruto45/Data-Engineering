import csv
import io
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from django.utils import timezone
from voting.crypto import decrypt_with_private
from voting.models import EncryptedVote
from reports.models import Report
from elections.models import Election


class Command(BaseCommand):
    help = "Tally votes for an election by decrypting stored votes and producing a report"

    def add_arguments(self, parser):
        parser.add_argument("election_id", type=int, help="ID of the election to tally")
        parser.add_argument("--export", action="store_true", help="Export CSV report and save to Reports")

    def handle(self, *args, **options):
        election_id = options["election_id"]
        election = get_object_or_404(Election, id=election_id)

        votes = EncryptedVote.objects.filter(election=election)

        counts = {}
        total = 0
        invalid = []

        for ev in votes:
            # verify signature if present
            if ev.signature:
                try:
                    ok = verify_with_tally_public(ev.encrypted_payload.encode("utf-8"), ev.signature)
                except Exception as e:
                    invalid.append((ev.id, f"signature verify error: {e}"))
                    continue
                if not ok:
                    invalid.append((ev.id, "signature invalid"))
                    continue

            try:
                pt = decrypt_with_private(ev.encrypted_payload)
            except Exception as e:
                # couldn't decrypt: skip and note
                invalid.append((ev.id, str(e)))
                continue

            try:
                # payload format: b"<candidate_id>|<token>"
                parts = pt.decode("utf-8").split("|")
                candidate_id = int(parts[0])
            except Exception as e:
                invalid.append((ev.id, f"parse error: {e}"))
                continue

            counts[candidate_id] = counts.get(candidate_id, 0) + 1
            total += 1

        # Build CSV in-memory
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["candidate_id", "count"]) 
        for cid, cnt in sorted(counts.items(), key=lambda x: -x[1]):
            writer.writerow([cid, cnt])

        summary = {
            "election": election.id,
            "total_counted": total,
            "invalid_records": len(invalid),
            "generated_at": timezone.now().isoformat(),
        }

        self.stdout.write(self.style.SUCCESS(f"Tally complete for election {election.id}: {summary}"))

        if options.get("export"):
            # Save CSV to Report model
            filename = f"tally_election_{election.id}_{timezone.now().strftime('%Y%m%d%H%M%S')}.csv"
            # create Report entry and attach file
            rpt = Report.objects.create(name=f"Tally {election.name} - {timezone.now().isoformat()}")
            # save file content
            rpt.file.save(filename, io.BytesIO(output.getvalue().encode("utf-8")))
            rpt.save()
            self.stdout.write(self.style.SUCCESS(f"Exported CSV to Report {rpt.id} (file: {rpt.file.name})"))
