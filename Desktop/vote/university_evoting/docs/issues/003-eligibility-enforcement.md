Title: Integrate eligibility checks into vote submission

Priority: P0

Description:
Ensure that vote submission (and token issuance) consults the Voter Eligibility engine (ABAC) before issuing tokens or accepting cast votes. Implement caching and rules versioning.

Acceptance Criteria:
- Token issuance fails for ineligible users
- Vote submission fails for ineligible or revoked users
- Admins can simulate eligibility changes and run bulk re-evaluation
- Integration tests cover representative scenarios
