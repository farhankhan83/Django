from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='Home'),
    path('about/', views.aboutUs, name='About'),
    path('contact/', views.contact, name='Contact'),
    path('login', views.login, name='Login'),
    path('logout/', views.logoutUser, name='Logout'),
]