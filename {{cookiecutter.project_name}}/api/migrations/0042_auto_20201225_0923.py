# Generated by Django 3.1.2 on 2020-12-25 09:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0041_remove_account_first_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountselectedkpis',
            name='account',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                       related_name='account_selected_kpis', to='api.account'),
        ),
    ]
