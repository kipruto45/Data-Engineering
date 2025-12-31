# Module 2 — Authentication & Authorization (Detailed)

## 1. Purpose & Scope
The Authentication & Authorization Module (Auth) controls how users prove identity and how the system enforces access. It is separate from User Management (which owns canonical user attributes), and from the Voting Engine (which enforces election-specific rules). Auth provides secure, auditable, and extensible authentication mechanisms and centralized access enforcement (RBAC + ABAC).

> **Important design rule:** This module stores no passwords in plaintext; it never stores voter choice or links votes to identities.

## 2. Actors
- End users (students, staff)
- Admins / election operators
- Third-party IdPs (SSO providers, Azure AD, LDAP)
- Auditor / Security team
- Token service (internal)

## 3. Use Cases & Flows
### 3.1 Primary flows
- Username/password login → issue JWT + refresh token
- SSO (OIDC/SAML) login → map external identity to internal user → issue tokens
- Passwordless / OTP flow → send OTP or magic link → short-lived login
- Refresh token rotation → exchange refresh token for new access token and rotated refresh token
- Logout / revoke → invalidate refresh token(s)/sessions
- MFA enrolment / verification (optional) → TOTP / WebAuthn

### 3.2 Exceptional flows
- Suspended user tries to login → deny and audit
- Compromised refresh token presented → revoke all sessions for user
- Admin forced logout (device/session revoke) → immediate token invalidation

## 4. Data Model (Django-style skeleton)
```python
class AuthSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    device = models.JSONField(null=True)  # user-agent, ip (hashed), client_id
    access_token_jti = models.UUIDField(null=True)
    refresh_token_hash = models.CharField(max_length=128)
    issued_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    revoked = models.BooleanField(default=False)

class RefreshToken(models.Model):
    session = models.ForeignKey(AuthSession, on_delete=models.CASCADE)
    token_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    rotated = models.BooleanField(default=False)

class MFADevice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=32)  # TOTP/WebAuthn/SMS
    details = models.JSONField()
    verified = models.BooleanField(default=False)
```

Notes:
- Only hashes of refresh tokens are stored (bcrypt/argon2).
- `access_token_jti` allows short-lived JWT revocation checks if needed.

## 5. API Surface (examples)
### Login / Token
- POST /api/auth/login/ — credentials / idp token → returns { access_token, access_expires, refresh_token }
- POST /api/auth/refresh/ — { refresh_token } → returns rotated refresh + new access token
- POST /api/auth/logout/ — invalidate session / refresh token

### SSO
- GET /api/auth/sso/:provider/redirect/ — redirect URL to IdP
- GET /api/auth/sso/:provider/callback/ — IdP callback → map to user, create session

### MFA
- POST /api/auth/mfa/enable/ — register device (WebAuthn/TOTP)
- POST /api/auth/mfa/verify/ — verify OTP

### Sessions
- GET /api/auth/sessions/ — list user sessions
- POST /api/auth/sessions/{id}/revoke/ — revoke session

### Admin endpoints (RBAC protected)
- GET /api/admin/auth/logins/ — login history and anomalies
- POST /api/admin/auth/impersonate/ — start admin impersonation (audited + limited)

## 6. Security Considerations (Critical)
- Access JWTs: **short-lived** (e.g., 10–15 min). Use RS256 or ES256 signing and include jti, exp, iss, aud.
- Refresh tokens: long-lived but stored only as hashes; rotate on use and detect reuse (token replay detection) to invalidate all session tokens.
- Store device fingerprint & IP (hashed) for anomaly detection (do not store raw IPs unless required by law).
- Enforce MFA for privileged roles & risky sessions (policy driven via ABAC engine).
- Rate-limit / throttle login endpoints and use progressive delays.
- Protect callback endpoints (SSO) against replay and CSRF.
- Keep cryptographic keys in HSM or a secrets manager; rotate keys and publish key IDs (kid) in JWK endpoint.
- Log authentication events in Audit module (avoid putting secrets in logs).

## 7. Authorization model
- RBAC (roles): coarse-grained (voter, election-admin, auditor, super-admin)
- ABAC (attributes): use attribute policies for fine-grained decisions, e.g., ``allow if user.faculty == election.faculty AND user.year >= 2``
- Policy evaluation endpoint: POST /api/authorization/evaluate/ — returns allow/deny & reason
- Decision caching: TTL-based caching of policy decisions for performance while ensuring immediate revocation for security-sensitive actions.

## 8. Integrations
- SSO providers (OIDC, SAML) with configurable connectors
- LDAP sync for user metadata (only read attributes — do not write)
- Device reputation & risk services (optional)
- Centralized secrets store and HSM for key operations
- Audit & SIEM integration for authentication events

## 9. High-level Sequence: Login + Refresh
1. User POST /api/auth/login/ with credentials or SSO token
2. Server verifies and verifies user.status via User Management (e.g., not suspended)
3. Create AuthSession, issue JWT (short-lived) and refresh token (rotated)
4. On /api/auth/refresh/, verify refresh token hash, rotate token, mark previous as rotated; on token reuse detection, revoke all sessions

## 10. Non-Functional Requirements (NFRs)
- Availability: 99.95% SLA for authentication endpoints during election windows
- Latency: 95th percentile login latency < 250ms (auth cache + idp fast paths)
- Throughput: scale to handle login bursts (e.g., start-of-election, 100k concurrent logins across campuses) using autoscaling and SSO provider capacity planning
- Durability: store session metadata replicated across data stores
- Auditability: all admin actions and security events preserved immutably

## 11. Monitoring & Alerting
- Failed login rate spike alert (> X failed attempts/min)
- Token reuse / replay alerts
- High refresh token usage patterns (possible credential stuffing)
- SSO provider failures or latency spikes

## 12. Acceptance Criteria
- Users can authenticate via password and SSO; sessions visible in UI
- Refresh token rotation functions, and reuse detection revokes sessions
- Admins can list and revoke sessions and view login history
- MFA is enforceable by policy and works end-to-end

## 13. Migration & Backward Compatibility
- Introduce new auth tables with migrations and data backfill for sessions when enabling features (MFA, device tracking)
- Provide graceful fallback to existing session behavior and clear migration runbooks

## 14. Security Review Checklist (for reviewers)
- ✔️ No plaintext passwords stored
- ✔️ Refresh tokens hashed, rotated, reuse detection implemented
- ✔️ JWTs short-lived and signed using rotating keys
- ✔️ SSO callback and assertion flows validated against replay and CSRF
- ✔️ MFA implementation vetted (WebAuthn for high assurance)

## 15. Example OpenAPI Snippet (login)
```yaml
paths:
  /api/auth/login/:
    post:
      summary: Login and return tokens
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                identifier: { type: string }
                password: { type: string }
      responses:
        '200':
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token: { type: string }
                  access_expires_in: { type: integer }
                  refresh_token: { type: string }
```

---
**Next step:** I'll add diagram placeholders for login/refresh flows and expand OpenAPI snippets, then hand this for your review. If this looks good, I will proceed to write test cases and example implementation notes (Django models + DRF serializers) for Module 2.
