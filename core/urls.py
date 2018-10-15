from django.urls import  path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.signup, name='register'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logout, {'next_page': '/'}, name='logout'),
]