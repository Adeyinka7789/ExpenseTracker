from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.cache import cache
from .models import Transaction

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializes user data for registration."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class TransactionSerializer(serializers.ModelSerializer):
    """Serializes transaction data and clears related cache on create."""
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'type', 'category', 'description', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
    
        transaction = Transaction.objects.create(**validated_data)
        user = validated_data.get('user')
        if user:
            cache_key = f"user_balance_{user.id}"
            cache.delete(cache_key)
            cache.set(f"update_{user.id}", str(transaction.created_at), timeout=300)

        return transaction