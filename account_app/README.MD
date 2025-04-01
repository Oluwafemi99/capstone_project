MODELS for Account application has been done and it consist of
Customer model
Account model
Transaction model 

testing API
* register
post
http://127.0.0.1:8000/account/register/

body
{
    "user": {
        "username": "newuser",
        "password": "1234",
        "email": "",
        "first_name": "den",
        "last_name": "kit"
    },
    "email": "custxample.com",
    "address": "103 lain Street",
    "phone_number": 1239967887,
}

*create account
Post
http://127.0.0.1:8000/account/create/
{
    "customer": 
    "account_type": "SAVINGS",
    "balance": 1000.00,
    "account_number": "1234567844"
}

*login
post
http://127.0.0.1:8000/account/login/

{
    "username": "newuser"
    "password": "1234"
}

*withdraw
post
http://127.0.0.1:8000/account/withdraw/

{
    "account": 
    "amount": 
}


*deposit
post
http://127.0.0.1:8000/account/deposit/
{
    "account": 
    "amount": 
}

*account details
Get
http://127.0.0.1:8000/account/account/pk/

*customer details
Get
http://127.0.0.1:8000/account/customer/pk/

*transaction details
Get
http://127.0.0.1:8000/account/account/pk/


* account list
Get
http://127.0.0.1:8000/account/account/

* customer list
Get
http://127.0.0.1:8000/account/customer/

* transaction list
Get
http://127.0.0.1:8000/account/transaction/
