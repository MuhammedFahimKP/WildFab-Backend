from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('user/cart-wishlist-count/',consumers.GetCartAndWishlistCountConsumer.as_asgi()),
    path('admin/get-count-dashboard/',consumers.AdminDashBoardCountConsumer.as_asgi()),
]