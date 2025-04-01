from rest_framework import serializers
from .models import Customer, Account, Transaction
from django.contrib.auth.models import User


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'customer', 'account_type', 'balance', 'account_number', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        # Check if the customer already has an account of the same type
        customer = data.get('customer')
        account_type = data.get('account_type')
        if Account.objects.filter(customer=customer, account_type=account_type).exists():
            raise serializers.ValidationError(f"The customer already has a {account_type} account.")
        return data


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'account', 'transaction_type', 'amount', 'time_stamp']
        read_only_fields = ['transaction_type', 'time_stamp']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ['id', 'user', 'email', 'address', 'phone_number']

    def create(self, validated_data):
        # Extract user data
        user_data = validated_data.pop('user')
        # Create the User object
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        # Create the Customer object linked to the User
        customer = Customer.objects.create(user=user, **validated_data)
        return customer
