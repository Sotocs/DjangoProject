from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import LoginView, ProfileUpdateView, register_view

app_name = "users"

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
]
