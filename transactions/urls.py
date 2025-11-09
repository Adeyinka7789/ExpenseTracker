from django.urls import path
from .views import RegisterView, TransactionListCreateView, AnalyticsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('transactions/', TransactionListCreateView.as_view(), name='transactions'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
]