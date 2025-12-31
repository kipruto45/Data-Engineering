# Module 5 — Position / Seat Management Module

## Overview
Defines positions contested in elections, seat limits, and position-specific rules.

## Responsibilities
- Create positions and assign to elections
- Seat limits and position constraints
- Hierarchical positions and conditional eligibility

## Data Model
```python
class Position(models.Model):
    election = models.ForeignKey('Election', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    seats = models.IntegerField(default=1)
    constraints = models.JSONField(default=dict)  # e.g., reserved seats
```

## REST API surface
- POST /api/elections/{election}/positions/ — create position
- GET /api/elections/{election}/positions/ — list

## Acceptance Criteria
- Support reserved seats and conditional eligibility per position
