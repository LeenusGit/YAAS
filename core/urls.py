from django.urls import  path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.signup, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('currency/', views.currency, name='currency'),
    path('emailhistory/', views.emails, name='email'),
]
