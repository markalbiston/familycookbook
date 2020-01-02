from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('loginpage', views.loginpage),
    path('registerpage', views.registerpage),
    path('logout', views.logout),
]