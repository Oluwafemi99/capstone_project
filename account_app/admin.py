from django.contrib import admin
from .models import Customer, Account, Transaction


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email', 'phone_number', 'address')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'account_type', 'balance', 'account_number', 'created_at')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'transaction_type', 'amount', 'time_stamp')
