from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import UserRegistrationView, ChatView, TokenBalanceView, TokenTopUpView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('chat/', ChatView.as_view(), name='chat'),
    path('tokens/', TokenBalanceView.as_view(), name='token-balance'),
    path('top-up/', TokenTopUpView.as_view(), name='token-top-up'),
]
