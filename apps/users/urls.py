from django.urls import path

from apps.users.views import UserLoginView, UserRegisterView, UserLogoutView, UserProfileView

app_name = "users"
urlpatterns = [
    path('login/', UserLoginView.as_view(), name="login-page"),
    path('logout/', UserLogoutView.as_view(), name="logout"),
    path('register/', UserRegisterView.as_view(), name="register-page"),
    path('user-profile/', UserProfileView.as_view(), name="user-profile")
]
