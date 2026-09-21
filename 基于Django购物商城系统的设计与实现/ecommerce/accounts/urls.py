from django.urls import path
from accounts.views import RegisterView, LoginView, UserProfileView, AddressView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('addresses/', AddressView.as_view(), name='addresses'),
]
