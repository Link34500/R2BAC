from django.urls import path
from .views import *

app_name = "accounts"

urlpatterns = [
    path("register/",RegisterView.as_view(),name="register"),
    path("verify/",VerifyView.as_view(),name="verify"),
    path("login/",LoginView.as_view(),name="login"),
    path("logout/",LogoutView.as_view(),name="logout"),
    path("profil/",ProfileView.as_view(),name="profile"),
    path("reset-password/",SendResetPasswordView.as_view(),name="reset_password"),
    path("reset-password/<str:token_id>/",PasswordResetView.as_view(),name="password_reset"),
    path("settings/",SettingsView.as_view(),name="settings")
]