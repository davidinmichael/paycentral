# Generated by Django 4.2.5 on 2023-11-13 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_appuser_token_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='password',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
