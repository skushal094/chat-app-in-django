from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name="chat_auth/login.html", redirect_authenticated_user=True),
         name="login"),
    path('register/', views.SignUpView.as_view(), name="signup"),
    path('logout/', LogoutView.as_view(template_name="chat_auth/logout.html"), name="logout"),
]
