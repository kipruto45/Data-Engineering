# Follow-up Implementation Issues (stubs)

These are recommended issues to create after merging the module specs.

## Phase 1 (P0)
- Implement refresh-token rotation and reuse detection in Auth module
- Add MFA (WebAuthn/TOTP) enforcement and tests
- Integrate Eligibility checks into vote submission (ABAC-based)
- Implement Role approval workflows and UI endpoints
- Harden token issuance: rate-limits, device tracking, anomaly detection
- Add signed tally pipeline and a reproducible tally CLI with artifact signing

## Phase 2 (P1)
- Implement duplicate detection/merge tool for user import
- Add high-availability architecture docs and autoscaling tests
- Implement append-only EncryptedVote storage (WORM) or ledger-backed storage
- Add long-term cold archive process for votes and results

## Security & Ops
- HSM integration for tally private keys and key rotation runbook
- Add automated dependency & security scanning (Snyk, Dependabot)
- Add production-grade monitoring (Prometheus metrics, Grafana dashboards)

## Testing
- Add integration tests for eligibility and tally (expanded)
- Create load tests for voting engine (e.g., locust scenarios)

---
*I can create GitHub issues from these stubs if you provide a token or push requests to the remote; otherwise these serve as local guidance.*