Title: Add MFA support (WebAuthn / TOTP)

Priority: P0

Description:
Add MFA device registration and enforcement for high-privilege roles and risky sessions. Support WebAuthn (passkeys) and TOTP.

Acceptance Criteria:
- Users can register and verify WebAuthn/TOTP devices
- Policy enforcement to require MFA for critical actions
- End-to-end tests for registration, verification and enforcement
- Recovery and backup codes implemented
