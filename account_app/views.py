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
    permission_classes = [permissions.IsAuthenticated]


class AccountCreateView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save()


class AccountDetailView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerCreateView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.AllowAny]


class CustomerDetailView(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]


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
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
