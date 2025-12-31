# Module 7 — Ballot Management Module

## Overview
Creates and locks digital ballots for voting.

## Responsibilities
- Create ballots per position/election
- Ballot preview and validation
- Ballot locking prior to election start
- Randomized candidate ordering and accessibility compliance

## Data Model
```python
class Ballot(models.Model):
    election = models.ForeignKey('Election', on_delete=models.CASCADE)
    positions = models.JSONField()  # positions and candidate ordering
    locked = models.BooleanField(default=False)
```

## REST API surface
- POST /api/elections/{election}/ballots/ — create
- POST /api/elections/{election}/ballots/{id}/lock/ — lock ballot

## Acceptance Criteria
- Ballot can be previewed and locked before voting
- Randomization and accessible views available
