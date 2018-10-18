from django.urls import path

from . import views

app_name = 'auctions'

urlpatterns = [
    path('', views.AuctionIndexView.as_view(), name='index'),
    path('<int:pk>/', views.AuctionDetailView.as_view(), name='detail'),
    path('create/', views.newAuction, name='create'),
    path('create/confirm', views.ConfirmAuctionView.as_view(), name='confirm'),
    path('create/success', views.successfulAuctionPost, name='success'),
    path('create/bad_request/', views.badRequest, name='badRequest'),
]
