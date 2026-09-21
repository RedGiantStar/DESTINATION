from django.urls import path
from payment.views import PaymentCreateView, PaymentCallbackView, PaymentListView

urlpatterns = [
    path('create/', PaymentCreateView.as_view(), name='payment-create'),
    path('callback/', PaymentCallbackView.as_view(), name='payment-callback'),
    path('list/', PaymentListView.as_view(), name='payment-list'),
]
