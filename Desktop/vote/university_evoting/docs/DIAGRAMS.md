# Diagrams & Architecture Sketches

This file contains textual sketches and pointers for diagrams to be created (draw.io, mermaid, or PlantUML).

## ERD — core entities
- Users (User) —< UserRole >— Roles
- Election -> Positions -> CandidateApplication
- Election -> Ballot -> Position entries
- VoteToken -> User
- VoteSubmission -> EncryptedVote

## Sequence: Vote submission
1. Voter requests token (claim endpoint)
2. Token issued (one-time, recorded)
3. Voter sends vote submission with token and encrypted payload
4. Voting Engine validates token & eligibility and records encrypted vote
5. Voting Engine returns receipt_hash

## Suggested files
- diagrams/erd.drawio (for ERD)
- diagrams/vote_submission_sequence.drawio

*Next: generate minimal OpenAPI snippets for key endpoints.*