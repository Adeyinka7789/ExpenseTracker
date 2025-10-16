from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.cache import cache
from decimal import Decimal
from django.db.models import Sum
from .models import Transaction, User
from .serializers import UserSerializer, TransactionSerializer


class RegisterView(generics.CreateAPIView):
    """Handles user registration."""
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class TransactionListCreateView(generics.ListCreateAPIView):
    """Lists and creates transactions for authenticated users."""
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AnalyticsView(generics.RetrieveAPIView):
    """Returns analytics such as balance and transaction count."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cache_key = f"user_balance_{user.id}"

        # Try fetching from cache first
        balance = cache.get(cache_key)
        if balance is None:
            transactions = Transaction.objects.filter(user=user)

            income = transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or Decimal(0)
            expenses = transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or Decimal(0)

            balance = income - expenses

            # Cache result for 5 minutes (300 seconds)
            cache.set(cache_key, float(balance), timeout=300)

        return Response({
            'balance': balance,
            'transaction_count': Transaction.objects.filter(user=user).count(),
            'last_updated': cache.get(f"update_{user.id}")  # Optional timestamp
        })