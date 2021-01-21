# Generated by Django 3.1.2 on 2020-11-16 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20201116_1253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='milking',
        ),
        migrations.AlterField(
            model_name='branch',
            name='milking',
            field=models.BooleanField(blank=True, help_text='auto update by using one of the specified names', null=True),
        ),
    ]
