from django.db import models
from django.contrib.auth.models import User
import random


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    address = models.TextField(max_length=200)
    phone_number = models.IntegerField()


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Account(models.Model):
    ACCOUNT_TYPES = [
        ('SAVINGS', 'savings'),
        ('CHEKINGS', 'checkings'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    account_number = models.CharField(max_length=10, unique=True)

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_account_number()
        super().save(*args, **kwargs)

    def generate_account_number(self):
        # Generate a random 10-digit account number
        while True:
            account_number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            if not Account.objects.filter(account_number=account_number).exists():
                return account_number

    def __str__(self):
        return f'{self.customer} - {self.account_type} - {self.account_number}'


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
