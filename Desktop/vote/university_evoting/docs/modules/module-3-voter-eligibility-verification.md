# Module 3 — Voter Eligibility & Verification Module

## Overview
Validates that only eligible users can vote and enforces one-person-one-vote rules. Provides eligibility rule management, simulation, and appeal workflows.

## Responsibilities
- Define eligibility rules by faculty, year, program, and campus
- Real-time voter validation prior to vote casting
- Track vote status (not-voted, voted, excluded)
- Appeals and override workflows

## Data Model (Django-style skeleton)
```python
class EligibilityRule(models.Model):
    name = models.CharField(max_length=200)
    conditions = models.JSONField()  # rule expression (ABAC policy)
    active = models.BooleanField(default=True)

class VoterStatus(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    eligible = models.BooleanField(default=False)
    reason = models.TextField(null=True)
    last_checked = models.DateTimeField(null=True)
```

## REST API surface
- GET /api/eligibility/rules/ — list rules
- POST /api/eligibility/evaluate/ — evaluate a user or batch
- POST /api/eligibility/simulate/ — run simulations for hypothetical changes
- POST /api/eligibility/appeal/ — submit appeals for ineligible voters

## Modernisation
- ABAC evaluation engine for complex conditional rules
- Dynamic eligibility config with versioning and rollback

## Acceptance Criteria
- Admins can define rules and simulate eligibility outcomes
- Voter check happens at vote submission and blocks ineligible voters
