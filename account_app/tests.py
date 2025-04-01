from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Customer, Account, Transaction


class AccountAppTests(TestCase):
    def setUp(self):
        # Set up API client
        self.client = APIClient()

        # Create a user and customer
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
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

        # Authenticate the client
        self.client.force_authenticate(user=self.user)

    def test_create_customer(self):
        # Test creating a customer via API
        payload = {
            "user": {
                "username": "newuser",
                "password": "securepassword",
                "email": "newuser@example.com"
            },
            "email": "customer@example.com",
            "address": "456 New Street",
            "phone_number": 9876543210
        }
        response = self.client.post('/account/register/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Customer.objects.count(), 2)  # One from setUp, one from this test
        self.assertEqual(Customer.objects.last().email, "customer@example.com")

    def test_deposit_transaction(self):
        # Test creating a deposit transaction via API
        payload = {
            "account": self.account.id,
            "amount": 500.00
        }
        response = self.client.post('/account/deposit/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.last().transaction_type, 'DEPOSIT')
        self.assertEqual(Transaction.objects.last().amount, 500.00)

        # Check if the account balance is updated
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 1500.00)

    def test_withdraw_transaction(self):
        # Test creating a withdrawal transaction via API
        payload = {
            "account": self.account.id,
            "amount": 300.00
        }
        response = self.client.post('/account/withdraw/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.last().transaction_type, 'WITHDRAW')
        self.assertEqual(Transaction.objects.last().amount, 300.00)

        # Check if the account balance is updated
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 700.00)

    def test_withdraw_insufficient_balance(self):
        # Test withdrawal with insufficient balance
        payload = {
            "account": self.account.id,
            "amount": 2000.00  # More than the current balance
        }
        response = self.client.post('/account/withdraw/', payload, format='json')
        self.assertEqual(response.status_code, 400)  # Expecting a 400 Bad Request
        self.assertEqual(Transaction.objects.count(), 0)  # No transaction should be created

        # Check that the account balance remains unchanged
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 1000.00)
