# Generated by Django 3.1.2 on 2020-12-02 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account_management_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usagereports',
            options={'verbose_name': 'Monthly Usage Report', 'verbose_name_plural': 'Monthly Usage Reports'},
        ),
    ]
