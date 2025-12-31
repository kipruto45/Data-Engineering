from collections import Counter
from .models import EncryptedVote


def simple_tally(election):
    """Return a dict mapping candidate_id to vote counts for the given election."""
    qs = EncryptedVote.objects.filter(election=election)
    counts = Counter(qs.values_list("candidate_id", flat=True))
    # return as dict of candidate_id: count
    return dict(counts)
