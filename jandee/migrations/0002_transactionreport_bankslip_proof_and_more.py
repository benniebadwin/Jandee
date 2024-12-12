# Generated by Django 5.1.4 on 2024-12-11 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jandee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionreport',
            name='bankslip_proof',
            field=models.ImageField(blank=True, null=True, upload_to='bankslip_proofs/'),
        ),
        migrations.AddField(
            model_name='transactionreport',
            name='mpesa_transaction_message',
            field=models.TextField(blank=True, help_text='Paste the Mpesa transaction message here', null=True),
        ),
    ]