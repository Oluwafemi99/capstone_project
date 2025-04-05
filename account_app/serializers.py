from rest_framework import serializers
from .models import Customer, Account, Transaction, Recipient_Account
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


class TransferTransactionSerializer(serializers.ModelSerializer):
    recipient_account = serializers.CharField(write_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'account', 'transaction_type', 'amount', 'recipient', 'recipient_account', 'time_stamp']
        read_only_fields = ['transaction_type', 'time_stamp']

    def validate(self, data):
        account = data.get('account')
        recipient_account = data.get('recipient_account')
        amount = data.get('amount')
        # Ensure that sender account has suficient balance
        if account.balance < amount:
            raise serializers.ValidationError({'Insufficient balance for the transfer.'})
        # Ensure the recipient account is valid and not the same as the sender's account
        if recipient_account == account:
            raise serializers.ValidationError({'sender and recipient account can not be the same'})
        return data

    def create(self, validated_data):
        # Extract recipient account number
        recipient_account_number = validated_data.pop('recipient_account')

        # Check if the recipient account already exists, otherwise create it
        recipient_account, created = Recipient_Account.objects.get_or_create(account_number=recipient_account_number)

        # Add the recipient_account object to the validated data
        validated_data['recipient_account'] = recipient_account

        # Create the transaction object
        transaction = Transaction.objects.create(**validated_data)
        return transaction


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
