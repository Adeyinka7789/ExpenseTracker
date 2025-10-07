from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.cache import cache
from decimal import Decimal
from django.db.models import Sum # We need Sum for AnalyticsView
from .models import Transaction, User
from .serializers import UserSerializer, TransactionSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AnalyticsView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        cache_key = f'balance_{user_id}'

        # Check cache first
        balance = cache.get(cache_key)
        if balance is None:
            # Compute from DB (simulate high-volume query)
            transactions = Transaction.objects.filter(user=request.user)
            
            # Use Sum imported above
            income = transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or Decimal(0)
            expenses = transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or Decimal(0)
            
            balance = income - expenses
            
            # Cache for 5 mins
            cache.set(cache_key, float(balance), 300) # Redis stores as float for simplicity

        return Response({
            'balance': balance,
            'transaction_count': Transaction.objects.filter(user=request.user).count(),
            # Note: The original PDF logic for 'last_updated' requires setting a timestamp somewhere.
            # Assuming update_{user_id} is set elsewhere, we leave this as is:
            'last_updated': cache.get(f'update_{user_id}'), # Optional: timestamp
        })
