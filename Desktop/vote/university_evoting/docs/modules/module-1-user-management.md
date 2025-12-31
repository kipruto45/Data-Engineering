# Module 1 — User Management Module

## Overview
Manages system users (students, staff, admins, candidates, auditors). Responsible for canonical identity records, role mappings, user lifecycle, and bulk imports; it does not handle authentication or votes.

## Responsibilities
- Maintain user profile records and attributes (name, id, email, campus, faculty, year, program, enrolment status)
- Role assignment and mapping (student, staff, admin, candidate, auditor, observer)
- Bulk import and reconciliation from Student Information Systems (SIS)
- Account lifecycle management (active, suspended, archived)
- Duplicate detection and merge workflows
- Multi-campus & multi-faculty support
- Role approval workflow with audit trail

## Data Model (Django-style skeleton)
```python
class User(models.Model):
    uid = models.CharField(max_length=64, unique=True)  # SIS ID
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    campus = models.ForeignKey('Campus', on_delete=models.PROTECT)
    faculty = models.ForeignKey('Faculty', on_delete=models.PROTECT, null=True)
    year = models.IntegerField(null=True)
    status = models.CharField(choices=[('active','Active'),('suspended','Suspended'),('archived','Archived')], default='active')
    metadata = models.JSONField(default=dict)

class Role(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True)
```

## REST API surface (examples)
- GET /api/users/ — list users (filter: campus, faculty, role, status)
- POST /api/users/import/ — start bulk import (payload: CSV/connector config)
- GET /api/users/{id}/ — user details
- POST /api/users/{id}/roles/ — assign role (requires approval workflow)
- POST /api/users/{id}/merge/ — merge duplicate accounts (admin-only)
- GET /api/users/duplicates/ — list potential duplicates

## Events & Integrations
- Emits events: user.created, user.updated, user.merged, user.role.assigned, user.role.approved
- Supports webhooks and message bus (Kafka/RabbitMQ) for downstream consumers (eligibility, audit)
- SIS connectors (cron or webhook-based) — incremental syncs and full imports

## Permissions
- Role-based and attribute-based checks (ABAC) — e.g., only campus admins can approve campus roles
- Audit trail for all admin actions

## Workflows
- Bulk import flow: validate -> dry-run report -> import -> reconcile errors
- Role assignment: request -> approver review -> approve/reject -> event emitted
- Duplicate detection: run fuzzy-match -> present candidates -> operator merges

## Non-functional requirements (NFRs)
- Import throughput: support 100k users per hour (batch mode)
- Latency: API list endpoints <200ms P95
- High availability and read-replicas for heavy reads
- Data retention & GDPR compliance

## Monitoring & Alerts
- Import job success/failure metrics
- Rate of role assignment approvals/rejections
- Number of duplicates detected per import

## Acceptance Criteria
- Admin can import a SIS CSV and see reconciliation report
- Role approval workflow requires explicit approval by authorized user
- Duplicate detection flags obvious duplicates and allows manual merge

## UX Notes
- Admin UI: bulk-import wizard with step-by-step validation
- User profile page editable with audit history

---
*Next step: draft Module 2 (Authentication & Authorization).*