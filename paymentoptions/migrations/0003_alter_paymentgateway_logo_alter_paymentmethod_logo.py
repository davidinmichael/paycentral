# Generated by Django 4.2.6 on 2023-11-28 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paymentoptions', '0002_paymentgateway_paymentmethod_userrating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentgateway',
            name='logo',
            field=models.ImageField(default='payment-gateway.png/', upload_to='payment_gateway/'),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='logo',
            field=models.ImageField(default='payment-option.png/', upload_to='payment_option/'),
        ),
    ]
