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

    permission_classes = [IsAuthenticated]

    def _get_balance_and_count(self, user):

        cache_key = f"user_analytics_{user.id}"
        cached = cache.get(cache_key)

        if cached:
            return cached['balance'], cached['count']

        agg = Transaction.objects.filter(user=user).aggregate(
            income=Sum('amount', filter=Q(type='income')),
            expenses=Sum('amount', filter=Q(type='expense')),
            count=Count('id')
        )

        income = agg['income'] or Decimal('0')
        expenses = agg['expenses'] or Decimal('0')
        balance = income - expenses
        count = agg['count'] or 0

        cache.set(cache_key, {
            'balance': float(balance),
            'count': count
        }, timeout=300)

        return balance, count

    def get(self, request):
        user = request.user
        balance, count = self._get_balance_and_count(user)

        return Response({
            'balance': balance,
            'transaction_count': count,
        })