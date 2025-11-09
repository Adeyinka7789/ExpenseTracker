from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- JWT Authentication Endpoints ---
    # The frontend is hardcoded to use /api/token/ for login (TokenObtainPairView).
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # --- Application Endpoints ---
    # This includes transactions/, analytics/, and importantly, register/
    path('api/', include('transactions.urls')),
]