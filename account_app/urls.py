from django.urls import path
from .views import (AccountCreateView, AccountDetailView, AccountListView,
                    CustomerCreateView, CustomerDetailView, CustomerListView,
                    TransactionDetailView, TransactionListView,
                    DepositTransactionCreateView, WithdrawTransactionCreateView)

urlspatterns = [
    path('register/', CustomerCreateView.as_view(), name='register'),
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name='customer_details'),
    path('customer/', CustomerListView.as_view(), name='customer_list'),
    path('account/create/', AccountCreateView.as_view(), name='account_create'),
    path('account/<int:pk>/', AccountDetailView.as_view(), name='account_details'),
    path('account/', AccountListView.as_view(), name='account_list'),
    path('transaction/<int:pk>/', TransactionDetailView.as_view(), name='transaction_details'),
    path('transaction/', TransactionListView.as_view(), name='transaction_list'),
    path('deposit/', DepositTransactionCreateView.as_view(), name='deposit'),
    path('withdraw/', WithdrawTransactionCreateView.as_view(), name='withdraw'),
]
