from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import (AccountSerializer, TransactionSerializer,
                          CustomerSerializer, TransferTransactionSerializer)
from .models import Account, Customer, Transaction
from rest_framework.exceptions import ValidationError


# Create your views here.
class ProfileView(generics.RetrieveAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        return customer


class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class AccountCreateView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]


class AccountDetailView(generics.RetrieveAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the authenticated user's customer object
        customer = Customer.objects.get(user=self.request.user)
        # Restrict the queryset to accounts belonging to the customer
        return Account.objects.filter(customer=customer)


class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class CustomerCreateView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.AllowAny]


class CustomerDetailView(generics.RetrieveAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Restrict the queryset to the authenticated user's customer object
        return Customer.objects.filter(user=self.request.user)


class TransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class WithdrawTransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Custom logic for withdraw transaction
        account = serializer.validated_data['account']
        amount = serializer.validated_data['amount']

        # Ensure the account belongs to the authenticated customer
        customer = Customer.objects.get(user=self.request.user)
        if account.customer != customer:
            raise ValidationError({"detail": "You are not authorized to perform transactions on this account."})

        # Ensure the account balance is not less than the amount
        if account.balance < amount:
            raise ValidationError({"detail": "Insufficient balance."})

        # Deduct amount from account balance
        account.balance -= amount
        account.save()
        serializer.save(transaction_type='WITHDRAW')


class TransferTransactionCreateview(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransferTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        amount = serializer.validated_data['amount']
        account = serializer.validated_data['account']
        # Ensure the account belongs to the authenticated customer
        customer = Customer.objects.get(user=self.request.user)
        if account.customer != customer:
            raise ValidationError({'detail': 'You are not authorized to perform transactions on this account.'})

        # Deduct the amount from the sender's account
        account.balance -= amount
        account.save()
        serializer.save(transaction_type='TRANSFER')


class DepositTransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        # Custom logic for deposit transaction
        account = serializer.validated_data['account']
        amount = serializer.validated_data['amount']

        # Add amount to the account balance
        account.balance += amount
        account.save()
        serializer.save(transaction_type='DEPOSIT')


class TransactionDetailView(generics.RetrieveAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the authenticated user's customer object
        customer = Customer.objects.get(user=self.request.user)
        # Restrict the queryset to transactions related to the customer's accounts
        return Transaction.objects.filter(account__customer=customer)


class CustomerTransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the authenticated user's customer object
        customer = Customer.objects.get(user=self.request.user)

        # Get the transactions related to the customer's accounts
        transaction = Transaction.objects.filter(account__customer=customer)
        return transaction
