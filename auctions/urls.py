from django.urls import path

from . import views

app_name = 'auctions'

urlpatterns = [
    path('', views.AuctionIndexView.as_view(), name='index'),
    path('<int:pk>/', views.AuctionDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.edit_auction, name='edit'),
    path('<int:pk>/ban_auction/', views.ban_auction, name='ban_auction'),
    path('create/', views.new_auction, name='create'),
    path('create/confirm', views.ConfirmAuctionView.as_view(), name='confirm'),
    path('create/success', views.successful_auction_post, name='success'),
    path('create/bad_request/', views.bad_request, name='bad_request'),
]
