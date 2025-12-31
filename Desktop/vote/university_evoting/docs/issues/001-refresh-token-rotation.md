Title: Implement refresh-token rotation with reuse detection

Priority: P0

Description:
Implement secure refresh-token lifecycle with hashed storage, rotation on refresh, and reuse detection that revokes all sessions for the user when detected.

Acceptance Criteria:
- Refresh tokens stored as secure hashes only
- Rotated on use and previous token recorded as rotated
- Reuse detection triggers session invalidation and admin alert
- Unit and integration tests cover rotation and reuse scenarios

Notes:
- Consider using sliding-window JWT expiration and token revocation lists
- Add monitoring for token reuse spikes
