from django.urls import path

from . import views

app_name = 'auctions'

urlpatterns = [
    path('', views.AuctionIndexView.as_view(), name='index'),
    path('create/', views.getNewAuction, name='create'),
    path('create/success', views.successfulAuctionPost, name='success'),
]
