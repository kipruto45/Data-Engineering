# Consolidated Data Models — Overview

This document provides a high-level consolidation of key models used across modules and recommended extensions for implementation.

## Core entities
- User, Role, UserRole
- Election, Position, CandidateApplication, Ballot
- VoteToken, VoteSubmission, EncryptedVote
- EligibilityRule, VoterStatus
- AuthSession, OTP
- AuditEntry, LogEntry

## Relationships (summary)
- User -> UserRole (1:N)
- Election -> Position (1:N)
- Position -> CandidateApplication (1:N)
- Election -> Ballot (1:N)
- VoteToken -> User (N:1), VoteSubmission -> Election (N:1)

## Suggested indexes and constraints
- Unique constraints on (Election.slug), (User.uid)
- Index on VoteSubmission(receipt_hash) for fast lookup

## Open points
- Design for append-only EncryptedVote storage
- Key management integration (HSM) interfaces

---
*Next: generate diagrams and API contract snippets.*