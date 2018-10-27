from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('auctions/', views.auctions, name='auctions'),
    path('auctions/<int:pk>/', views.auction_detail, name='detail'),
    path('auctions/<int:pk>/bid/', views.new_bid, name='bid')
]
