# Generated by Django 3.1.2 on 2021-01-14 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_auto_20210113_0745'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmkpis',
            name='happy_score',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Happy Score'),
        ),
        migrations.AddField(
            model_name='farmkpis',
            name='natural_score',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Natural Score'),
        ),
        migrations.AddField(
            model_name='farmkpis',
            name='wellbeing_score',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='WellBeing Score'),
        ),
    ]
