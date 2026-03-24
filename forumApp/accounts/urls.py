from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import UserRegisterView
from django.contrib.auth.views import LogoutView, LoginView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('my-account/', views.UserUpdateView.as_view(), name='my_account'),
]
