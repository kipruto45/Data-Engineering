Title: HSM / Key management integration for tally keys

Priority: P0

Description:
Integrate HSM or cloud KMS (AWS KMS/Google Cloud KMS/Azure Key Vault) for secure storage and signing of tally private keys. Provide key rotation/revocation procedures and test harness for signing/verification.

Acceptance Criteria:
- Tally signing keys can be configured to use HSM/KMS
- Signing operations use secure signing endpoints or libraries
- Key rotation procedure documented and tested
