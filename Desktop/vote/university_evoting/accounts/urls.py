from django.urls import path
from .views import MeView, MFATOTPRegisterView, MFATOTPVerifyView, MFATOTPListView, MFATOTPDeleteView
from .views import MagicLinkRequestView, MagicLinkVerifyView

urlpatterns = [
    path("me/", MeView.as_view(), name="api-me"),
    # MFA (TOTP)
    path("mfa/totp/register/", MFATOTPRegisterView.as_view(), name="mfa-totp-register"),
    path("mfa/totp/verify/", MFATOTPVerifyView.as_view(), name="mfa-totp-verify"),
    path("mfa/totp/", MFATOTPListView.as_view(), name="mfa-totp-list"),
    path("mfa/totp/<int:pk>/", MFATOTPDeleteView.as_view(), name="mfa-totp-delete"),
    # Magic link (passwordless)
    path("magic/request/", MagicLinkRequestView.as_view(), name="magic-request"),
    path("magic/verify/", MagicLinkVerifyView.as_view(), name="magic-verify"),
]
