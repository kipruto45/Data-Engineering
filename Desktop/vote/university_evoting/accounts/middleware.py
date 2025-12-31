import uuid
from django.http import JsonResponse
from .models import RevokedAccessToken
import logging

logger = logging.getLogger(__name__)

class RevokedAccessTokenMiddleware:
    """Middleware to reject requests with revoked JTI access tokens.

    Expects Authorization header in form: "Bearer <jti>.<random>" where <jti> is the UUID JTI.
    If the JTI exists in RevokedAccessToken and is revoked, respond with 401.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth = request.META.get("HTTP_AUTHORIZATION", "")
        if auth.startswith("Bearer "):
            token = auth.split(" ", 1)[1]
            parts = token.split(".")
            if parts:
                jti_str = parts[0]
                try:
                    jti = uuid.UUID(jti_str)
                    revoked = RevokedAccessToken.objects.filter(jti=jti, revoked=True).exists()
                    if revoked:
                        logger.warning("Request with revoked access token", extra={"jti": str(jti)})
                        return JsonResponse({"detail": "token revoked"}, status=401)
                except Exception:
                    # malformed JTI - ignore here and let auth fail downstream
                    pass
        return self.get_response(request)
