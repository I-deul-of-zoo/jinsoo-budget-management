from django.urls import path
from accounts.views import RegisterView, LoginView

app_name = "accounts"
# base_url: api/auth/

urlpatterns =[
    path("signup/", RegisterView.as_view()),
    path("jwt-login/", LoginView.as_view()),
]
