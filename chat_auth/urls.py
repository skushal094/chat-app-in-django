from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name="chat_auth/login.html", redirect_authenticated_user=True),
         name="login"),
]
