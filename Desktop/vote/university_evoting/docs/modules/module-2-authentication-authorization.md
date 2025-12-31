# Module 2 — Authentication & Authorization Module

## Overview
Handles authentication (login, OTP, password), session and JWT management, and access enforcement across the system. This module integrates with SSO and external identity providers.

## Responsibilities
- Authentication flows (password, OTP, passwordless)
- Session and JWT management and token rotation
- Role-Based Access Control (RBAC) and integration with ABAC
- SSO integrations (SAML, OIDC, Azure AD, LDAP)
- Login history and device trust
- Risk-based authentication (optional)

## Data Model (Django-style skeleton)
```python
class AuthSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    jwt = models.TextField()
    refresh_token_hash = models.CharField(max_length=128)
    device_info = models.JSONField(null=True)
    last_active = models.DateTimeField(auto_now=True)

class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code_hash = models.CharField(max_length=128)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
```

## REST API surface
- POST /api/auth/login/ — supports id/password, OTP token exchange (returns JWT & refresh token)
- POST /api/auth/logout/ — invalidate session / refresh token
- POST /api/auth/refresh/ — rotate refresh token and issue new JWT
- POST /api/auth/passwordless/ — start passwordless login (email/sms link)
- POST /api/auth/sso/callback/ — SSO authentication endpoint
- GET /api/auth/sessions/ — list active sessions (user+admin)

## Security Considerations
- Use strong rotating refresh tokens, store only hashed refresh tokens
- JWT short lifetime (e.g., 15m) with refresh rotation
- Rate limiting and anomaly detection for login endpoints
- Enforce MFA for high-privilege actions

## Modernisation & Integrations
- Support passwordless, passkeys (WebAuthn) and FIDO2
- Pluggable identity providers via OIDC/SAML adaptors
- Centralized identity microservice for enterprise deployments

## Monitoring & Compliance
- Failed login rate, successful/failed MFA events
- Device trust issuance and revocations
- Audit logs for elevated privilege assignments

## Acceptance Criteria
- Users can authenticate via password and SSO
- Refresh token rotation works and invalidated on logout
- Admins can view and revoke user sessions

---
*Next step: draft Modules 3–8 in the next batch.*