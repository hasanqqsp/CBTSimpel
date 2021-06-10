# Generated by Django 3.1.1 on 2021-06-10 09:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0008_auto_20210610_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='testtaker',
            name='sequences',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='questID',
            field=models.CharField(blank=True, max_length=16, unique=True),
        ),
        migrations.AlterField(
            model_name='testtaker',
            name='timeFinish',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 6, 10, 16, 37, 33, 430989), null=True),
        ),
        migrations.AlterField(
            model_name='testtaker',
            name='timeStart',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 6, 10, 16, 37, 33, 430946), null=True),
        ),
    ]