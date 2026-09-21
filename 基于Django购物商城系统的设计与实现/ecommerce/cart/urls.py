from django.urls import path
from cart.views import CartView, CartItemAddView, CartItemUpdateView, CartItemDeleteView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('items/add/', CartItemAddView.as_view(), name='cart-item-add'),
    path('items/<int:pk>/update/', CartItemUpdateView.as_view(), name='cart-item-update'),
    path('items/<int:pk>/delete/', CartItemDeleteView.as_view(), name='cart-item-delete'),
]
