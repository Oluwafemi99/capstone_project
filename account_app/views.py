from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import (AccountSerializer, TransactionSerializer,
                          CustomerSerializer)
from .models import Account, Customer, Transaction
from rest_framework.exceptions import ValidationError


# Create your views here.
class ProfileView(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class AccountCreateView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        customer = serializer.validated_data['customer']
        account_type = serializer.validated_data['account_type']

        # Check if the customer already has an account of the same type
        if Account.objects.filter(customer=customer, account_type=account_type).exists():
            raise ValidationError({"detail": f"The customer already has a {account_type} account."})

        serializer.save()


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

        if account.balance < amount:
            raise ValidationError({"detail": "Insufficient balance for withdrawal."})
        account.balance -= amount
        account.save()
        serializer.save(transaction_type='withdraw')


class DepositTransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Custom logic for deposit transaction
        account = serializer.validated_data['account']
        amount = serializer.validated_data['amount']
        customer = Customer.objects.get(user=self.request.user)
        if account.customer != customer:
            raise ValidationError({"detail": "You are not authorized to perform transactions on this account."})
        account.balance += amount
        account.save()
        serializer.save(transaction_type='deposit')


class TransactionDetailView(generics.RetrieveAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the authenticated user's customer object
        customer = Customer.objects.get(user=self.request.user)
        # Restrict the queryset to transactions related to the customer's accounts
        return Transaction.objects.filter(account__customer=customer)
