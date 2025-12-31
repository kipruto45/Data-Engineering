# Module 11 — Vote Counting & Tally Module

## Overview
Automated and verifiable counting of votes after election closure.

## Responsibilities
- Perform deterministic tallying and validation checks
- Support recounts and multi-stage approvals
- Digitally sign published results using tally key

## Process
1. Close election and seal storage snapshot
2. Validate storage integrity and proof-of-possession
3. Decrypt or aggregate encrypted votes, depending on scheme
4. Produce signed results and publish

## APIs
- POST /api/tally/{election}/run/ — run tally
- GET /api/tally/{election}/results/ — retrieve signed results

## Acceptance Criteria
- Tally process is reproducible and logs integrity metadata
- Results are signed and verifiable
