from django.db import models
from django.contrib.auth.models import User
from django.db.models import F


# Create your models here.
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    address = models.TextField(max_length=200)
    phone_number = models.IntegerField()

    def __str__(self):
        return self.user


class Account(models.Model):
    ACCOUNT_TYPES = [
        ('SAVINGS', 'savings'),
        ('CHEKINGS', 'checkings'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer} - {self.account_type}'


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'deposit'),
        ('WITHDRAW', 'withdraw'),
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=100, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.transaction_type} - {self.amount} - {self.time_stamp}'

    def save(self, *args, **kwargs):
        if self.transaction_type == 'DEPOSIT':
            self.account.balance = F('balance') + self.amount
        elif self.transaction_type == 'WITHDRAWAL':
            if self.account.balance < self.amount:
                raise ValueError("Insufficient funds for withdrawal")
            self.account.balance = F('balance') - self.amount
        self.account.save()
        super().save(*args, **kwargs)
