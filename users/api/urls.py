from django.urls import path
from .views import UserCreate, LoginView

urlpatterns = [
    path('register',UserCreate.as_view(), name='register-user'),
    path('login-user', LoginView.as_view(), name='login-user')
]
