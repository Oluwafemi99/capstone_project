from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Customer, Account, Transaction


class AccountAppTests(TestCase):
    def setUp(self):
        # Set up API client
        self.client = APIClient()

        # Create a user and customer
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')

        self.user.is_staff = True  # Make the user a staff user
        self.user.save()
        self.client.force_authenticate(user=self.user)  # Authenticate the user

        self.customer = Customer.objects.create(
            user=self.user,
            email='testuser@example.com',
            address='123 Test Street',
            phone_number=1234567890
        )

        # Create an account for the customer
        self.account = Account.objects.create(
            customer=self.customer,
            account_type='SAVINGS',
            balance=1000.00,
            account_number='1234567890'
        )

    def test_create_customer(self):
        # Test registering a new customer
        payload = {
            "user": {
                "username": "newuser",
                "password": "1234",
                "email": "newuser@example.com",
                "first_name": "Ola",
                "last_name": "Dada"
            },
            "email": "customer@example.com",
            "address": "103 Main Street",
            "phone_number": 9876543210
        }
        response = self.client.post('/account/register/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)  # One from setUp, one from this test
        self.assertEqual(Customer.objects.last().email, "customer@example.com")

    def test_create_account(self):
        # Test creating a new account
        payload = {
            "customer": self.customer.id,
            "account_type": "CHECKINGS",
            "balance": 500.00,
            "account_number": "9876543210"
        }
        response = self.client.post('/account/create/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 2)  # One from setUp, one from this test
        self.assertEqual(Account.objects.last().account_type, "CHECKINGS")

    def test_transaction(self):
        # Test creating a transaction
        payload = {
            "account": self.account.id,
            "transaction_type": "DEPOSIT",
            "amount": 200.00
        }
        response = self.client.post('/account/deposit/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 1200.00)  # Initial balance + deposit amount
