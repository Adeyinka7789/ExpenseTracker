from django.urls import path
from .views import RegisterView, TransactionListCreateView, AnalyticsView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('transactions/', TransactionListCreateView.as_view(), name='transactions'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
]