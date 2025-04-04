# Generated by Django 5.1.7 on 2025-04-05 08:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0005_remove_recipient_account_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='recipient',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='recipient_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recieved_transactions', to='account_app.recipient_account'),
        ),
    ]
