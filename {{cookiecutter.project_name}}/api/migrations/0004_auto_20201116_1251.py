# Generated by Django 3.1.2 on 2020-11-16 12:51

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20201116_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branch',
            name='farm_size',
        ),
        migrations.RemoveField(
            model_name='group',
            name='farm_size',
        ),
        migrations.AlterField(
            model_name='branch',
            name='daily_rumination_ranges',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), default=[10, 20, 30], size=3),
        ),
        migrations.AlterField(
            model_name='branch',
            name='health_rate_ranges',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), default=[10, 20, 30], size=3),
        ),
        migrations.AlterField(
            model_name='branch',
            name='ten_days_avg_rumination_ranges',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), default=[10, 20, 30], size=3),
        ),
        migrations.AlterField(
            model_name='branch',
            name='ten_days_rumination_ranges',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), default=[10, 20, 30], size=3),
        ),
        migrations.AlterField(
            model_name='group',
            name='daily_rumination_ranges',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), default=[10, 20, 30], size=3),
        ),
        migrations.AlterField(
            model_name='group',
            name='health_rate_ranges',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), default=[10, 20, 30], size=3),
        ),
        migrations.AlterField(
            model_name='group',
            name='ten_days_avg_rumination_ranges',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), default=[10, 20, 30], size=3),
        ),
        migrations.AlterField(
            model_name='group',
            name='ten_days_rumination_ranges',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), default=[10, 20, 30], size=3),
        ),
    ]
