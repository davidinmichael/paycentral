# Generated by Django 4.2.5 on 2023-11-13 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_appuser_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]