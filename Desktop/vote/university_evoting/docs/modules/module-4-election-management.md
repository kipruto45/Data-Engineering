# Module 4 — Election Management Module

## Overview
Manages the end-to-end lifecycle of elections: creation, scheduling, state transitions, and archiving.

## Responsibilities
- Create/configure elections and time windows
- State management (draft, scheduled, active, closed, archived)
- Templates and parallel elections
- Emergency pause and auto-archive

## Data Model
```python
class Election(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    state = models.CharField(choices=[('draft','Draft'),('active','Active'),('closed','Closed'),('archived','Archived')])
    start = models.DateTimeField()
    end = models.DateTimeField()
    config = models.JSONField(default=dict)
```

## REST API surface
- POST /api/elections/ — create
- PATCH /api/elections/{id}/state/ — change state
- GET /api/elections/ — list and filter

## Acceptance Criteria
- Can schedule an election and transition state automatically
- Supports emergency pause and resume

---
*Next: Module 5 (Position/Seat Management).*