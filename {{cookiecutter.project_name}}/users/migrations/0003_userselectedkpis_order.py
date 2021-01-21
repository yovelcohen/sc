# Generated by Django 3.1.2 on 2021-01-17 15:53

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210105_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='userselectedkpis',
            name='order',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, help_text='order of the selected kpis', max_length=4, null=True, size=None),
        ),
    ]
