from django.urls import path

from . import views

app_name = 'bids'

urlpatterns = [
    path('', views.BidView.as_view(), name='bid'),
]
