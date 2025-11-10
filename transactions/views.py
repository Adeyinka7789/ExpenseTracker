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
    """Returns user balance and transaction analytics with caching."""
    permission_classes = [IsAuthenticated]

    def _get_balance(self, user):
        """
        Calculate user balance from income and expenses.
        """
        cache_key = f"user_balance_{user.id}"
        cached_balance = cache.get(cache_key)

        if cached_balance is not None:
            return Decimal(str(cached_balance))

        transactions = Transaction.objects.filter(user=user)
        income = transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or Decimal('0')
        expenses = transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or Decimal('0')
        balance = income - expenses
        cache.set(cache_key, float(balance), timeout=300)
        return balance

    def get(self, request):
        user = request.user
        balance = self._get_balance(user)

        return Response({
            'balance': balance,
            'transaction_count': Transaction.objects.filter(user=user).count(),
        })