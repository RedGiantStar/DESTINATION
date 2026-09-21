from django.urls import path
from orders.views import OrderCreateView, OrderListView, OrderDetailView, OrderCancelView, OrderConfirmView

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('list/', OrderListView.as_view(), name='order-list'),
    path('detail/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('cancel/<int:pk>/', OrderCancelView.as_view(), name='order-cancel'),
    path('confirm/<int:pk>/', OrderConfirmView.as_view(), name='order-confirm'),
]
