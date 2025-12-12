"""URL configuration for the auth app."""

from django.urls import path
from rest_framework_simplejwt import views

urlpatterns = [
    path(
        "login",
        views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh",
        views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
