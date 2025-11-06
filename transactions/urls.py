# REVIEW: full code review requested

from django.urls import path
from .views import RegisterView, TransactionListCreateView, AnalyticsView
# Note: TokenObtainPairView is only imported if needed elsewhere, 
# but removed from urlpatterns since it's mapped at the project level (/api/token/).

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # REMOVED: path('login/', TokenObtainPairView.as_view(), name='login'), 
    # This path is redundant. JWT login is handled at the project level path('api/token/', ...)
    path('transactions/', TransactionListCreateView.as_view(), name='transactions'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
]