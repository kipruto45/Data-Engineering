import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=64, blank=True, null=True, unique=True)
    ROLE_CHOICES = [
        ("student", "Student"),
        ("staff", "Staff"),
        ("admin", "Admin"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")

    STATUS_ACTIVE = 'active'
    STATUS_SUSPENDED = 'suspended'
    STATUS_ARCHIVED = 'archived'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_SUSPENDED, 'Suspended'),
        (STATUS_ARCHIVED, 'Archived'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)

    campus = models.CharField(max_length=100, blank=True)
    faculty = models.CharField(max_length=100, blank=True)

    # Generic attributes for ABAC and integrations
    attributes = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# Authentication session and refresh token models
class AuthSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    device = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    revoked = models.BooleanField(default=False)

    def __str__(self):
        return f"Session {self.session_id} for {self.user} ({'revoked' if self.revoked else 'active'})"


class RefreshToken(models.Model):
    session = models.ForeignKey(AuthSession, on_delete=models.CASCADE, related_name="refresh_tokens")
    token_id = models.UUIDField(default=uuid.uuid4, editable=False)
    token_hash = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    rotated = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=["token_id"]) ]

    def __str__(self):
        return f"RefreshToken {self.token_id} (rotated={self.rotated})"


class RevokedAccessToken(models.Model):
    """Tracks issued access tokens and their revocation state (simple JTI revocation list).

    This is intentionally simple for the POC: store a UUID JTI, link to an auth session and allow
    marking revoked when refresh-token misuse is detected.
    """
    jti = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    session = models.ForeignKey(AuthSession, on_delete=models.CASCADE, related_name="access_tokens")
    issued_at = models.DateTimeField(auto_now_add=True)
    revoked = models.BooleanField(default=False)
    revoked_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"AccessToken {self.jti} (revoked={self.revoked})"
