from django.urls import path
from .views import (AccountCreateView, AccountDetailView, AccountListView,
                    CustomerCreateView, CustomerDetailView, CustomerListView,
                    TransactionDetailView, TransactionListView,
                    DepositTransactionCreateView, WithdrawTransactionCreateView)
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', CustomerCreateView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='auth-token'),
    path('logout/', obtain_auth_token, name='logout'),
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name='customer_details'),
    path('customer/', CustomerListView.as_view(), name='customer_list'),
    path('create/', AccountCreateView.as_view(), name='account_create'),
    path('account/<int:pk>/', AccountDetailView.as_view(), name='account_details'),
    path('account/', AccountListView.as_view(), name='account_list'),
    path('transaction/<int:pk>/', TransactionDetailView.as_view(), name='transaction_details'),
    path('transaction/', TransactionListView.as_view(), name='transaction_list'),
    path('deposit/', DepositTransactionCreateView.as_view(), name='deposit'),
    path('withdraw/', WithdrawTransactionCreateView.as_view(), name='withdraw')
]
