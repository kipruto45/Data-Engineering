# Module 6 — Candidate Management Module

## Overview
Handles candidate applications, approvals, manifestos, and campaign compliance.

## Responsibilities
- Candidate registration and profile management
- Manifesto upload and verification
- Approval/rejection workflow with audit trail
- Campaign violation tracking

## Data Model
```python
class CandidateApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.ForeignKey('Position', on_delete=models.CASCADE)
    manifesto = models.FileField(null=True)
    status = models.CharField(choices=[('pending','Pending'),('approved','Approved'),('rejected','Rejected')], default='pending')
```

## REST API surface
- POST /api/elections/{election}/positions/{position}/candidates/ — apply
- GET /api/candidates/{id}/ — details
- PATCH /api/candidates/{id}/status/ — approve/reject

## Acceptance Criteria
- Candidates can apply, and admins can approve/reject with reasons
- Manifesto files stored securely with virus scanning
