# University E-Voting System — Architecture & Module Map

This document maps the comprehensive module list into a practical implementation plan (Django backend + REST APIs). It also indicates which app(s) will own the responsibility and the immediate next steps.

## A. CORE SYSTEM MODULES (Mandatory)

1. User Management Module — accounts app
   - Models: `Profile` (exists)
   - API: /api/accounts/

2. Authentication & Authorization Module — Django auth + accounts
   - Use Django auth, optional OTP and 2FA in `accounts` or `integrations` (SSO)

3. Voter Eligibility & Verification Module — elections app / voting app
   - Eligibility rules via `Election` and `Position` models

4. Election Management Module — elections app
   - Models: `Election`, `Position`, `Candidate` (exists)

5. Position / Seat Management Module — elections app (exists)

6. Candidate Management Module — elections app (exists)

7. Ballot Management Module — voting app
   - Ballot rendering and locking on publish

8. Voting Engine Module — voting app (exists start)
   - API: /api/voting/issue/, /api/voting/cast/ (scaffolded)

9. Vote Encryption & Anonymization Module — voting app / integrity
   - Use public-key crypto in production; `utils.simple_encrypt_vote` is a demo stub

10. Vote Storage Module — voting app (EncryptedVote + VoteToken exist)

11. Vote Counting & Tally Module — results / reports app

12. Results Management Module — results / reports app

## B. TRANSPARENCY, AUDIT & CONTROL MODULES

13. Audit & Logging Module — audit app (scaffolded)
    - Log user/actions without storing vote content

14. Election Monitoring Module — monitoring app (scaffolded)

15. Dispute & Complaint Management Module — disputes app (scaffolded)

16. Verification & Integrity Module — integrity app (scaffolded)

## C. COMMUNICATION & ENGAGEMENT MODULES

17. Notification Module — notifications app (scaffolded)

18. Announcement & Bulletin Module — notifications / elections

19. Voter Education Module — docs + templates

## D. REPORTING & EXPORT MODULES

20. Reporting & Analytics Module — reports / analytics apps (scaffolded)

21. Data Export Module — reports app

## E. SYSTEM & INFRASTRUCTURE MODULES

22. Role & Permission Management Module — accounts + policy
23. System Configuration Module — settings + admin UI
24. Security & Threat Protection Module — middleware, rate-limiting, WAF
25. Backup & Recovery Module — ops documentation
26. API & Integration Module — integrations app (scaffolded)

## F. ADVANCED / OPTIONAL MODULES

27. Blockchain / Immutable Ledger Module — ledger app (scaffolded)
28. Biometric Verification Module — integrations (external)
29. AI Anomaly Detection Module — analytics app (scaffolded)
30. Offline / Failover Voting Module — offline app (scaffolded)
31. Public Verification Portal — reports + public endpoints

## G. USER INTERFACE MODULES

32. Voter Dashboard — frontend
33. Admin Dashboard — frontend
34. Candidate Dashboard — frontend
35. Auditor Dashboard — frontend

---

## Implementation Priorities
- Phase 1 (MVP): accounts, elections, voting, basic audit, notifications, reports (skeleton)
- Phase 2: vote encryption, integrity verification, monitoring, dispute handling
- Phase 3: scaling, blockchain ledger (optional), offline support, advanced analytics

## Next steps taken by this commit
- Scaffolding for `audit`, `reports`, `integrity`, `ledger`, `monitoring`, `disputes`, `analytics`, `integrations`, `offline` created.
- Basic models and admin registration added for each new app.
- Apps registered in `INSTALLED_APPS`.

---

If you'd like, I can now:
- Flesh out DB schema per module (generate ER diagrams)
- Implement REST APIs & serializers for each module
- Start a React scaffold for front-end dashboards

The detailed module specification is available in `docs/MODULE_SPEC.md` — I can scaffold the top-priority APIs next.

Tell me which of the above to do next or I can continue and implement the APIs automatically.
