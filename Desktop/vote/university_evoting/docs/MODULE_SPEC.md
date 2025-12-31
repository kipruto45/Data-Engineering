# Module Specification — University E-Voting System

This document consolidates the detailed module specifications and maps each to the current codebase (apps) and prioritized implementation tasks.

## Overview & Purpose
Each module below describes: a short description, core features, modernisation priorities, additional features, current mapping to the repo, and recommended next steps and acceptance criteria.

---

## Module 1 — User Management Module
Description: Manages system users (students, staff, admins, candidates, auditors) and roles.
Core Features:
- Bulk import (SIS), profile management, role assignment, lifecycle states (active/suspended/archived)
Modernisation:
- University SSO sync, ABAC, microservice-ready architecture
Additional:
- Duplicate detection, role-approval workflows, multi-campus/faculty support
Repo mapping: `accounts` app (models.Profile exists)
Next steps: implement bulk import CLI, SSO sync adapter, ABAC policy skeleton, duplicate detection job
Acceptance criteria: import CLI handles CSV/JSON/SIS, SSO sync tests, ABAC eval unit tests

---

## Module 2 — Authentication & Authorization Module
Description: Login, identity verification, access enforcement.
Core: login via student/staff ID, password & OTP, JWT/session handling, RBAC
Modernisation: passwordless, SSO (AzureAD/LDAP), refresh token rotation
Repo mapping: `accounts`, Django auth (integration points for OTP/SSO in `integrations`)
Next steps: add OTP endpoints, SSO adapter, refresh-token mechanism
Acceptance criteria: OTP login flow tests, SSO integration smoke test

---

## Module 3 — Voter Eligibility & Verification Module
Description: Ensure only eligible users can vote.
Core: eligibility rules (faculty/year/campus), voter validation, vote status tracking
Modernisation: ABAC-based dynamic rules
Repo mapping: `elections` (Election, Position), `voting`
Next steps: add a rules engine where eligibility can be configured and evaluated
Acceptance criteria: eligibility rules unit tests and endpoint to simulate eligibility

---

## Module 4 — Election Management Module
Description: Full election lifecycle.
Core: create/configure elections, scheduling, election states (draft/active/closed)
Modernisation: templates, parallel elections
Repo mapping: `elections` app
Next steps: implement election templates and admin actions for pause/archival
Acceptance criteria: admin flows and state transition tests

---

## Module 5 — Position / Seat Management Module
Description: Define positions contested in elections.
Core: positions, seat limits, position-level rules
Repo mapping: `elections` app
Next steps: add seat limits validation and tests

---

## Module 6 — Candidate Management Module
Description: Candidate registration and approval flows.
Repo mapping: `elections` app
Next steps: add candidate registration APIs and approval workflow + tests

---

## Module 7 — Ballot Management Module
Description: Create and lock digital ballots.
Core: candidate listing per position, ballot preview, ballot locking
Modernisation: dynamic ballots, accessibility
Repo mapping: `voting` app
Next steps: implement ballot rendering, locking on publication, accessibility tests

---

## Module 8 — Voting Engine Module
Description: Secure vote capture.
Core: vote submission, one-time tokens, confirmation receipts
Modernisation: stateless APIs, HA design
Repo mapping: `voting` app
Next steps: scale/harden voting APIs and test for idempotency and token enforcement

---

## Module 9 — Vote Encryption & Anonymization Module
Description: Prevent traceability of votes to voters.
Core: asymmetric encryption, hashing, identity separation
Modernisation: E2E encryption, ZK proofs
Repo mapping: `voting.crypto`, `integrity`
Next steps: research ZKP libraries, define E2E flows, KMS/HSM integration
Acceptance criteria: test vectors for encryption/decryption, signed and verifiable results

---

## Module 10 — Vote Storage Module
Description: Secure storage of encrypted votes.
Core: encrypted storage, timestamping, token tracking
Modernisation: append-only DB, distributed storage
Repo mapping: `voting` (EncryptedVote)
Next steps: add append-only behavior, immutability checks, archiving job

---

## Module 11 — Vote Counting & Tally Module
Description: Counting votes after closure.
Core: automated tallying, validation, recount support
Modernisation: parallel counting, deterministic verification
Repo mapping: `reports`, `voting` management commands
Next steps: multi-stage approval for published tallies, reproducible tally pipelines

---

## Module 12 — Results Management Module
Description: Controls result publication and access.
Core: winner declaration, statistics, result locking
Modernisation: live dashboards, digitally signed results
Repo mapping: `reports` (ResultPublication implemented)
Next steps: UI endpoints for published results, signed result export

---

## Module 13 — Audit & Logging Module
Description: Accountability without vote content leakage.
Core: user activity, admin action logs, error logs
Modernisation: immutable logs, SIEM integration
Repo mapping: `audit` app
Next steps: append-only audit logs, SIEM forwarder

---

## Module 14 — Reporting & Analytics Module
Repo mapping: `reports`, `analytics`
Next steps: BI dashboard scaffolding and export APIs

---

## Module 15 — Security, Backup & Integration Module
Repo mapping: `integrations`, ops docs
Next steps: document backup strategy, add integration adapters for SIS/SSO/KMS

---

## Implementation prioritisation (suggested)
- Phase 1 (MVP): Core user management, authentication, election orchestration, voting engine, basic audit and reporting
- Phase 2: Vote encryption hardening, KMS/HSM, results publication workflow, monitoring and disputes
- Phase 3: MPC/threshold decryption, ZKP-based verifiability, advanced analytics

---

## Acceptance & QA
For each module we will add unit tests, integration tests and end-to-end scenarios. Each major feature must include:
- API and behavior tests
- Admin permission tests
- Integration/adapter smoke tests (SSO, SIS, KMS)

---

## Next steps (I will perform):
1. Finish writing this spec (this file) — in progress ✅
2. Identify gaps per module and create per-module implementation tasks (todo list created) ✅
3. Start with high-priority tasks (User Management SSO sync / ABAC skeleton and Auth OTP/JWT work)

---

If you want, I can now: scaffold missing APIs for the top 3 priority tasks, or create a ticket/issue list for your review.
