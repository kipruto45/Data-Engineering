# Module 12 — Results Management Module

## Overview
Controls result publication, access, and locking of finalized results.

## Responsibilities
- Declare winners and publish statistics
- Lock and sign published results
- Support live dashboards and historical comparisons

## APIs
- POST /api/results/{election}/publish/ — publish signed results
- GET /api/results/{election}/ — retrieve published results and metadata

## Acceptance Criteria
- Results are signed and immutable after publication
- Role-based access for drafts and publishing
