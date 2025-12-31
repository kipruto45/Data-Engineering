# Module 8 — Voting Engine Module

## Overview
Captures and validates votes securely. Ensures one-person-one-vote and provides confirmation receipts.

## Responsibilities
- Handle vote submission APIs and validation
- Issue and validate one-time voting tokens
- Provide voter confirmation receipts
- Integrate with VOTE ENCRYPTION & ANONYMIZATION and VOTE STORAGE modules

## Data Model (high-level)
```python
class VoteToken(models.Model):
    token = models.CharField(max_length=128, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()

class VoteSubmission(models.Model):
    election = models.ForeignKey('Election', on_delete=models.CASCADE)
    ballot_snapshot = models.JSONField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    receipt_hash = models.CharField(max_length=128)
```

## REST API surface
- POST /api/elections/{election}/vote/ — submit a vote (requires valid token & eligibility)
- POST /api/elections/{election}/tokens/claim/ — claim a one-time token
- GET /api/elections/{election}/receipt/{receipt_hash}/ — verify receipt

## Non-functional requirements
- High availability and stateless API design
- Idempotency and duplication protections

## Acceptance Criteria
- Only eligible and token-holding users can submit one vote per election
- Voter receives a verifiable receipt for their submission
