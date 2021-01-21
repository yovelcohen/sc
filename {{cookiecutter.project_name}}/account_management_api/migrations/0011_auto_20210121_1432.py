# Generated by Django 3.1.2 on 2021-01-21 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_management_api', '0010_auto_20201208_0910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usagereports',
            name='file',
        ),
        migrations.RemoveField(
            model_name='usagereports',
            name='year',
        ),
        migrations.AddField(
            model_name='usagereports',
            name='raw_report',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='usagereports',
            name='retry_failed',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='usagereports',
            name='successfully_sent',
            field=models.BooleanField(default=False, help_text="When we send the request, if it wasn't successful, we'll try again day after"),
        ),
        migrations.DeleteModel(
            name='FarmMonthlyUsage',
        ),
    ]
