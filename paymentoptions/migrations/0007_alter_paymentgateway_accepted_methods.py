# Generated by Django 4.2.6 on 2023-12-28 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paymentoptions', '0006_alter_paymentgateway_accepted_methods'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentgateway',
            name='accepted_methods',
            field=models.TextField(blank=True, default='None', null=True),
        ),
    ]
